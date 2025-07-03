import tempfile
from PIL import Image # Pillow is needed for creating dummy images
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe

class RecipeModelTest(TestCase):
    """
    Tests for the Recipe model.
    Verifies creation, retrieval, string representation, and custom methods.
    """

    def setUp(self):
        """
        Set up a dummy recipe instance for testing.
        """
        # Create a dummy image file for testing ImageField
        image_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(image_file, 'jpeg')
        image_file.close()
        self.image_path = image_file.name

        # Create a SimpleUploadedFile instance
        with open(self.image_path, 'rb') as f:
            self.uploaded_image = SimpleUploadedFile(
                name='test_image.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )

        self.recipe = Recipe.objects.create(
            title="Spicy Chicken Curry",
            ingredients="Chicken, Spices, Coconut Milk",
            steps="1. Cook chicken. 2. Add spices. 3. Simmer.",
            image=self.uploaded_image # Assign the SimpleUploadedFile
        )
        self.recipe_no_image = Recipe.objects.create(
            title="Simple Salad",
            ingredients="Lettuce, Tomato, Cucumber",
            steps="1. Chop veggies. 2. Mix."
        )
        self.recipe_with_image_url = Recipe.objects.create(
            title="Pasta Primavera",
            ingredients="Pasta, Vegetables, Olive Oil",
            steps="1. Boil pasta. 2. Sauté veggies.",
            image_url="http://example.com/pasta.jpg"
        )

    def tearDown(self):
        """
        Clean up dummy image files after tests.
        """
        import os
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        # Ensure uploaded media files are cleaned up by Django's test runner
        # or manually if necessary for specific cases.

    def test_recipe_creation(self):
        """
        Test that a Recipe object can be created and its fields are correct.
        """
        self.assertEqual(self.recipe.title, "Spicy Chicken Curry")
        self.assertEqual(self.recipe.ingredients, "Chicken, Spices, Coconut Milk")
        self.assertEqual(self.recipe.steps, "1. Cook chicken. 2. Add spices. 3. Simmer.")
        self.assertIsNotNone(self.recipe.created_at)
        self.assertIsNotNone(self.recipe.updated_at)
        self.assertTrue(self.recipe.image.name.endswith('test_image.jpg')) # Check image name
        self.assertIsNone(self.recipe.image_url) # Should be None as image was uploaded

    def test_recipe_str_method(self):
        """
        Test the __str__ method returns the recipe title.
        """
        self.assertEqual(str(self.recipe), "Spicy Chicken Curry")

    def test_get_absolute_url(self):
        """
        Test that get_absolute_url returns the correct URL for the recipe detail view.
        """
        expected_url = reverse('recipes:recipe_detail', args=[self.recipe.pk])
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)

    def test_get_image_display_url(self):
        """
        Test the get_image_display_url method's logic.
        """
        # Case 1: Image uploaded
        self.assertIn('test_image.jpg', self.recipe.get_image_display_url())

        # Case 2: No image, but image_url provided
        self.assertEqual(self.recipe_with_image_url.get_image_display_url(), "http://example.com/pasta.jpg")

        # Case 3: Neither image nor image_url provided
        self.assertEqual(self.recipe_no_image.get_image_display_url(), 'https://via.placeholder.com/150?text=No+Image')

    def test_unique_title_constraint(self):
        """
        Test that creating a recipe with a duplicate title raises an IntegrityError.
        """
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(
                title="Spicy Chicken Curry", # Duplicate title
                ingredients="Different ingredients",
                steps="Different steps"
            )

class RecipeViewTest(TestCase):
    """
    Integration tests for Recipe views (ListView, DetailView, CreateView, UpdateView, DeleteView).
    Simulates HTTP requests and checks responses, templates, and context.
    """

    def setUp(self):
        """
        Set up a client and some recipe instances for view testing.
        """
        self.client = Client()
        self.recipe1 = Recipe.objects.create(
            title="Breakfast Burrito",
            ingredients="Eggs, Tortilla, Cheese",
            steps="1. Scramble eggs. 2. Wrap."
        )
        self.recipe2 = Recipe.objects.create(
            title="Chocolate Chip Cookies",
            ingredients="Flour, Sugar, Chocolate Chips",
            steps="1. Mix. 2. Bake."
        )

        # URLs for testing
        self.list_url = reverse('recipes:recipe_list')
        self.detail_url = reverse('recipes:recipe_detail', args=[self.recipe1.pk])
        self.create_url = reverse('recipes:recipe_create')
        self.update_url = reverse('recipes:recipe_update', args=[self.recipe1.pk])
        self.delete_url = reverse('recipes:recipe_delete', args=[self.recipe1.pk])

    def test_recipe_list_view(self):
        """
        Test RecipeListView: GET request, status code, template, and context.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertIn('recipes', response.context) # Check if 'recipes' is in context
        self.assertEqual(len(response.context['recipes']), 2) # Check number of recipes
        self.assertContains(response, self.recipe1.title) # Check if recipe title is in content
        self.assertContains(response, self.recipe2.title)

    def test_recipe_detail_view(self):
        """
        Test RecipeDetailView: GET request, status code, template, and context.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertIn('recipe', response.context) # Check if 'recipe' is in context
        self.assertEqual(response.context['recipe'], self.recipe1) # Check if correct recipe
        self.assertContains(response, self.recipe1.title)
        self.assertContains(response, self.recipe1.ingredients)
        self.assertContains(response, self.recipe1.steps)

    def test_recipe_detail_view_404(self):
        """
        Test RecipeDetailView for a non-existent recipe (should return 404).
        """
        response = self.client.get(reverse('recipes:recipe_detail', args=[9999])) # Non-existent PK
        self.assertEqual(response.status_code, 404) # Not Found

    def test_recipe_create_view_get(self):
        """
        Test RecipeCreateView (GET request): status code and template.
        """
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertContains(response, '<form') # Check for form tag

    def test_recipe_create_view_post_valid_data(self):
        """
        Test RecipeCreateView (POST request with valid data): redirect, and database creation.
        """
        initial_recipe_count = Recipe.objects.count()
        
        # Create a dummy image file for POST request
        image_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        img = Image.new('RGB', (100, 100), color = 'blue')
        img.save(image_file, 'jpeg')
        image_file.close()
        
        with open(image_file.name, 'rb') as f:
            uploaded_image = SimpleUploadedFile(
                name='new_recipe_image.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )

            response = self.client.post(self.create_url, {
                'title': 'New Delicious Cake',
                'ingredients': 'Flour, Sugar, Eggs',
                'steps': '1. Mix. 2. Bake.',
                'image': uploaded_image # Include image in POST data
            })
        
        import os # Clean up the temporary image file
        if os.path.exists(image_file.name):
            os.remove(image_file.name)

        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertEqual(Recipe.objects.count(), initial_recipe_count + 1) # One more recipe
        new_recipe = Recipe.objects.get(title='New Delicious Cake')
        self.assertRedirects(response, reverse('recipes:recipe_detail', args=[new_recipe.pk]))

    def test_recipe_create_view_post_invalid_data(self):
        """
        Test RecipeCreateView (POST request with invalid data): form redisplay and errors.
        """
        initial_recipe_count = Recipe.objects.count()
        response = self.client.post(self.create_url, {
            'title': '', # Invalid: title is required
            'ingredients': 'Some ingredients',
            'steps': 'Some steps'
        })
        self.assertEqual(response.status_code, 200) # Form redisplayed
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors) # Check for form errors
        self.assertContains(response, 'This field is required.') # Specific error message
        self.assertEqual(Recipe.objects.count(), initial_recipe_count) # No new recipe created

    def test_recipe_update_view_get(self):
        """
        Test RecipeUpdateView (GET request): status code, template, and pre-populated form.
        """
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance, self.recipe1) # Form pre-populated with recipe1
        self.assertContains(response, self.recipe1.title) # Check if existing title is in form

    def test_recipe_update_view_post_valid_data(self):
        """
        Test RecipeUpdateView (POST request with valid data): redirect and database update.
        """
        updated_title = "Updated Breakfast Burrito"
        response = self.client.post(self.update_url, {
            'title': updated_title,
            'ingredients': self.recipe1.ingredients,
            'steps': self.recipe1.steps
        })
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.recipe1.refresh_from_db() # Reload recipe1 from database
        self.assertEqual(self.recipe1.title, updated_title) # Check if title updated
        self.assertRedirects(response, reverse('recipes:recipe_detail', args=[self.recipe1.pk]))

    def test_recipe_update_view_post_invalid_data(self):
        """
        Test RecipeUpdateView (POST request with invalid data): form redisplay and errors.
        """
        original_title = self.recipe1.title
        response = self.client.post(self.update_url, {
            'title': '', # Invalid: title is required
            'ingredients': self.recipe1.ingredients,
            'steps': self.recipe1.steps
        })
        self.assertEqual(response.status_code, 200) # Form redisplayed
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertTrue(response.context['form'].errors)
        self.assertContains(response, 'This field is required.')
        self.recipe1.refresh_from_db()
        self.assertEqual(self.recipe1.title, original_title) # Title should not have changed

    def test_recipe_delete_view_get(self):
        """
        Test RecipeDeleteView (GET request): status code and template.
        """
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'recipes/recipe_confirm_delete.html')
        self.assertContains(response, f'Are you sure you want to delete the recipe "<strong>{self.recipe1.title}</strong>"?')

    def test_recipe_delete_view_post(self):
        """
        Test RecipeDeleteView (POST request): redirect and database deletion.
        """
        initial_recipe_count = Recipe.objects.count()
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertEqual(Recipe.objects.count(), initial_recipe_count - 1) # One less recipe
        self.assertFalse(Recipe.objects.filter(pk=self.recipe1.pk).exists()) # Recipe should be deleted
        self.assertRedirects(response, self.list_url) # Redirects to list view