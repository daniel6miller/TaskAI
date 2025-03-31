# recordTasks.py
from flask import Flask, request, jsonify, g, current_app
import threading
from datetime import datetime
from pynput import mouse, keyboard
from functools import partial
import time
from .globals import actions, mouse_listener, keyboard_listener, is_dragging, lock, is_recording

# Mouse event handlers
def on_click(x, y, button, pressed):
    global is_dragging
    if pressed:
        # Mouse button pressed; start of a click or a drag
        is_dragging = True
        timestamp = datetime.now()
        action = f"{button} pressed"
        actions.append([action, timestamp, x, y])
    else:
        # Mouse button released; end of a click or a drag
        is_dragging = False
        timestamp = datetime.now()
        action = f"{button} released"
        actions.append([action, timestamp, x, y])

def on_move(x, y):
    global is_dragging
    if is_dragging:
        # Mouse is moving while a button is pressed; this is a drag
        timestamp = datetime.now()
        action = "dragging"
        actions.append([action, timestamp, x, y])

# Keyboard event handler
def on_key_press(key):
    try:
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            # Number pad keys 0-9
            key_name = f'NumPad {key.vk - 96}'
        else:
            key_name = key.char or key.name
    except AttributeError:
        if hasattr(key,'name'):
            key_name = key.name  # Special keys
        else:
            key_name = key.char
    timestamp = datetime.now()
    actions.append([key_name, timestamp])

# Scroll event handler
def on_mouse_scroll(x, y, dx, dy):
    timestamp = datetime.now()
    actions.append(['Scroll', x, y, dx, dy, timestamp])

def start_recording():
    global mouse_listener, keyboard_listener, is_recording
    print(f"before Recording Started: mouse_listener: {mouse_listener}, keyboard_listener: {keyboard_listener}")

    # Locking to prevent race conditions
    with lock:
        if mouse_listener is None and keyboard_listener is None:  # Prevent multiple listeners
            # Initialize listeners only if they are not already initialized
            print("Initializing listeners...")
            mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_mouse_scroll)
            keyboard_listener = keyboard.Listener(on_press=on_key_press)

            # Start listeners in separate threads
            mouse_listener.start()
            keyboard_listener.start()

            # Signal that recording has started
            is_recording.set()  # This signals that recording has started

            print(f"Recording Started: mouse_listener: {mouse_listener}, keyboard_listener: {keyboard_listener}")

            # Check if the threads remain active
            time.sleep(1)  # Allow time for listeners to initialize
            print(f"After 1s: mouse_listener: {mouse_listener}, keyboard_listener: {keyboard_listener}")
        else:
            print("Listeners are already initialized or recording is already started.")

    return



def stop_recording(task_name):
    global mouse_listener, keyboard_listener, is_recording

    print("Stopping listeners...")

    with lock:
        if is_recording.is_set():  # Only proceed if recording has started
            if mouse_listener is not None:
                mouse_listener.stop()  
                mouse_listener = None  # Reset after stopping
            
            if keyboard_listener is not None:
                keyboard_listener.stop()  
                keyboard_listener = None  # Reset after stopping

            # Reset the recording flag
            is_recording.clear()

            print(f"Stopped recording for task: {task_name}")

            # Cleanup actions list
            i = 0
            while i < len(actions):
                if actions[i][0] is None:
                    actions.pop(i)
                elif 'NumPad' in actions[i][0]:
                    actions[i][0] = actions[i][0][-1]
                else:
                    i += 1

            # Store new task in MongoDB
            db = current_app.config["MONGO_DB"]
            tasks_collection = db['tasks']
            new_task = {'task_name': task_name, 'actions': actions}
            tasks_collection.insert_one(new_task)

            return jsonify({'message': f'Task "{task_name}" recorded successfully'}), 201

        else:
            print("Recording was not started: Listeners not initialized")
            return jsonify({"error": "Recording was not started."}), 400