# recipes/forms.py
from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """
    A ModelForm for the Recipe model.
    This form is used for both creating new recipes and updating existing ones.
    It automatically generates form fields based on the Recipe model.
    """
    class Meta:
        # Link this form to the Recipe model
        model = Recipe
        # Specify which fields from the Recipe model should be included in the form.
        # This list directly corresponds to the input fields the user will see.
        fields = ['title', 'image', 'image_url', 'ingredients', 'steps']
        
        # Optional: Customize the HTML widgets for specific fields for better UX.
        # Here, we make the text areas for ingredients and steps larger.
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }
        
        # Optional: Provide custom help text for fields, which will display next to the input.
        help_texts = {
            'image': 'Upload an image file for the recipe. This will take precedence over an Image URL.',
            'image_url': 'Alternatively, you can provide a direct URL to an external image.',
        }