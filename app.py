## Creating a simple Task List App

from flask import Flask
from flask_restful import Api

from task import Task, TaskList

app = Flask(__name__)
api = Api(app)

api.add_resource(Task, '/task/<string:desc>')
api.add_resource(TaskList, '/tasks')

print(__name__)

if __name__ == "__main__":
    app.run(port=4990, debug=True)

