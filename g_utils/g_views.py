def generateView(paths):
  with open(f"generated/views.py","w") as file:
    # --- Write Header ---
    file.write(generateViewsHeader())
    for path, data in paths.items():
      # --- Write Class Header ---
      name = convertCapitalName(path)
      file.write(generateViewsClassHeader(name, data.get('summary')))

      # --- Write Class Methods ---
      for method, entities in data.items():
        if method in ['get','post','put','patch','delete']:
          desc = entities.get('description')
          props = entities.get('responses').get('200').get('content').get('application/json').get('schema').get('properties')
          print(props)
          print("=========+=========+=========+=========+=========+")
          file.write(generateViewsMethodHeader(method, desc, ("With" in name)))
          file.write(generateViewsMethodBody())
          # --- Write Responses Properties ---
          for property, item in props.items():
            file.write(generateViewsResponseProps(property, item))
          file.write(generateViewsMethodException())

# =========+=========+=========+=========+=========+
# UTILITY
# =========+=========+=========+=========+=========+
def generateViewsHeader():
  return f"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# =========+=========+=========+=========+=========+
# Views
# =========+=========+=========+=========+=========+
"""

def generateViewsClassHeader(name, summary):
  return f"""
class {name}View(APIView):
  # SUMMARY: {summary} ---
  # =========+=========+=========+=========+=========+
"""
def generateViewsMethodHeader(method, description, flg):
  return f"""  def {method}(self, {"request, pk" if flg else "request"}):
    # DESC: {description} ---
"""
def generateViewsMethodBody():
  return f"""    try:
      # === add your business logic ===

      res = {{
"""
def generateViewsResponseProps(property, item):
  return f"""       \"{property}\": {getExampleData(item.get('type'))},
"""
def generateViewsMethodException():
  return f"""      }}
      return Response(res, status=status.HTTP_200_OK)

    except Exception as err:
      return Response({{"error": str(err)}})

  # =========+=========+=========+=========+=========+
"""

def getExampleData(item:str):
  match item:
    case "string"  : return ""
    case "integer" : return 0
    case "number"  : return 0
    case "boolean" : return False
    case "array"   : return []
    case "object"  : return {}
    case _: return None

def convertCapitalName(path:str):
  retList = []
  parts = path.split("/")
  for part in parts:
    if not part:
      continue
    if part.startswith("{") and part.endswith("}"):
      part = f"With{part.strip("{}").capitalize()}"
    else:
      part = part.capitalize()
    retList.append(part)
  return "".join(retList)