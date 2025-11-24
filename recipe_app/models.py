from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User




FLAME_LEVEL_CHOICES = [
    ('None', 'None'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]


MEAL_TYPE_CHOICES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Dessert', 'Dessert'),
    ('Salad', 'Salad'),
    ('Snack', 'Snack'),
    ('Other', 'Other'),
]


# ------------------------
# Module 2: Smart Recipe Management Module
# ------------------------
class recipe_model(models.Model):
    recipe_name = models.CharField(max_length=255)
    description = models.TextField()
    serves = models.PositiveIntegerField(default=4, help_text="Default servings for this recipe")
    image = models.ImageField(
        upload_to='recipes/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])]
        
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='Other',
        help_text="Classify this recipe by meal type",
    )

    @property
    def total_time(self):
        return self.prep_time + self.cook_time

    prep_time = models.PositiveIntegerField(default=10, help_text='Preparation time in minutes')
    cook_time = models.PositiveIntegerField(default=10, help_text='Cooking time in minutes')
    difficulty = models.CharField(max_length=20, default="Easy")
    calories = models.IntegerField(default=0)
    flame_level = models.CharField(max_length=20, choices=FLAME_LEVEL_CHOICES, default="Medium")  # <-- changed line
    utensils = models.CharField(max_length=100, default="Frying Pan")
    video_url = models.URLField(blank=True, default="")
    cooking_steps = models.TextField(default="")

    def __str__(self):
        return self.recipe_name
    



# ------------------------
# Module 9: User Query/Feedback Module
# ------------------------
class UserQuery(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"
    



# ------------------------
# Module 3: AI-Powered Beginner Cooking Guide
# ------------------------
class BeginnerGuide(models.Model):
    recipe = models.OneToOneField('recipe_model', on_delete=models.CASCADE)
    tooltip_text = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, default="")

    def __str__(self):
        return f"Guide for {self.recipe.recipe_name}"
    



# ------------------------
# Module 4: Flame & Utensil Guidance Module
# ------------------------
class CookingStep(models.Model):
    recipe = models.ForeignKey('recipe_model', on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    flame_level = models.CharField(
        max_length=20,
        choices=FLAME_LEVEL_CHOICES,  # <-- changed line
        default='Medium'
    )
    utensil = models.CharField(max_length=100, default="Frying Pan")

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number} of {self.recipe.recipe_name}"
    



# ------------------------
# Module 5: Adaptive Ingredient & Serving Scaler
# ------------------------
class Ingredient(models.Model):
    recipe = models.ForeignKey('recipe_model', on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=30, help_text='e.g., grams, cups, tsp')

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    


#---------------------------
#-------Comment Logic-------
#--------------------------
class RecipeComment(models.Model):
    recipe = models.ForeignKey('recipe_model', on_delete=models.CASCADE, related_name='recipe_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='child_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.recipe_name}"

    def helpful_count(self):
        return self.comment_ratings.filter(helpful=True).count()


class CommentRating(models.Model):
    comment = models.ForeignKey(RecipeComment, on_delete=models.CASCADE, related_name='comment_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    helpful = models.BooleanField(default=True)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"Rating by {self.user.username} ({'Helpful' if self.helpful else 'Not Helpful'})"
    

    
    
# ------------------------
# Module 7: Grocery Assistant & Shopping List Generator
# ------------------------
class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="My Shopping List")
    created_at = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField('recipe_model', help_text="Select recipes to include")

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class ShoppingListItem(models.Model):
    CATEGORIES = [
        ('Vegetables', 'Vegetables'),
        ('Fruits', 'Fruits'),
        ('Dairy', 'Dairy'),
        ('Spices', 'Spices'),
        ('Grains', 'Grains'),
        ('Proteins', 'Proteins'),
        ('Oils & Fats', 'Oils & Fats'),
        ('Other', 'Other'),
    ]
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    ingredient_name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='Other')
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ingredient_name} ({self.quantity} {self.unit})"


