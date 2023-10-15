import json
import os.path

from config import BASE_DIR


def load_schema(file_name):
    path = os.path.join(
        BASE_DIR,
        'regres_in_demo_project',
        'json_schemas',
        file_name
    )
    with open(path) as file:
        return json.loads(file.read())
