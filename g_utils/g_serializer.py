def generateSerializer(components):
  with open(f"generated/serializers.py","w") as file:
    # --- Write Header ---
    file.write(generateSerializerHeader())

    for name, data in components.get('schemas',{}).items():
      # --- Write Class ---
      file.write(generateSerializerClass(name, data))


# =========+=========+=========+=========+=========+
# UTILITY
# =========+=========+=========+=========+=========+
def generateSerializerHeader():
  return f"""
from rest_framework import serializers
from .models import *

# =========+=========+=========+=========+=========+
# Serializers
# =========+=========+=========+=========+=========+
"""

def generateSerializerClass(name, data):
  return f"""
class {name}Serializer(serializers.ModelSerializer):
  class Meta:
    model = {name}
    base_props   = [\"id\", \"created_at\", \"updated_at\", \"deleted_at\"]
    fields_props = {list(data.get('properties').keys())}
# =========+=========+=========+=========+=========+
"""