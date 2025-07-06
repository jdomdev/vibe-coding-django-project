# recipes/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q # Import Q object for complex lookups

from .models import Recipe
from .forms import RecipeForm

class RecipeListView(ListView):
    """
    Displays a list of all recipes, with optional search functionality.
    """
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9 # Example pagination: 9 recipes per page

    def get_queryset(self):
        """
        Returns the queryset of recipes, optionally filtered by a search query.
        """
        queryset = super().get_queryset() # Get the default ordered queryset
        query = self.request.GET.get('q') # Get the search query from the URL parameter 'q'

        if query:
            # Use Q objects for OR conditions across multiple fields
            # icontains makes the search case-insensitive
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(ingredients__icontains=query) |
                Q(steps__icontains=query)
            ).distinct() # Use .distinct() to avoid duplicate results if a recipe matches multiple Q conditions

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds the search query back to the context so the search bar can retain its value.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '') # Pass the search query back to the template
        return context

# ... (RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView remain unchanged)

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    """
    Handles the creation of a new recipe.
    Uses RecipeForm for form validation and rendering.
    """
    model = Recipe
    form_class = RecipeForm # Use our custom ModelForm
    template_name = 'recipes/recipe_form.html' # Reusing a generic form template
    # success_url = reverse_lazy('recipes:recipe_list') # Redirect to list after creation

    def get_success_url(self):
        """
        Redirect to the detail page of the newly created recipe.
        """
        return reverse_lazy('recipes:recipe_detail', kwargs={'pk': self.object.pk})

class RecipeUpdateView(UpdateView):
    """
    Handles the updating of an existing recipe.
    Uses RecipeForm for form validation and rendering.
    """
    model = Recipe
    form_class = RecipeForm # Use our custom ModelForm
    template_name = 'recipes/recipe_form.html' # Reusing the generic form template
    context_object_name = 'recipe' # The object being edited will be available as 'recipe' in template
    # success_url = reverse_lazy('recipes:recipe_list') # Redirect to list after update

    def get_success_url(self):
        """
        Redirect to the detail page of the updated recipe.
        """
        return reverse_lazy('recipes:recipe_detail', kwargs={'pk': self.object.pk})

class RecipeDeleteView(DeleteView):
    """
    Handles the deletion of a recipe.
    """
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html' # Template to confirm deletion
    context_object_name = 'recipe' # The object to be deleted will be available as 'recipe'
    success_url = reverse_lazy('recipes:recipe_list') # Redirect to list after deletion