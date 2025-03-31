# Task AI

Task AI is a Python-based automation application designed to track and execute user tasks efficiently. By leveraging `pynput`, MongoDB, and a task execution engine, Task AI automates repetitive computer tasks, reducing manual workload and improving efficiency.

## Features

- **Automated Task Tracking:** Uses `pynput` to monitor user activity and store tasks in a MongoDB database.
- **Task Execution Engine:** Searches the database and performs tasks automatically based on user input.
- **Flask-based API:** Provides a structured way to interact with tasks and automation workflows.
- **Large Language Model Integration:** Enhances automation efficiency and user interaction.
- **Secure Authentication:** Implements JWT authentication for secure task execution.

## Installation

### Prerequisites
- Python 3.x
- MongoDB
- Flask
- Required dependencies (install via `requirements.txt`)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/daniel6miller/TaskAI.git
   cd TaskAI
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask server:
   ```bash
   python app.py
   ```

## Current Development

- **Gathering large amounts of task data** to improve automation models.
- **Enhancing LLM capabilities** for more autonomous task execution.
- **Expanding adaptability** to handle varying conditions and environments.

## License
This project is licensed under the MIT License.
