
def generateModel(components):
  with open(f"generated/models.py","w") as file:
    # --- Write Header ---
    file.write(generateModelHeader())

    for name, data in components.get('schemas',{}).items():
      # --- Write Class Header ---
      file.write(generateClassHeader(name))
      # --- Write Class Properties ---
      for property, item in data.get('properties',{}).items():
        file.write(f"  {property} = {formingField(item)}\n")
      # --- Write Class Footer ---
      file.write(generateClassFooter(data))

# =========+=========+=========+=========+=========+
# UTILITY
# =========+=========+=========+=========+=========+
def generateModelHeader():
  return f"""
from django.db import models
from django.core.exceptions import ValidationError

class BaseModelClass(models.Model):
  # === Base Properties ===
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    abstract = True

  def valid_list(target):
    if not isinstance(target, dict):
      raise ValidationError("This field must be a LIST...")
  def valid_dict(target):
    if not isinstance(target, dict):
      raise ValidationError("This field must be a JSON...")

# =========+=========+=========+=========+=========+
# Models
# =========+=========+=========+=========+=========+
"""
def generateClassHeader(name):
  return f"""
class {name}(BaseModelClass):
  # === Properties ===
"""
def generateClassFooter(data):
  return f"""
  # === Meta ===
  class Meta:
    verbose_name = "{data.get('description')}"
    ordering = ['-created_at']

  def __str__(self):
    return f"{{self.name}}"
# =========+=========+=========+=========+=========+
"""

def formingField(item):
  type_data   = item.get('type')
  default     = item.get('default')
  description = item.get('description')
  match type_data:
    case "string" : return formingStringField(item)
    case "number" : return f"models.FloatField(default=0, verbose_name=\"{description}\")"
    case "integer": return f"models.IntegerField(default=0, verbose_name=\"{description}\")"
    case "boolean": return f"models.BooleanField(default={default}, verbose_name=\"{description}\")"
    case "array"  : return f"models.JSONField(validators=[BaseModelClass().valid_list], default=list, verbose_name=\"{description}\")"
    case "object" : return f"models.JSONField(validators=[BaseModelClass().valid_dict], default=dict, verbose_name=\"{description}\")"
    case _:  return "-1 #Invalid Field Data"

def formingStringField(item):
  format_data = item.get('format')
  description = item.get('description')
  max_length  = item.get('maxLength')
  match format_data:
    case "date"     : return f"models.DateField(default=\"1990-01-01\", verbose_name=\"{description}\")"
    case "date-time": return f"models.DateTimeField(default=\"1990-01-01 12:00:00\", verbose_name=\"{description}\")"
    case None:
      if max_length:
        return f"models.CharField(max_length={max_length}, default=\"\", verbose_name=\"{description}\")"
      else:
        return f"models.TextField(default=\"\", verbose_name=\"{description}\")"
    case _:  return "-1 #Invalid Field Data"



