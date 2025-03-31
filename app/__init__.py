from flask import Flask, current_app
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables



logging.getLogger("pymongo").setLevel(logging.WARNING)

def create_app():
    app = Flask(__name__)

    # Connect once and store in `app.config`
    app.config["MONGO_CLIENT"] = MongoClient(os.getenv("MONGO_URI"))
    app.config["MONGO_DB"] = app.config["MONGO_CLIENT"][os.getenv("MONGO_DB")]

    # Ensure we use an app context when accessing Flask-specific features
    with app.app_context():
        try:
            db = current_app.config["MONGO_DB"]  # Get the MongoDB database
            print("Successfully connected to MongoDB")
            count = db["Tasks"].count_documents({})
            print(f"Number of documents in 'tasks': {count}")
            tasks = list(db["Tasks"].find({}))
            print(tasks)
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            db = None  # Set db to None if connection fails  

    from app.routes import routes  # Import here to avoid circular import
    app.register_blueprint(routes)  # Register Blueprint

    return app

