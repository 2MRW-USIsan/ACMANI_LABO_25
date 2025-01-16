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

class BaseModelClassSerializer(serializers.ModelSerializer):
  class Meta:
    abstract = True
    model = BaseModelClass
    base_props   = [\"id\", \"created_at\", \"updated_at\", \"deleted_at\"]

# =========+=========+=========+=========+=========+
# Serializers
# =========+=========+=========+=========+=========+
"""

def generateSerializerClass(name, data):
  return f"""
class {name}Serializer(BaseModelClassSerializer):
  class Meta:
    model = {name}
    fields_props = {list(data.get('properties').keys())}
# =========+=========+=========+=========+=========+
"""