import yaml

from g_utils.g_model import generateModel
from g_utils.g_serializer import generateSerializer
from g_utils.g_views import generateView

def getSwaggerData():
  with open("swagger.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)
    return data['info'], data['paths'], data['components']

def generateViewss(paths):
  for api_path, data in paths.items():
    print(api_path)
    for method, data in data.items():
      print(data.get('summary',{}))
      print(data.get('description',{}))
      print(data.get('requestBody',{}))
      print(data.get('responses',{}))
      print(data.get('parameters'))
      print("=========+=========+=========+=========+=========+")

if __name__ == "__main__":
  info, paths, components = getSwaggerData()
  generateModel(components)
  generateSerializer(components)
  generateView(paths)