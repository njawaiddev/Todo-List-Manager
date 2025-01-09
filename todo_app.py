import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tkinter import StringVar

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x500")
        
        # Configure dark theme
        self.root.configure(bg='#2b2b2b')
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure styles
        self.style.configure("Custom.TFrame", background="#2b2b2b")
        self.style.configure("Custom.TButton", 
                           padding=5, 
                           background="#404040",
                           foreground="white")
        self.style.configure("Task.TCheckbutton", 
                           padding=5,
                           background="#2b2b2b",
                           foreground="white")
        self.style.configure("TEntry", 
                           fieldbackground="#404040",
                           foreground="white",
                           insertcolor="white")
        self.style.configure("TSpinbox", 
                           fieldbackground="#404040",
                           foreground="white",
                           insertcolor="white")
        
        # Initialize tasks
        self.tasks = []
        self.load_tasks()
        
        # Create main container
        self.main_frame = ttk.Frame(root, style="Custom.TFrame", padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create input frame
        self.input_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Task entry
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(
            self.input_frame, 
            textvariable=self.task_var,
            font=("Helvetica", 12),
            width=40,
            style="TEntry"
        )
        self.task_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Date and Time Frame
        self.datetime_frame = ttk.Frame(self.input_frame, style="Custom.TFrame")
        self.datetime_frame.pack(side=tk.LEFT, padx=(0, 5))
        
        # Due Date picker
        self.due_date = DateEntry(
            self.datetime_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            showweeknumbers=False,
            firstweekday='sunday',
            selectbackground='darkblue',
            selectforeground='white',
            normalbackground='#404040',
            normalforeground='white',
            headersbackground='#404040',
            headersforeground='white',
            disabledbackground='#2b2b2b',
            disabledforeground='gray'
        )
        self.due_date.pack(side=tk.LEFT, padx=(0, 5))
        
        # Time picker frame
        self.time_frame = ttk.Frame(self.datetime_frame, style="Custom.TFrame")
        self.time_frame.pack(side=tk.LEFT)
        
        # Hour picker
        self.hour_var = StringVar(value="00")
        self.hour_spinbox = ttk.Spinbox(
            self.time_frame,
            from_=0,
            to=23,
            width=2,
            format="%02.0f",
            textvariable=self.hour_var,
            wrap=True,
            style="TSpinbox"
        )
        self.hour_spinbox.pack(side=tk.LEFT)
        
        ttk.Label(self.time_frame, text=":", foreground="white", background="#2b2b2b").pack(side=tk.LEFT)
        
        # Minute picker
        self.minute_var = StringVar(value="00")
        self.minute_spinbox = ttk.Spinbox(
            self.time_frame,
            from_=0,
            to=59,
            width=2,
            format="%02.0f",
            textvariable=self.minute_var,
            wrap=True,
            style="TSpinbox"
        )
        self.minute_spinbox.pack(side=tk.LEFT)
        
        # Add button
        self.add_button = ttk.Button(
            self.input_frame,
            text="Add Task",
            command=self.add_task,
            style="Custom.TButton"
        )
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        # Create tasks frame with scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg="#2b2b2b", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Custom.TFrame")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons frame
        self.action_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Delete completed button
        self.delete_button = ttk.Button(
            self.action_frame,
            text="Delete Completed",
            command=self.delete_completed,
            style="Custom.TButton"
        )
        self.delete_button.pack(side=tk.RIGHT)
        
        # Sort button
        self.sort_button = ttk.Button(
            self.action_frame,
            text="Sort by Due Date",
            command=self.sort_by_due_date,
            style="Custom.TButton"
        )
        self.sort_button.pack(side=tk.RIGHT, padx=5)
        
        # Bind enter key to add task
        self.root.bind('<Return>', lambda e: self.add_task())
        
        # Load existing tasks
        self.refresh_tasks()
        
        # Alert settings
        self.last_alert_check = datetime.now()
        self.alert_interval = 60000  # Check every minute (in milliseconds)
        
        # Start alert checker
        self.check_due_tasks()

    def get_due_datetime(self):
        """Get the combined date and time for the due date."""
        date_str = self.due_date.get_date().strftime("%Y-%m-%d")
        time_str = f"{self.hour_var.get()}:{self.minute_var.get()}"
        return f"{date_str} {time_str}"

    def migrate_task(self, task):
        """Migrate old task format to new format."""
        if 'created_date' not in task:
            # If it's an old task, use the 'date' field as created_date
            task['created_date'] = task.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if 'due_date' not in task:
            # Set due date to created date if not present
            task['due_date'] = task['created_date']
        if 'completion_date' not in task:
            task['completion_date'] = task['created_date'] if task.get('completed', False) else None
        # Remove old date field if it exists
        task.pop('date', None)
        return task

    def load_tasks(self):
        try:
            if os.path.exists('tasks.json'):
                with open('tasks.json', 'r') as f:
                    loaded_tasks = json.load(f)
                    # Migrate each task to new format
                    self.tasks = [self.migrate_task(task) for task in loaded_tasks]
                    # Save migrated tasks
                    self.save_tasks()
            else:
                self.tasks = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.tasks = []

    def save_tasks(self):
        try:
            with open('tasks.json', 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

    def add_task(self):
        task_text = self.task_var.get().strip()
        if task_text:
            new_task = {
                'text': task_text,
                'completed': False,
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'due_date': self.get_due_datetime(),
                'completion_date': None
            }
            self.tasks.append(new_task)
            self.task_var.set("")  # Clear input
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def toggle_task(self, index):
        self.tasks[index]['completed'] = not self.tasks[index]['completed']
        if self.tasks[index]['completed']:
            self.tasks[index]['completion_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.tasks[index]['completion_date'] = None
        self.save_tasks()
        self.refresh_tasks()

    def delete_completed(self):
        self.tasks = [task for task in self.tasks if not task['completed']]
        self.save_tasks()
        self.refresh_tasks()

    def sort_by_due_date(self):
        self.tasks.sort(key=lambda x: x['due_date'])
        self.refresh_tasks()

    def refresh_tasks(self):
        # Clear all widgets in scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get current time for comparison
        current_time = datetime.now()

        # Recreate task widgets
        for i, task in enumerate(self.tasks):
            task_frame = ttk.Frame(self.scrollable_frame)
            task_frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar(value=task['completed'])
            
            # Create task text with dates and status
            task_text = f"{task['text']}"
            date_text = f"\nCreated: {task['created_date']} | Due: {task['due_date']}"
            
            # Add status indicators
            if not task['completed']:
                try:
                    due_time = datetime.strptime(task['due_date'], "%Y-%m-%d %H:%M")
                    time_diff = due_time - current_time
                    
                    if time_diff.total_seconds() < 0:
                        date_text += " [OVERDUE]"
                    elif time_diff.total_seconds() <= 300:  # 5 minutes or less
                        date_text += " [DUE SOON]"
                except (ValueError, TypeError):
                    pass
            
            if task['completion_date']:
                date_text += f" | Completed: {task['completion_date']}"
            
            cb = ttk.Checkbutton(
                task_frame,
                text=task_text + date_text,
                variable=var,
                command=lambda i=i: self.toggle_task(i),
                style="Task.TCheckbutton"
            )
            cb.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            if task['completed']:
                cb.state(['selected'])

    def check_due_tasks(self):
        """Check for tasks that are due and show alerts."""
        current_time = datetime.now()
        
        for task in self.tasks:
            if not task['completed']:
                try:
                    due_time = datetime.strptime(task['due_date'], "%Y-%m-%d %H:%M")
                    time_diff = due_time - current_time
                    
                    # Alert conditions
                    if time_diff.total_seconds() > 0:  # Future task
                        minutes_remaining = time_diff.total_seconds() / 60
                        
                        # Alert 5 minutes before
                        if 4.9 <= minutes_remaining <= 5.1:
                            messagebox.showwarning(
                                "Task Due Soon",
                                f"Task '{task['text']}' is due in 5 minutes!"
                            )
                        # Alert 1 minute before
                        elif 0.9 <= minutes_remaining <= 1.1:
                            messagebox.showwarning(
                                "Task Due Very Soon",
                                f"Task '{task['text']}' is due in 1 minute!"
                            )
                    # Alert when task is exactly due
                    elif -0.1 <= time_diff.total_seconds() <= 0.1:
                        messagebox.showwarning(
                            "Task Due Now",
                            f"Task '{task['text']}' is due now!"
                        )
                    # Alert for overdue tasks (only once)
                    elif -300 <= time_diff.total_seconds() <= -240:  # 5 minutes overdue
                        messagebox.showwarning(
                            "Task Overdue",
                            f"Task '{task['text']}' is overdue!"
                        )
                except (ValueError, TypeError):
                    continue  # Skip if date format is invalid
        
        # Schedule next check
        self.root.after(self.alert_interval, self.check_due_tasks)

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 