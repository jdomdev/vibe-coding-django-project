# recipes/urls.py
from django.urls import path
from . import views

app_name = 'recipes' # This is important for namespacing URLs

urlpatterns = [
    # path('', views.recipe_list, name='recipe_list'),
    # path('add/', views.recipe_create, name='recipe_create'),
    # path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    # path('<int:pk>/edit/', views.recipe_update, name='recipe_update'),
    # path('<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
]