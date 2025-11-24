from django.contrib import admin
from django.urls import path, include
from recipe_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Module 2: Smart Recipe Management Module
   
    path("success_page/", views.success_page, name="success_page"),  # Success confirmation
    path("view_recipe_page/", views.view_recipe_page, name="view_recipe_page"),  # List & search recipes

    # Fixed: Using existing view 'recipe_detail' (delete detail_page if unused)
    path("recipe_detail/<int:pk>/", views.recipe_detail, name='recipe_detail'),

    # Module 1: User Authentication & Dashboard
    path("home_page/", views.home_page, name="home_page_buttons"),  # Dashboard/home after login

    # Module 4: Flame & Utensil Guidance
    path('flame_utensil_guide/<int:pk>/', views.flame_utensil_guide_view, name='flame_utensil_guide'),

    # Module 3: AI-Powered Beginner Cooking Guide
    path('beginner_guide/<int:pk>/', views.beginner_guide_view, name='beginner_guide'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='recipe_app/login.html'), name='login'),

    # Comment Logic
    path('recipe/<int:pk>/add_comment/', views.add_recipe_comment, name='add_recipe_comment'),
    path('rate_comment/', views.rate_comment, name='rate_comment'),
    path('recipe/<int:pk>/comments/', views.recipe_comments_list, name='recipe_comments_list'),


    #module no . 7 
    path('shopping_cart/<int:recipe_id>/', views.add_to_shopping_cart, name='add_to_shopping_cart'),
    path('shopping_cart/', views.view_shopping_cart, name='view_shopping_cart'),
    path('generate_shopping_list/', views.generate_shopping_list, name='generate_shopping_list'),
    
    
]
