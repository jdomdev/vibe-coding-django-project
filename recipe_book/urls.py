from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_recipes(request):
    return redirect('recipes:recipe_list')

urlpatterns = [
    path('', redirect_to_recipes, name='home'),  # Redirige la ruta raíz a recipes
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')), # Include your recipes app URLs    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Not strictly necessary for STATIC_URL in DEBUG, but good for completeness