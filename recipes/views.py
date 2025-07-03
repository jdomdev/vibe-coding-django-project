# recipes/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # Used for success_url with CBVs
from .models import Recipe
from .forms import RecipeForm # Import our newly created form

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    # paginate_by = 10

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