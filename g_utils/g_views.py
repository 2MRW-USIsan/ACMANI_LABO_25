def generateView(paths):
  viewSets = []
  for path, _ in paths.items():
    api_name = path.split("/")[1].capitalize()
    if api_name in viewSets:
      continue
    else:
      viewSets.append(api_name)
  with open(f"generated/views.py","w") as file:
    # --- Write Header ---
    file.write(generateViewsHeader())
    for name in viewSets:
      # --- Write ViewSets Class ---
      file.write(generateViewsClass(name))

  with open(f"generated/urls.py","w") as file:
    # --- Write Header ---
    file.write(generateURLsHeader())
    for name in viewSets:
      # --- Write ViewSets Class ---
      file.write(generateURLsClass(name))
    # --- Write Footer ---
    file.write(generateURLsFooter())



# =========+=========+=========+=========+=========+
# UTILITY
# =========+=========+=========+=========+=========+
def generateViewsHeader():
  return f"""
from rest_framework import viewsets
from .models import *
from .serializers import *

# =========+=========+=========+=========+=========+
# ViewSets
# =========+=========+=========+=========+=========+
"""

def generateViewsClass(name):
  return f"""
class {name}ViewSet(viewsets.ModelViewSet):
  queryset = BaseModelClass.objects.all() # FIX Model
  serializer_class  = BaseModelClass.objects.all() # FIX Serializer
# =========+=========+=========+=========+=========+
"""

def generateURLsHeader():
  return f"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from .views import *

# Initialize
router = DefaultRouter()
"""

def generateURLsClass(name):
  return f"""router.register(r'{name.lower()}', {name}ViewSet)
"""

def generateURLsFooter():
  return f"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('', include(router.urls)),
]
"""