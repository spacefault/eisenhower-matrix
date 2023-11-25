import json
import os


class taskmatrix:
    TASK_PATH = os.path.expanduser("~/.config/eisenhower-matrix")
    TASK_LOCATION = os.path.join(TASK_PATH, "tasks.json")

    def __init__(self):
        self.tasks = {'Urgent & Important': [], 'Not Urgent & Important': [],
                      'Urgent & Not Important': [], 'Not Urgent & Not Important': []}
        self.load_tasks()

    def add_task(self, task, quadrant):
        self.tasks[quadrant].append(task)

    def delete_task(self, task, quadrant):
        if task in self.tasks[quadrant]:
            self.tasks[quadrant].remove(task)
            return True
        return False

    def show_matrix(self):
        os.system("clear")
        print("\nEisenhower Matrix:")
        print("An Eisenhower matrix is a good way to quickly organize and manage a lot of tasks at once.")
        print("")
        print("\033[1mUrgent & Important tasks\033[0m" " should be prioritized, and done as soon as possible")
        print("\033[1mNot Urgent & Important tasks\033[0m" " should be scheduled for later")
        print("\033[1mUrgent but Not Important tasks\033[0m" " should be delegated, find someone to assist you.")
        print("\033[1mNot urgent and are Not important tasks\033[0m" " should be deleted, they are distractions.")
        print("")
        print("Your tasks are saved on exit, please do NOT Control+C or else data loss might occur!")
        print("")
        for quadrant, task_list in self.tasks.items():
            print(f"{quadrant}:\n")
            for task in task_list:
                print(f"- {task}")
            print("\n")

    def save_tasks(self):
        if not os.path.exists(self.TASK_PATH):
            os.makedirs(self.TASK_PATH)

        with open(self.TASK_LOCATION, 'w') as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        if not os.path.exists(self.TASK_LOCATION):
            return

        try:
            with open(self.TASK_LOCATION, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            pass  # File doesn't exist yet

def get_quadrant_from_user():
    while True:
        print("Select Quadrant:")
        print("1. Urgent & Important")
        print("2. Not Urgent & Important")
        print("3. Urgent & Not Important")
        print("4. Not Urgent & Not Important")
        choice = input("Enter your choice (1-4): ")

        if choice in ['1', '2', '3', '4']:
            quadrants = ['Urgent & Important', 'Not Urgent & Important', 'Urgent & Not Important', 'Not Urgent & Not Important']
            return quadrants[int(choice) - 1]
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    matrix = taskmatrix()

    while True:
        matrix.show_matrix()

        task = input("Enter your task (or 'exit' to quit, 'delete' to delete a task): ")

        if task.lower() == 'exit':
            matrix.save_tasks()
            break
        elif task.lower() == 'delete':
            task_to_delete = input("Enter the task to delete: ")
            quadrant_to_delete = get_quadrant_from_user()
            if matrix.delete_task(task_to_delete, quadrant_to_delete):
                print(f"Task '{task_to_delete}' deleted from {quadrant_to_delete}.\n")
            else:
                print(f"Task '{task_to_delete}' not found in {quadrant_to_delete}.\n")
        else:
            quadrant = get_quadrant_from_user()
            matrix.add_task(task, quadrant)
            print(f"Task '{task}' added to {quadrant}.\n")


if __name__ == '__main__':
    main()

