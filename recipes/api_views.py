# recipes/api_views.py
from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Recipe instances.
    Provides 'list', 'create', 'retrieve', 'update', 'partial_update', and 'destroy' actions.
    """
    queryset = Recipe.objects.all().order_by('title') # Define the base queryset
    serializer_class = RecipeSerializer # Link the serializer to this ViewSet

    # Optional: You can customize individual actions if needed
    # def list(self, request, *args, **kwargs):
    #     # Custom logic for listing recipes
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     # Custom logic for creating recipes
    #     return super().create(request, *args, **kwargs)