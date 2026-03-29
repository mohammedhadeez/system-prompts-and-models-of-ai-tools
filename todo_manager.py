import json
import os
import argparse

DEFAULT_TODO_FILE = "todo_list.json"

def load_todos(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"tasks": [], "current_task": None}
    return {"tasks": [], "current_task": None}

def save_todos(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def set_tasks(filename, tasks):
    if not tasks:
        print("Error: No tasks provided.")
        return

    data = {
        "tasks": [{"name": t, "status": "todo"} for t in tasks],
        "current_task": tasks[0] if tasks else None
    }
    if data["tasks"]:
        data["tasks"][0]["status"] = "in-progress"

    save_todos(filename, data)
    print(f"Tasks set: {tasks}")
    print(f"Current task: {data['current_task']}")

def add_task(filename, task):
    data = load_todos(filename)
    data["tasks"].append({"name": task, "status": "todo"})
    if not data["current_task"]:
        data["current_task"] = task
        data["tasks"][-1]["status"] = "in-progress"
    save_todos(filename, data)
    print(f"Added task: {task}")

def move_to_task(filename, task_name):
    data = load_todos(filename)

    # Verify task exists
    task_exists = False
    for t in data["tasks"]:
        if t["name"] == task_name:
            task_exists = True
            break

    if not task_exists:
        print(f"Error: Task '{task_name}' not found.")
        return

    # Mark prior tasks as done
    found = False
    for t in data["tasks"]:
        if t["name"] == task_name:
            t["status"] = "in-progress"
            data["current_task"] = task_name
            found = True
        elif not found:
            t["status"] = "done"
        else:
            t["status"] = "todo"

    save_todos(filename, data)
    print(f"Moved to task: {task_name}")

def mark_all_done(filename):
    data = load_todos(filename)
    for t in data["tasks"]:
        t["status"] = "done"
    data["current_task"] = None
    save_todos(filename, data)
    print("All tasks marked as done.")

def read_list(filename):
    data = load_todos(filename)
    if not data["tasks"]:
        print("No tasks found.")
        return

    print("Todo List:")
    for t in data["tasks"]:
        status_symbol = "[ ]"
        if t["status"] == "done":
            status_symbol = "[x]"
        elif t["status"] == "in-progress":
            status_symbol = "[>]"
        print(f"{status_symbol} {t['name']}")

def main():
    parser = argparse.ArgumentParser(description="Todo Manager Tool")
    parser.add_argument("action", choices=["set_tasks", "add_task", "move_to_task", "mark_all_done", "read_list"], help="Action to perform")
    parser.add_argument("--tasks", nargs="+", help="List of tasks for set_tasks")
    parser.add_argument("--task", help="Task for add_task")
    parser.add_argument("--moveToTask", help="Task name for move_to_task")
    parser.add_argument("--file", default=DEFAULT_TODO_FILE, help="Path to todo list file")

    args = parser.parse_args()

    if args.action == "set_tasks":
        if args.tasks:
            set_tasks(args.file, args.tasks)
        else:
            print("Error: --tasks required for set_tasks")
    elif args.action == "add_task":
        if args.task:
            add_task(args.file, args.task)
        else:
            print("Error: --task required for add_task")
    elif args.action == "move_to_task":
        if args.moveToTask:
            move_to_task(args.file, args.moveToTask)
        else:
            print("Error: --moveToTask required for move_to_task")
    elif args.action == "mark_all_done":
        mark_all_done(args.file)
    elif args.action == "read_list":
        read_list(args.file)

if __name__ == "__main__":
    main()
