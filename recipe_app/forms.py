from django import forms
from .models import recipe_model, UserQuery, FLAME_LEVEL_CHOICES
from django.contrib.auth.models import User



class RecipeForm(forms.ModelForm):
    flame_level = forms.ChoiceField(choices=FLAME_LEVEL_CHOICES)  # Explicit dropdown, optional




class RecipeForm(forms.ModelForm):
    class Meta:
        model = recipe_model
        fields = [
            "recipe_name", "description", "image", "prep_time",
            "serves", "difficulty", "cooking_steps",
            "utensils", "cook_time", "calories", "flame_level", "video_url"
        ]


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserQueryForm(forms.ModelForm):
    class Meta:
        model = UserQuery
        fields = ['name', 'email', 'subject', 'message']
