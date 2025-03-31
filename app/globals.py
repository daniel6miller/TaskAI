# globals.py
import threading

actions = []
mouse_listener = None
keyboard_listener = None
is_dragging = False
lock = threading.Lock()  # Add a lock
is_recording = threading.Event()  # Event to signal when recording has started