from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://saivinoth94:SOpXoLi4R8wIh6hO@cluster0.qwcfcro.mongodb.net/todo?retryWrites=true&w=majority"
CORS(app, resources={r"/api/*": {"origins": "https://todos-name.netlify.app/"}})

mongo = PyMongo(app)
todo_collection = mongo.db.todos

# Create a new task
@app.route('/api/todos', methods=['POST'])
def create_todo():
    name = request.json['name']
    description = request.json.get('description', '')
    completed = request.json.get('completed', False)

    new_todo = {
        'name': name,
        'description': description,
        'completed': completed
    }

    todo_id = todo_collection.insert_one(new_todo).inserted_id
    created_todo = todo_collection.find_one({'_id': todo_id})
    created_todo['_id'] = str(created_todo['_id'])  # Convert ObjectId to string
    return jsonify(created_todo), 201

# Get all tasks
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = list(todo_collection.find())
    for todo in todos:
        todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
    return jsonify(todos)

# Update a task
@app.route('/api/todos/<string:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    name = request.json.get('name')
    description = request.json.get('description')
    completed = request.json.get('completed')

    update_data = {}
    if name:
        update_data['name'] = name
    if description:
        update_data['description'] = description
    if completed is not None:
        update_data['completed'] = completed

    todo_collection.update_one({'_id': ObjectId(todo_id)}, {'$set': update_data})
    updated_todo = todo_collection.find_one({'_id': ObjectId(todo_id)})
    updated_todo['_id'] = str(updated_todo['_id'])  # Convert ObjectId to string
    return jsonify(updated_todo)

## Delete a task
@app.route('/api/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        result = todo_collection.delete_one({'_id': ObjectId(todo_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
