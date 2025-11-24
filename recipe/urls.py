from django.contrib import admin
from django.urls import path, include
from recipe_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ------------------------
    # Module 1: User Authentication & Dashboard
    # ------------------------
    path('', views.home_page, name='home_page'),  # Homepage/Dashboard
    path('register/', views.register, name='register'),
    # Add this line to support the standard 'login' name:
    path('login/', auth_views.LoginView.as_view(template_name='recipe_app/login.html'), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='recipe_app/login.html'), name='login_alt'),  # optional (keep both)


    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin/login/', auth_views.LoginView.as_view(template_name='recipe_app/admin_login.html'), name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='admin_logout'),
    path('admin/', admin.site.urls),

    # ------------------------
    # Static/Informational Pages
    # ------------------------
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),

    # ------------------------
    # Module 2: Smart Recipe Management Module
    # ------------------------
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('success_page/', views.success_page, name='success_page'),
    path('view_recipe_page/', views.view_recipe_page, name='view_recipe_page'),
   
    path('recipe_detail/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('home_page/', views.home_page, name='home_page'), # for buttons
    
    # ------------------------
    # Module 5: Adaptive Ingredient & Serving Scaler
    # ------------------------
    path('ingredient_scaler/', views.ingredient_scaler_view, name='ingredient_scaler'),

    # ------------------------
    # Module 4: Flame & Utensil Guidance
    # ------------------------
    path('flame_utensil_guide/<int:pk>/', views.flame_utensil_guide_view, name='flame_utensil_guide'),

    # ------------------------
    # Module 3: AI-Powered Beginner Cooking Guide
    # ------------------------
    path('beginner_guide/<int:pk>/', views.beginner_guide_view, name='beginner_guide'),
    path('beginner_guides/', views.beginner_guide_list, name='beginner_guide_list'),





    #-------------------------
    #
    #-------------------------
    path('recipe_list/', views.recipe_list_view, name='recipe_list'),



    #--------------------------
    #- - -
    #--------------------------
    path('', include('recipe_app.urls')),  




    # ------------------------
    # Module 7: Grocery Assistant & Shopping List Generator
    # ------------------------
    path('add_to_shopping_cart/<int:recipe_id>/', views.add_to_shopping_cart, name='add_to_shopping_cart'),
    path('create_shopping_list/', views.create_shopping_list, name='create_shopping_list'),
    path('shopping_list/<int:pk>/', views.view_shopping_list, name='view_shopping_list'),
    path('shopping_list/<int:pk>/export/csv/', views.export_shopping_list_csv, name='export_shopping_list_csv'),
    path('shopping_list/<int:pk>/export/pdf/', views.export_shopping_list_pdf, name='export_shopping_list_pdf'),

    



]

#  Media serving in DEBUG mode only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






