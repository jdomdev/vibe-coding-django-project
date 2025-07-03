from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    """
    Represents a single recipe in the personal collection.
    """
    title = models.CharField(
        max_length=200,
        unique=True,  # Ensure recipe titles are unique for easy identification
        help_text="The name of the recipe."
    )
    image = models.ImageField(
        upload_to='recipe_images/',  # Images will be stored in media/recipe_images/
        blank=True,  # Image is optional
        null=True,   # Allows the database column to be NULL
        help_text="Upload an image for the recipe. Optional."
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Alternatively, provide a URL for the recipe image. Optional."
    )
    ingredients = models.TextField(
        help_text="List all ingredients, separated by newlines or commas. Markdown formatting allowed."
    )
    steps = models.TextField(
        help_text="Provide step-by-step instructions for preparing the recipe. Markdown formatting allowed."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically sets the creation timestamp when the object is first created
        help_text="The date and time when the recipe was added."
    )
    updated_at = models.DateTimeField(
        auto_now=True,      # Automatically updates the timestamp every time the object is saved
        help_text="The date and time when the recipe was last updated."
    )

    class Meta:
        # Define the default ordering for querysets
        ordering = ['title']
        # Add a verbose name for the model, which will appear in the Django admin
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        """
        String representation of the Recipe object, useful for the admin interface.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to access a particular instance of the recipe.
        This is a Django best practice for models and is used by DetailView, UpdateView etc.
        """
        return reverse('recipes:recipe_detail', args=[str(self.id)])

    def get_image_display_url(self):
        """
        Helper method to return either the uploaded image URL or the provided image_url.
        Prioritizes uploaded image over URL.
        """
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return 'https://via.placeholder.com/150?text=No+Image' # Placeholder if neither is provided