import os
import ipywidgets as widgets
from IPython.display import display, clear_output

TASK_FILE = "tasks.txt"

# Load tasks from file
def load_tasks():
    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            for line in f:
                task, status = line.strip().split("|")
                tasks.append({"task": task, "status": status})
    return tasks

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        for t in tasks:
            f.write(f"{t['task']}|{t['status']}\n")

# Initialize tasks
tasks = load_tasks()

# Widgets
task_input = widgets.Text(
    placeholder="Enter a new task...",
    description="Task:",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width="400px")
)

add_button = widgets.Button(description="Add Task", button_style="success")
remove_button = widgets.Button(description="Remove Task", button_style="danger")
complete_button = widgets.Button(description="Mark Complete", button_style="info")
task_dropdown = widgets.Dropdown(options=[], description="Select Task:")

output = widgets.Output()

# Update dropdown options
def update_dropdown():
    task_dropdown.options = [f"{i+1}. {t['task']} ({t['status']})" for i, t in enumerate(tasks)]

# Display tasks in colorful HTML
def show_tasks():
    with output:
        clear_output()
        html = "<h3 style='color:blue'>--- Your To-Do List ---</h3>"
        if not tasks:
            html += "<p style='color:red'>No tasks yet!</p>"
        else:
            for i, t in enumerate(tasks, 1):
                if t["status"] == "pending":
                    html += f"<p style='color:orange'>{i}. {t['task']} [Pending]</p>"
                else:
                    html += f"<p style='color:green'>{i}. {t['task']} [Completed]</p>"
        display(widgets.HTML(html))

# Button actions
def add_task_action(b):
    if task_input.value.strip():
        tasks.append({"task": task_input.value.strip(), "status": "pending"})
        save_tasks(tasks)
        task_input.value = ""
        update_dropdown()
        show_tasks()

def remove_task_action(b):
    if task_dropdown.value:
        idx = task_dropdown.options.index(task_dropdown.value)
        tasks.pop(idx)
        save_tasks(tasks)
        update_dropdown()
        show_tasks()

def complete_task_action(b):
    if task_dropdown.value:
        idx = task_dropdown.options.index(task_dropdown.value)
        tasks[idx]["status"] = "completed"
        save_tasks(tasks)
        update_dropdown()
        show_tasks()

# Bind actions
add_button.on_click(add_task_action)
remove_button.on_click(remove_task_action)
complete_button.on_click(complete_task_action)

# Layout
ui = widgets.VBox([
    task_input,
    widgets.HBox([add_button, remove_button, complete_button]),
    task_dropdown,
    output
])

update_dropdown()
show_tasks()
display(ui)
