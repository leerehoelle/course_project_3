import json

def load_transactions():
    with open ('/Users/mariiasaliutina/course_project_3/operations.json') as file:
        return json.load(file)


