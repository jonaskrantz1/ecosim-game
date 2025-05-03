import json
from pyodide.http import open_url

def load_json(path):
    response = open_url(path)
    return json.loads(response.read())
