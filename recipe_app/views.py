import re
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import CommentRating, RecipeComment, ShoppingList, ShoppingListItem, recipe_model, BeginnerGuide
from .forms import RecipeForm, UserRegisterForm, UserQueryForm


# ------------------------
# Module 1: User Authentication & Dashboard
# ------------------------


@login_required(login_url='login')
def home_page(request):
    return render(request, 'recipe_app/home_page.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # auto-login after registration
            return redirect('home_page')
    else:
        form = UserRegisterForm()
    return render(request, 'recipe_app/register.html', {'form': form})


# ------------------------
# Module 2: Smart Recipe Management
# ------------------------


def add_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if name and description:
            data = recipe_model(recipe_name=name, description=description, image=image)
            data.save()
            return redirect("success_page")
        else:
            return render(request, "recipe_app/home_page.html")
    return render(request, 'recipe_app/add_recipe.html')


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe uploaded successfully!")
            return redirect('success_page')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipeForm()
    return render(request, 'recipe_app/add_recipe.html', {'form': form})


def success_page(request):
    return render(request, 'recipe_app/success_page.html')


# ------------------------
# Module 6: Meal Type & Time Classification
# ------------------------

def view_recipe_page(request):
    search_query = request.GET.get('recipe_name', '')
    filter_meal = request.GET.get('meal_type', None)
    recipes = recipe_model.objects.all()
    if search_query:
        recipes = recipes.filter(recipe_name__icontains=search_query)
    if filter_meal:
        recipes = recipes.filter(meal_type=filter_meal)
    recipes = recipes.order_by("-id")
    return render(request, 'recipe_app/view_recipe_page.html', {'get_all': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(recipe_model, pk=pk)
    return render(request, 'recipe_app/recipe_detail.html', {'data': recipe})


# ------------------------
# Module 9: User Query/Feedback
# ------------------------


def contact_us(request):
    if request.method == 'POST':
        form = UserQueryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'recipe_app/success_page.html')
    else:
        form = UserQueryForm()
    return render(request, 'recipe_app/contact_us.html', {'form': form})


# ------------------------
# Module 3: AI-Powered Beginner Cooking Guide
# ------------------------


def beginner_guide_view(request, pk):
    recipe = get_object_or_404(recipe_model, pk=pk)
    guide = BeginnerGuide.objects.filter(recipe_id=pk).first()
    return render(request, "recipe_app/beginner_guide.html", {
        "recipe": recipe,
        "guide": guide
    })


def beginner_guide_list(request):
    guides = BeginnerGuide.objects.select_related('recipe').all()
    return render(request, 'recipe_app/beginner_guide_list.html', {'guides': guides})


# ------------------------
# Module 4: Flame & Utensil Guidance (Step-by-step)
# ------------------------


def flame_utensil_guide_view(request, pk):
    recipe = get_object_or_404(recipe_model, pk=pk)
    steps = recipe.steps.all()
    return render(request, 'recipe_app/flame_utensil_guide.html', {'recipe': recipe, 'steps': steps})


# ------------------------
# Module 5: Adaptive Ingredient & Serving Scaler
# ------------------------


def extract_int(raw_serves):
    """ Extracts integer from a string like '4 people' or '4' """
    if isinstance(raw_serves, int):
        return raw_serves
    if not raw_serves:
        return 1
    match = re.search(r'\d+', str(raw_serves))
    return int(match.group()) if match else 1


def ingredient_scaler_view(request):
    recipes = recipe_model.objects.all().order_by('recipe_name')

    recipe_id = request.GET.get('recipe_id')
    if recipe_id:
        recipe = get_object_or_404(recipe_model, pk=recipe_id)
    else:
        recipe = recipes.first()

    base_servings = extract_int(recipe.serves)

    try:
        servings_raw = request.GET.get('servings', base_servings)
        servings = extract_int(servings_raw)
        if servings <= 0:
            servings = base_servings
    except Exception:
        servings = base_servings

    factor = servings / base_servings

    scaled_ingredients = [
        {
            'name': ing.name,
            'quantity': round(ing.quantity * factor, 2),
            'unit': ing.unit,
        }
        for ing in recipe.ingredients.all()
    ]

    context = {
        'recipes': recipes,
        'recipe': recipe,
        'servings': servings,
        'scaled_ingredients': scaled_ingredients,
        'default_servings': base_servings,
    }
    return render(request, 'recipe_app/ingredient_scaler.html', context)


# ------------------------
# Standard informational/static pages
# ------------------------


def about_us(request):
    return render(request, 'recipe_app/about_us.html')


# ---------------------------------------
# Additional helper view for listing all recipes (optional)
# -----------------------------------------
def recipe_list_view(request):
    meal_types = ["Breakfast", "Salad", "Lunch", "Snack", "Dinner", "Dessert"]
    # Always order recipes by meal_type first for grouping
    recipes = recipe_model.objects.all().order_by("meal_type", "-id")
    return render(request, "recipe_app/recipe_list.html", {
        "recipes": recipes,
        "meal_types": meal_types,
    })






#--------------------------
#-----Comment Logic------
#--------------------------
@login_required
def add_recipe_comment(request, pk):
    recipe = get_object_or_404(recipe_model, pk=pk)
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')

    if content:
        parent_comment = RecipeComment.objects.filter(pk=parent_id).first() if parent_id else None
        comment = RecipeComment.objects.create(recipe=recipe, user=request.user, content=content, parent=parent_comment)
        return JsonResponse({'success': True, 'comment_id': comment.id})
    return HttpResponseBadRequest('Missing content.')

@login_required
def rate_comment(request):
    comment_id = request.POST.get('comment_id')
    helpful = request.POST.get('helpful', 'true') == 'true'
    comment = RecipeComment.objects.filter(pk=comment_id).first()
    if not comment:
        return HttpResponseBadRequest('Comment does not exist.')
    rating, created = CommentRating.objects.get_or_create(comment=comment, user=request.user)
    rating.helpful = helpful
    rating.save()
    # Make sure you added `helpful_count()` method in RecipeComment model as discussed before.
    return JsonResponse({'success': True, 'helpful_count': comment.helpful_count()})

def recipe_comments_list(request, pk):
    recipe = get_object_or_404(recipe_model, pk=pk)
    comments = recipe.recipe_comments.select_related('user').prefetch_related('child_comments', 'comment_ratings').order_by('-created_at')
    return render(request, 'recipe_app/recipe_comments_list.html', {'comments': comments, 'recipe': recipe})








#--------------------------------------------
#------Module no . 7 Grocery Assistant & ----
# -------Shopping List Generator-------------
#--------------------------------------------

@login_required
def create_shopping_list(request):
    if request.method == 'POST':
        recipe_ids = request.POST.getlist('recipe_ids')
        if not recipe_ids:
            messages.error(request, "Please select at least one recipe.")
            return redirect('view_recipe_page')
        recipes = recipe_model.objects.filter(id__in=recipe_ids)
        shopping_list = ShoppingList.objects.create(user=request.user, name="Grocery List")
        shopping_list.recipes.set(recipes)

        category_map = {
            'Tomato|Onion|Potato|Carrot|Spinach|Cabbage|Cucumber|Pepper|Broccoli|Cauliflower': 'Vegetables',
            'Apple|Banana|Orange|Mango|Grapes|Papaya': 'Fruits',
            'Milk|Cheese|Butter|Yogurt|Cream': 'Dairy',
            'Salt|Pepper|Turmeric|Cumin|Coriander|Chili|Garam Masala': 'Spices',
            'Rice|Wheat|Oats|Pasta|Bread': 'Grains',
            'Chicken|Egg|Fish|Paneer|Tofu|Beef': 'Proteins',
            'Oil|Ghee|Butter': 'Oils & Fats',
        }

        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                name = ingredient.name.lower()
                category = 'Other'
                for keywords, cat in category_map.items():
                    if any(k.lower() in name for k in keywords.split('|')):
                        category = cat
                        break

                ShoppingListItem.objects.create(
                    shopping_list=shopping_list,
                    ingredient_name=ingredient.name,
                    quantity=ingredient.quantity,
                    unit=ingredient.unit,
                    category=category
                )

        messages.success(request, "Shopping list created successfully!")
        return redirect('view_shopping_list', pk=shopping_list.pk)

    return redirect('view_recipe_page')

@login_required
def view_shopping_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    items_by_category = {}
    for item in shopping_list.items.all().order_by('category', 'ingredient_name'):
        items_by_category.setdefault(item.category, []).append(item)

    return render(request, 'recipe_app/shopping_list.html', {
        'shopping_list': shopping_list,
        'items_by_category': items_by_category,
        'user': request.user,
    })

@login_required
def export_shopping_list_csv(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{shopping_list.name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Category', 'Ingredient', 'Quantity', 'Unit'])
    for item in shopping_list.items.all().order_by('category'):
        writer.writerow([item.category, item.ingredient_name, item.quantity, item.unit])

    return response

@login_required
def export_shopping_list_pdf(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph(f"<b>{shopping_list.name}</b>", styles['Title'])
    elements.append(title)

    data = [['Category', 'Ingredient', 'Qty', 'Unit']]
    for item in shopping_list.items.all().order_by('category'):
        data.append([item.category, item.ingredient_name, item.quantity, item.unit])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff8928')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fff8ee')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#f47321'))
    ]))
    elements.append(table)

    elements.append(Paragraph("<br/><br/>By SwadShaala Team", styles['Normal']))
    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')



@login_required
def add_to_shopping_cart(request, recipe_id):
    recipe = get_object_or_404(recipe_model, pk=recipe_id)
    cart = request.session.get('shopping_cart', [])
    added_count = 0
    for ingredient in recipe.ingredients.all():
        item = {'name': ingredient.name, 'quantity': ingredient.quantity, 'unit': ingredient.unit}
        if item not in cart:
            cart.append(item)
            added_count += 1
    request.session['shopping_cart'] = cart
    request.session.modified = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "added": added_count, "cart_count": len(cart)})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




@login_required
def view_shopping_cart(request):
    cart = request.session.get('shopping_cart', [])
    return render(request, 'recipe_app/shopping_cart.html', {
        'cart': cart,
        'ingredient_count': len(cart),
        'user': request.user,
    })


@login_required
def generate_shopping_list(request):
    cart = request.session.get('shopping_cart', [])
    return render(request, 'recipe_app/generated_shopping_list.html', {
        'cart': cart,
        'user': request.user,
    })


