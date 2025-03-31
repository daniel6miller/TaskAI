# routes.py
import subprocess
import os
from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, g, request_finished
from .recordTasks import start_recording, stop_recording
import logging
import threading
from .recordTasks import start_recording, stop_recording
from .globals import actions, mouse_listener, keyboard_listener, is_dragging
from bson import ObjectId

routes = Blueprint('routes', __name__)

@routes.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Route is working!"})


@routes.route('/get_tasks', methods=['GET'])
def get_tasks():
    db = current_app.config["MONGO_DB"]  # Get the MongoDB database

    # Assuming the 'tasks' collection exists in your database
    tasks_collection = db['Tasks']
    
    # Convert ObjectId to string for JSON serialization
    tasks = list(tasks_collection.find({}, {"_id": 1, "name": 1}))
    for task in tasks:
        task["_id"] = str(task["_id"])  # Convert ObjectId to string
    
    print("Tasks: ", tasks)  # Debugging
    
    return jsonify({'tasks': tasks})


@routes.route('/')
def index():
    db = current_app.config["MONGO_DB"]  # Get the MongoDB database

    # Assuming the 'tasks' collection exists in your database
    tasks_collection = db['tasks']
    tasks = list(tasks_collection.find())  # Find all tasks
    if tasks is None:
        return "Database connection error 3", 500
    
    task_list = [task.get('name') for task in tasks]  # Handle missing fields safely
    return render_template('index.html', tasks=task_list)

logging.basicConfig(level=logging.DEBUG)  # Enable logging

# Flask route
@routes.route('/record_task', methods=['POST'])
def record_task():
    global mouse_listener, keyboard_listener
    data = request.get_json()
    task_name = data.get('task_name')
    action = data.get('action')

    if not task_name:
        return jsonify({"error": "Task name is required"}), 400
    if not action:
        return jsonify({"error": "Action is required"}), 400

    if action == 'start':
        print(f"Before Start mouse_listener: {mouse_listener}, keyboard_listener: {keyboard_listener}")
        if mouse_listener is None and keyboard_listener is None:
            thread = threading.Thread(target=start_recording, daemon=True)
            thread.start()
        print(f"START mouse_listener: {mouse_listener}, keyboard_listener: {keyboard_listener}")
        return jsonify({'message': f'Task "{task_name}" recording started'}), 200
    
    elif action == 'stop':
        print(f"STOP mouse_listener: {mouse_listener}, keyboard_listener: {keyboard_listener}")
        if mouse_listener and keyboard_listener:
            stop_recording(task_name)  # Pass task_name

            # db = current_app.config["MONGO_DB"]
            # tasks_collection = db['tasks']
            # tasks = list(tasks_collection.find())

            # if not tasks:
            #     return jsonify({"error": "No tasks found."}), 400

            # task_list = [task.get('name', 'No Name') for task in tasks]   
            return jsonify({'message': f'Task "{task_name}" recording stopped'}), 200
        else:
            print("Recording was not started: Listeners not initialized")
            return jsonify({"error": "Recording was not started."}), 400
    else:
        return jsonify({"error": "Invalid action."}), 400


@routes.route('/run_task', methods=['POST'])
def run_task():
    task_name = request.form.get('task_name', 'Unnamed Task')
    # Logic to process/run the task
    return redirect(url_for('routes.index'))



