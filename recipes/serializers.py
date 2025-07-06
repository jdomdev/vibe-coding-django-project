# recipes/serializers.py
from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.
    Converts Recipe model instances to JSON and vice-versa.
    """
    # Custom field to get the full URL for the image, prioritizing uploaded image
    # read_only=True means this field is not used for creating/updating the model
    image_display_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        # Fields to include in the serialized output.
        # '__all__' includes all model fields. You can also specify a tuple of field names.
        fields = ['id', 'title', 'image', 'image_url', 'image_display_url', 'ingredients', 'steps', 'created_at', 'updated_at']
        # read_only_fields are fields that will be included in the output but cannot be set via the API
        read_only_fields = ['created_at', 'updated_at']

    def get_image_display_url(self, obj):
        """
        Returns the appropriate image URL for display.
        Uses the helper method defined in the Recipe model.
        """
        request = self.context.get('request')
        if request is not None:
            # Build absolute URL for uploaded image if it exists
            if obj.image:
                return request.build_absolute_uri(obj.image.url)
            elif obj.image_url:
                return obj.image_url
        # Fallback if no request context or no image
        return obj.get_image_display_url() # Use the model's method as a fallback