# performTask.py -
from flask import Flask, request, jsonify
import time
import os
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MController
from pynput.mouse import Button
import threading
from datetime import datetime
from PIL import ImageGrab
from functools import partial
from config import secret
from .globals import actions, mouse_listener, keyboard_listener, is_dragging

app = Flask(__name__)

# Assuming create_app() is called to initialize the app and connect to MongoDB
from app import create_app
app = create_app()  # Initialize app and establish DB connection

@app.route('/perform_task', methods=['POST'])
def perform_task():
    task_name = request.form['task_name']
    task = taskData.find_one({'task_name': task_name})
    actions = task['actions']
    
    for action in actions:
        time.sleep((action[1] - actions[0][1]).total_seconds())
        # Perform the action based on the recorded task (similar to your original script)
        # Perform the actions (mouse, keyboard, etc.)
    
    return jsonify({'message': f'Task "{task_name}" performed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
