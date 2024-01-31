from flask import Flask, jsonify, request
from flask.helpers import make_response
from flask.views import MethodView

app = Flask(__name__)

tasks = []

class Task:
    def __init__(self, id, title, is_completed=False):
        self.id = id
        self.title = title
        self.is_completed = is_completed

class TaskAPI(MethodView):
    def post(self):
        data = request.get_json()
        if 'title' in data:
            new_task = Task(id=len(tasks) + 1, title=data['title'])
            tasks.append(new_task)
            return jsonify({"id": new_task.id}), 201
        else:
            return jsonify({"error": "Title is required"}), 400

    def get(self, task_id=None):
        if task_id is None:
            return jsonify({"tasks": [task.__dict__ for task in tasks]}), 200
        else:
            task = next((task for task in tasks if task.id == task_id), None)
            if task:
                return jsonify(task.__dict__), 200
            else:
                return jsonify({"error": "There is no task at that id"}), 404

    def delete(self, task_id):
        global tasks
        tasks = [task for task in tasks if task.id != task_id]
        return '', 204

    def put(self, task_id):
        data = request.get_json()
        task = next((task for task in tasks if task.id == task_id), None)
        if task:
            if 'title' in data:
                task.title = data['title']
            if 'is_completed' in data:
                task.is_completed = data['is_completed']
            return '', 204
        else:
            return jsonify({"error": "There is no task at that id"}), 404

app.add_url_rule('/v1/tasks', view_func=TaskAPI.as_view('tasks'))
app.add_url_rule('/v1/tasks/<int:task_id>', view_func=TaskAPI.as_view('task'))

if __name__ == '__main__':
    app.run(debug=True)
