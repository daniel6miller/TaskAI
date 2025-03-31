
document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_tasks')
        .then(response => {
            if (!response.ok) {
                throw new Error('Database connection error for tasks');
            }
            return response.json();
        })
        .then(data => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = '';  // Clear any existing content

            if (data.tasks.length > 0) {
                data.tasks.forEach(task => {
                    const li = document.createElement('li');
                    li.classList.add("task-item"); // For styling

                    // Task Name
                    const taskName = document.createElement('span');
                    taskName.textContent = task.name || 'Unnamed Task';

                    // Run Task Button
                    const runButton = document.createElement('button');
                    runButton.textContent = 'Run Task';
                    runButton.classList.add('run-task-btn');
                    runButton.onclick = () => runTask(task._id);

                    // More Options (Ellipsis)
                    const moreOptions = document.createElement('div');
                    moreOptions.classList.add('dropdown');

                    const ellipsis = document.createElement('span');
                    ellipsis.innerHTML = '⋮'; // Three dots
                    ellipsis.classList.add('ellipsis-btn');
                    ellipsis.onclick = () => toggleDropdown(task._id);

                    // Dropdown Menu
                    const dropdownMenu = document.createElement('ul');
                    dropdownMenu.classList.add('dropdown-menu');
                    dropdownMenu.id = `dropdown-${task._id}`;

                    const viewEdit = document.createElement('li');
                    viewEdit.textContent = 'View/Edit';
                    viewEdit.onclick = () => viewEditTask(task._id);

                    const rename = document.createElement('li');
                    rename.textContent = 'Rename';
                    rename.onclick = () => renameTask(task._id);

                    const deleteTask = document.createElement('li');
                    deleteTask.textContent = 'Delete';
                    deleteTask.classList.add('delete-task');
                    deleteTask.onclick = () => deleteTaskFunction(task._id);

                    // Append items to dropdown menu
                    dropdownMenu.appendChild(viewEdit);
                    dropdownMenu.appendChild(rename);
                    dropdownMenu.appendChild(deleteTask);

                    moreOptions.appendChild(ellipsis);
                    moreOptions.appendChild(dropdownMenu);

                    // Append everything to task item
                    li.appendChild(taskName);
                    li.appendChild(runButton);
                    li.appendChild(moreOptions);
                    taskList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = 'No tasks available';
                taskList.appendChild(li);
            }
        })
        .catch(error => {
            console.error(error);
        });
});

// Function to toggle dropdown
function toggleDropdown(taskId) {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        if (menu.id !== `dropdown-${taskId}`) menu.style.display = "none";
    });
    const dropdown = document.getElementById(`dropdown-${taskId}`);
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

// Function placeholders (implement these as needed)
function runTask(taskId) {
    console.log(`Running task with ID: ${taskId}`);
}

function viewEditTask(taskId) {
    console.log(`Viewing/Editing task with ID: ${taskId}`);
}

function renameTask(taskId) {
    console.log(`Renaming task with ID: ${taskId}`);
}

function deleteTaskFunction(taskId) {
    console.log(`Deleting task with ID: ${taskId}`);
}

// Submit task recording form
const taskForm = document.getElementById('taskForm');
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
taskForm.addEventListener('submit', (event) => {
    event.preventDefault();
    
    const taskName = document.getElementById('taskName').value;
    const action = 'start'; // Default action is 'start'

    // Create the payload with the task name and action
    const payload = {
        task_name: taskName,
        action: action,
    };
    console.log(payload);  // Ensure the payload has task_name and action set correctly
    console.log("Hello World"); 

    // Make a fetch request to the Flask server
    fetch('/record_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Send the content as JSON
        },
        body: JSON.stringify(payload),  // Convert the payload to JSON
    })
    .then(response => {
        if (response.ok) {
            return response.json().then(data => {
                console.log(data);  // This logs the parsed JSON response
                return data;  // You can return the data here for further use if needed
            });
        } else {
            throw new Error('Recording Issue');
        }
    })
    .then(data => {
        alert(data.message);  // Show success message
        // Toggle button visibility based on action
        if (action === 'start') {
            recordButton.style.display = 'none';
            stopButton.style.display = 'inline';
        } else {
            recordButton.style.display = 'inline';
            stopButton.style.display = 'none';
        }
    })
    .catch(error => {
        console.error(error);
        alert('Failed to record task.',error);  // Handle errors
    });
});

// Handle stop recording when "Stop Recording" button is clicked
stopButton.addEventListener('click', (event) => {
    const taskName = document.getElementById('taskName').value;
    const action = 'stop'; // Action for stop

    // Create the payload with the task name and action
    const payload = {
        task_name: taskName,
        action: action,
    };

    // Make a fetch request to the Flask server
    fetch('/record_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),  // Convert the payload to JSON
    })
    .then(response => {
        if (response.ok) {
            return response.json().then(data => {
                console.log(data);  // This logs the parsed JSON response
                return data;  // You can return the data here for further use if needed
            });
        } else {
            return response.json().then(errData => {
                throw new Error(errData.error || 'Recording Issue');
            });
        }
    })
    .then(data => {
        alert(data.message);  // Show success message
        // Toggle button visibility based on action
        recordButton.style.display = 'inline';
        stopButton.style.display = 'none';
    })
    .catch(error => {
        console.error(error);
        alert('Failed to stop recording.', error);  // Handle errors
    });
});