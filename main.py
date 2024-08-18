import os

# Task list to store tasks
tasks = []

def add_task():
    task = input("Enter the task: ")
    tasks.append(task)
    print(f"'{task}' has been added to your to-do list.\n")

def delete_task():
    view_tasks()
    if tasks:
        try:
            task_number = int(input("Enter the task number to delete: ")) - 1
            if 0 <= task_number < len(tasks):
                removed_task = tasks.pop(task_number)
                print(f"'{removed_task}' has been removed from your to-do list.\n")
            else:
                print("Invalid task number.\n")
        except ValueError:
            print("Please enter a valid number.\n")
    else:
        print("No tasks to delete.\n")

def view_tasks():
    if tasks:
        print("Your To-Do List:")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task}")
        print()
    else:
        print("Your to-do list is empty.\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        print("To-Do List Application")
        print("1. Add a task")
        print("2. Delete a task")
        print("3. View all tasks")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            clear_screen()
            add_task()
        elif choice == '2':
            clear_screen()
            delete_task()
        elif choice == '3':
            clear_screen()
            view_tasks()
        elif choice == '4':
            clear_screen()
            print("Exiting the application. Goodbye!")
            break
        else:
            clear_screen()
            print("Invalid choice. Please enter a number between 1 and 4.\n")

if __name__ == "__main__":
    clear_screen()
    main_menu()
