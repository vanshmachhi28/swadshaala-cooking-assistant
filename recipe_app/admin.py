from django.contrib import admin
from .models import CommentRating, RecipeComment, ShoppingList, ShoppingListItem, recipe_model, BeginnerGuide, UserQuery, CookingStep, Ingredient

# ------------------------
# Module 2: Smart Recipe Management Module
# ------------------------
@admin.register(recipe_model)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "recipe_name", "meal_type", "prep_time", "cook_time", "total_time", "description", "image"
    ]
    list_filter = ['meal_type', 'difficulty']
# ------------------------
# Module 9: User Query/Feedback Module
# ------------------------
@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')

# ------------------------
# Module 3: AI-Powered Beginner Cooking Guide
# ------------------------
@admin.register(BeginnerGuide)
class BeginnerGuideAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tooltip_text', 'video_url')

# ------------------------
# Module 4: Flame & Utensil Guidance Module
# ------------------------
@admin.register(CookingStep)
class CookingStepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'step_number', 'flame_level', 'utensil')
    list_filter = ('recipe', 'flame_level', 'utensil')
    ordering = ('recipe', 'step_number')

# ------------------------
# Module 5: Adaptive Ingredient & Serving Scaler
# ------------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'name', 'quantity', 'unit')
    list_filter = ('recipe',)






#-----------------------------
#------Comment Logic-----------
#------------------------------
@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'content', 'created_at', 'parent')
    search_fields = ('content', 'user__username', 'recipe__recipe_name')
    readonly_fields = ('created_at',)

@admin.register(CommentRating)
class CommentRatingAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'helpful')
    list_filter = ('helpful', 'user')


#--------------------------------------------
#------Module no . 7 Grocery Assistant & ----
# -------Shopping List Generator-------------
#--------------------------------------------

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'recipe_count')
    list_filter = ('user', 'created_at')
    filter_horizontal = ('recipes',)

    def recipe_count(self, obj):
        return obj.recipes.count()
    recipe_count.short_description = "Recipes Included"

@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name', 'quantity', 'unit', 'category', 'shopping_list', 'checked')
    list_filter = ('category', 'checked', 'shopping_list')
    


