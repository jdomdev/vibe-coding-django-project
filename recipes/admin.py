from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Customizes the display and functionality of the Recipe model in the Django Admin.
    """
    # 1. list_display: Fields to display in the change list page (table columns)
    #    These are the columns you'll see when you go to Recipes in the admin.
    list_display = ('title', 'created_at', 'updated_at', 'has_image')

    # 2. search_fields: Fields to search against when using the search bar
    #    Adds a search box that queries these fields.
    search_fields = ('title', 'ingredients', 'steps')

    # 3. list_filter: Fields to add filters to the right sidebar
    #    Allows filtering recipes by these fields.
    list_filter = ('created_at', 'updated_at')

    # 4. date_hierarchy: Adds a date-based drilldown navigation
    #    Useful for navigating by year, month, day.
    date_hierarchy = 'created_at'

    # 5. fields or fieldsets: Control the layout and order of fields on the add/edit form
    #    You can group fields and make them read-only if needed.
    # fields = ('title', 'image', 'image_url', 'ingredients', 'steps') # Simple list
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'image_url')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'steps'),
            'description': 'Provide the ingredients and step-by-step instructions.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Makes this section collapsible
            'description': 'Automatically managed timestamps.'
        }),
    )
    readonly_fields = ('created_at', 'updated_at') # Prevent manual editing of timestamps

    # Custom method for list_display to show if an image exists
    def has_image(self, obj):
        return bool(obj.image or obj.image_url)
    has_image.boolean = True # Displays a nice checkmark/X icon
    has_image.short_description = 'Image' # Column header name