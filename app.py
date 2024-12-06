from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados (base de datos en memoria)
tasks = [
    {"id": 1, "title": "Tarea 1", "description": "Primera tarea", "done": False},
    {"id": 2, "title": "Tarea 2", "description": "Segunda tarea", "done": True}
]

# Ruta para obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Ruta para obtener una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

# Ruta para agregar una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Ruta para actualizar una tarea
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    task.update({
        "title": data.get("title", task["title"]),
        "description": data.get("description", task["description"]),
        "done": data.get("done", task["done"])
    })
    return jsonify(task)

# Ruta para eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
