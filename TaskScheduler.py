import tkinter as tk
from tkinter import messagebox
import json
import os

def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

def add_task():
    task_name = entry_task.get()
    if task_name:
        tasks.append({"task": task_name, "completed": False})
        list_tasks()
        entry_task.delete(0, tk.END)
        save_tasks(tasks)
    else:
        messagebox.showwarning("Input Error", "Please enter a task name.")

def complete_task():
    selected_task = listbox_tasks.curselection()
    if selected_task:
        task_index = selected_task[0]
        tasks[task_index]["completed"] = True
        list_tasks()
        save_tasks(tasks)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

def delete_task():
    selected_task = listbox_tasks.curselection()
    if selected_task:
        task_index = selected_task[0]
        del tasks[task_index]
        list_tasks()
        save_tasks(tasks)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

def list_tasks():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        listbox_tasks.insert(tk.END, f"{task['task']} - {status}")

window = tk.Tk()
window.title("Simple Task Scheduler")

tasks = load_tasks()

entry_task = tk.Entry(window, width=40)
entry_task.pack(pady=10)

btn_add = tk.Button(window, text="Add Task", command=add_task)
btn_add.pack(pady=5)

btn_complete = tk.Button(window, text="Mark as Completed", command=complete_task)
btn_complete.pack(pady=5)

btn_delete = tk.Button(window, text="Delete Task", command=delete_task)
btn_delete.pack(pady=5)

listbox_tasks = tk.Listbox(window, width=50, height=10)
listbox_tasks.pack(pady=10)

list_tasks()

window.mainloop()
