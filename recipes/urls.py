# recipes/urls.py
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Recipe List
    path('', views.RecipeListView.as_view(), name='recipe_list'),

    # Recipe Detail
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),

    # Add New Recipe
    path('add/', views.RecipeCreateView.as_view(), name='recipe_create'),

    # Edit Existing Recipe
    path('<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe_update'),

    # Delete Recipe
    path('<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
]