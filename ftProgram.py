import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from connection import Connections 

class FitJourneyApp:
    def __init__(self):
        self.db_connection = Connections()

    # Setup window with background
    def setup_window_with_background(self, window, title, width, height, image_path):
        window.title(title)
        window.geometry(f"{width}x{height}+{(window.winfo_screenwidth() - width) // 2}+{(window.winfo_screenheight() - height) // 2}")
        self.window.resizable(False, False)  # Disable resizing
        background_image = Image.open(image_path)
        background_image = background_image.resize((width, height), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(background_image)

        canvas = tk.Canvas(window, width=width, height=height)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=bg_photo)

        window.bg_photo = bg_photo  # Prevent garbage collection
        return canvas

    # Main entry point
    def run(self):
        self.main_window()

    # Main Window
    def main_window(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)  # Disable resizing

        # Setup background
        canvas = self.setup_window_with_background(self.window, "FitJourney - Login", 400, 300, "images/background.jpg")

        # Welcome Text
        canvas.create_text(200, 50, text="Welcome to FitJourney!", font=("Arial", 20, "bold"), fill="black")

        # Login Buttons (User and Admin)
        login_user_button = ttk.Button(self.window, text="Login as User", command=self.login_user)
        login_admin_button = ttk.Button(self.window, text="Login as Admin", command=self.login_admin)

        # Register Button
        register_button = ttk.Button(self.window, text="Register", command=self.register_user)

        # Placing buttons on the canvas
        canvas.create_window(200, 120, window=login_user_button)
        canvas.create_window(200, 160, window=login_admin_button)
        canvas.create_window(200, 200, window=register_button)

        # Start the main loop to display the window
        self.window.mainloop()








    # Admin Login
    def login_admin(self):
        def verify_login():
            username = entry_username.get()
            password = entry_password.get()

            if not username or not password:
                messagebox.showerror("Error", "Both fields are required.")
                return

            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT admin_id FROM admin WHERE admin_username = %s AND admin_password = %s", (username, password))
                user = cursor.fetchone()
                conn.close()

                if user:
                    messagebox.showinfo("Success", "Login successful!")
                    login_window.destroy()
                    self.admin_dashboard(user[0])
                else:
                    messagebox.showerror("Error", "Invalid username or password.")

        login_window = tk.Toplevel()
        login_window.resizable(False, False)  # Disable resizing
        canvas = self.setup_window_with_background(login_window, "Admin Login", 400, 300, "images/background.jpg")

        # Title label for admin login
        canvas.create_text(200, 40, text="Admin Login", anchor="center", font=("Arial", 16, "bold"), fill="black")

        # Username label and input
        canvas.create_text(200, 100, text="Username:", anchor="center", font=("Arial", 12))
        entry_username = ttk.Entry(login_window)
        canvas.create_window(200, 130, window=entry_username, width=250)

        # Password label and input
        canvas.create_text(200, 170, text="Password:", anchor="center", font=("Arial", 12))
        entry_password = ttk.Entry(login_window, show="*")
        canvas.create_window(200, 200, window=entry_password, width=250)

        # Login button
        login_button = ttk.Button(login_window, text="Login", command=verify_login)
        canvas.create_window(200, 250, window=login_button, width=100)

        login_window.mainloop()



    # User Login
    def login_user(self):
        def verify_login():
            username = entry_username.get()
            password = entry_password.get()

            if not username or not password:
                messagebox.showerror("Error", "Both fields are required.")
                return

            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                conn.close()

                if user:
                    messagebox.showinfo("Success", "Login successful!")
                    login_window.destroy()
                    self.main_dashboard(user[0])
                else:
                    messagebox.showerror("Error", "Invalid username or password.")

        login_window = tk.Toplevel()
        login_window.resizable(False, False)  # Disable resizing
        canvas = self.setup_window_with_background(login_window, "Login", 400, 300, "images/background.jpg")

        # Login Form
        canvas.create_text(100, 100, text="Username:", anchor="e", font=("Arial", 12))
        entry_username = ttk.Entry(login_window)
        canvas.create_window(220, 100, window=entry_username, width=180)

        canvas.create_text(100, 140, text="Password:", anchor="e", font=("Arial", 12))
        entry_password = ttk.Entry(login_window, show="*")
        canvas.create_window(220, 140, window=entry_password, width=180)

        login_button = ttk.Button(login_window, text="Login", command=verify_login)
        canvas.create_window(200, 200, window=login_button)


    # User Registration
    def register_user(self):
        def save_user():
            username = entry_username.get()
            password = entry_password.get()
            self.window.resizable(False, False)  # Disable resizing
            if not username or not password:
                messagebox.showerror("Error", "Both fields are required.")
                return

            # Check if the username already exists in the database
            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
                user_count = cursor.fetchone()[0]
                
                if user_count > 0:
                    messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                    conn.close()
                    return  # Prevent further registration if the username exists
                
                # If username doesn't exist, proceed with registration
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registration successful!")
                register_window.destroy()

        register_window = tk.Toplevel()
        register_window.resizable(False, False)  # Disable resizing
        canvas = self.setup_window_with_background(register_window, "Register", 400, 300, "images/background.jpg")

        canvas.create_text(100, 100, text="Username:", anchor="e", font=("Arial", 12))
        entry_username = ttk.Entry(register_window)
        canvas.create_window(220, 100, window=entry_username, width=180)

        canvas.create_text(100, 140, text="Password:", anchor="e", font=("Arial", 12))
        entry_password = ttk.Entry(register_window, show="*")
        canvas.create_window(220, 140, window=entry_password, width=180)

        save_button = ttk.Button(register_window, text="Register", command=save_user)
        canvas.create_window(200, 200, window=save_button)


    def logout_and_redirect(self):
        """Logout the user and redirect to the main window."""
        if self.window is not None:  # Check if there's an active window
            self.window.destroy()  # Close the current window
        self.main_window()  # Open the main login/register window










    def admin_dashboard(self, user_id):
        self.window.destroy()  # Destroy the previous window
        self.window = tk.Tk()
        self.window.resizable(False, False)  # Disable resizing
        self.window.title("FitJourney Dashboard")

        # Window dimensions
        window_width = 500
        window_height = 400

        # Center the window
        position_x = (self.window.winfo_screenwidth() // 2) - (window_width // 2)
        position_y = (self.window.winfo_screenheight() // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Add a canvas to set the background image
        canvas = tk.Canvas(self.window, width=window_width, height=window_height)
        canvas.pack(fill="both", expand=True)

        # Load the background image
        bg_image = Image.open("images/background.jpg")  # Replace with your image path
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # High-quality resizing
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Add the image to the canvas
        canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

        # Admin Dashboard Header
        canvas.create_text(
            window_width // 2, 40, 
            text="FitJourney Admin Dashboard", 
            font=("Arial", 20, "bold"), 
            fill="black"
        )

        # Display Admin Info
        canvas.create_text(
            window_width // 2, 80, 
            text=f"Admin ID: {user_id}", 
            font=("Arial", 12), 
            fill="black"
        )

        # Add buttons for the dashboard functionality
        btn_manage_Worktype = ttk.Button(self.window, text="Manage Worktype", command=self.manage_worktype)
        btn_manage_Exercise = ttk.Button(self.window, text="Manage Exercise", command=self.manage_Exercise)
        btn_manage_users = ttk.Button(self.window, text="Manage Users", command=self.manage_users)
        btn_logout = ttk.Button(self.window, text="Logout", command=self.logout_and_redirect)

        # Place buttons on the canvas
        canvas.create_window(window_width // 2, 120, window=btn_manage_Worktype)
        canvas.create_window(window_width // 2, 170, window=btn_manage_Exercise)
        canvas.create_window(window_width // 2, 220, window=btn_manage_users)
        canvas.create_window(window_width // 2, 270, window=btn_logout)

        self.window.mainloop()


    def manage_worktype(self):
        # Close the previous manage window if it's still open
        if hasattr(self, 'manage_window') and self.manage_window.winfo_exists():
            self.manage_window.destroy()

        # Create a new window to manage workout types
        self.manage_window = tk.Toplevel()
        self.manage_window.title("Manage Workout Types")
        self.manage_window.geometry("600x400")

        # Create Treeview widget to display workout types
        tree = ttk.Treeview(self.manage_window, columns=("ID", "Name"), show="headings")
        tree.heading("ID", text="Type ID")
        tree.heading("Name", text="Workout Type Name")
        tree.pack(fill=tk.BOTH, expand=True)

        # Fetch workout type data from the database
        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM workout_types")
            workout_types = cursor.fetchall()
            conn.close()

            # Insert the workout type data into the Treeview
            for workout in workout_types:
                tree.insert("", "end", values=workout)

        # Function to edit a selected workout type
        def edit_workout_type():
            selected_item = tree.selection()
            if selected_item:
                type_id = tree.item(selected_item)["values"][0]
                self.edit_workout_type_window(type_id)
            else:
                messagebox.showwarning("Selection Error", "Please select a workout type to edit.")

        # Function to delete a selected workout type
        def delete_workout_type():
            selected_item = tree.selection()
            if selected_item:
                type_id = tree.item(selected_item)["values"][0]
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete workout type {type_id}?")
                if confirm:
                    conn = self.db_connection.connect_db()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM workout_types WHERE id = %s", (type_id,))
                        conn.commit()
                        conn.close()
                        tree.delete(selected_item)  # Remove from treeview
                        messagebox.showinfo("Success", f"Workout type {type_id} deleted successfully.")
            else:
                messagebox.showwarning("Selection Error", "Please select a workout type to delete.")

        # Add Edit and Delete buttons
        btn_edit = ttk.Button(self.manage_window, text="Edit Workout Type", command=edit_workout_type)
        btn_edit.pack(side=tk.LEFT, padx=20, pady=20)

        btn_delete = ttk.Button(self.manage_window, text="Delete Workout Type", command=delete_workout_type)
        btn_delete.pack(side=tk.LEFT, padx=20, pady=20)




    def manage_Exercise(self):
        # Close the previous manage window if it's still open
        if hasattr(self, 'manage_window') and self.manage_window.winfo_exists():
            self.manage_window.destroy()

        # Create a new window to manage exercises
        self.manage_window = tk.Toplevel()
        self.manage_window.title("Manage Exercises")
        self.manage_window.geometry("800x400")

        # Create Treeview widget to display exercises
        tree = ttk.Treeview(self.manage_window, columns=("ID", "Name", "Workout Type"), show="headings")
        tree.heading("ID", text="Exercise ID")
        tree.heading("Name", text="Exercise Name")
        tree.heading("Workout Type", text="Workout Type")
        tree.pack(fill=tk.BOTH, expand=True)

        # Fetch exercise data from the database
        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.name, w.name AS workout_type
                FROM exercise_types e
                LEFT JOIN workout_types w ON e.workout_type_id = w.id
            """)
            exercises = cursor.fetchall()
            conn.close()

            # Insert the exercise data into the Treeview
            for exercise in exercises:
                tree.insert("", "end", values=exercise)

        # Function to edit a selected exercise
        def edit_exercise():
            selected_item = tree.selection()
            if selected_item:
                exercise_id = tree.item(selected_item)["values"][0]
                self.edit_exercise_window(exercise_id)
            else:
                messagebox.showwarning("Selection Error", "Please select an exercise to edit.")

        # Function to delete a selected exercise
        def delete_exercise():
            selected_item = tree.selection()
            if selected_item:
                exercise_id = tree.item(selected_item)["values"][0]
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete exercise {exercise_id}?")
                if confirm:
                    conn = self.db_connection.connect_db()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM exercise_types WHERE id = %s", (exercise_id,))
                        conn.commit()
                        conn.close()
                        tree.delete(selected_item)  # Remove from treeview
                        messagebox.showinfo("Success", f"Exercise {exercise_id} deleted successfully.")
            else:
                messagebox.showwarning("Selection Error", "Please select an exercise to delete.")

        # Add Edit and Delete buttons
        btn_edit = ttk.Button(self.manage_window, text="Edit Exercise", command=edit_exercise)
        btn_edit.pack(side=tk.LEFT, padx=20, pady=20)

        btn_delete = ttk.Button(self.manage_window, text="Delete Exercise", command=delete_exercise)
        btn_delete.pack(side=tk.LEFT, padx=20, pady=20)











    def manage_users(self):
        # Close the previous manage window if it's still open
        if hasattr(self, 'manage_window') and self.manage_window.winfo_exists():
            self.manage_window.destroy()

        # Create a new window to manage users
        self.manage_window = tk.Toplevel()
        self.manage_window.title("Manage Users")
        self.manage_window.geometry("600x400")

        # Create Treeview widget to display users
        tree = ttk.Treeview(self.manage_window, columns=("ID", "Username", "Password"), show="headings")
        tree.heading("ID", text="User ID")
        tree.heading("Username", text="Username")
        tree.heading("Password", text="Password")
        tree.pack(fill=tk.BOTH, expand=True)

        # Fetch user data from the database
        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password FROM users")
            users = cursor.fetchall()
            conn.close()

            # Insert the user data into the Treeview
            for user in users:
                tree.insert("", "end", values=user)

        # Function to edit a selected user
        def edit_user():
            selected_item = tree.selection()
            if selected_item:
                user_id = tree.item(selected_item)["values"][0]
                self.edit_user_window(user_id)
            else:
                messagebox.showwarning("Selection Error", "Please select a user to edit.")

        # Function to delete a selected user
        def delete_user():
            selected_item = tree.selection()
            if selected_item:
                user_id = tree.item(selected_item)["values"][0]
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user_id}?")
                if confirm:
                    conn = self.db_connection.connect_db()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                        conn.commit()
                        conn.close()
                        tree.delete(selected_item)  # Remove from treeview
                        messagebox.showinfo("Success", f"User {user_id} deleted successfully.")
            else:
                messagebox.showwarning("Selection Error", "Please select a user to delete.")

        # Add Edit and Delete buttons
        btn_edit = ttk.Button(self.manage_window, text="Edit User", command=edit_user)
        btn_edit.pack(side=tk.LEFT, padx=20, pady=20)

        btn_delete = ttk.Button(self.manage_window, text="Delete User", command=delete_user)
        btn_delete.pack(side=tk.LEFT, padx=20, pady=20)



    def edit_user_window(self, user_id):
        # Create a new window to edit user details
        edit_window = tk.Toplevel()
        edit_window.title("Edit User")
        edit_window.geometry("400x300")

        # Fetch user details from the database
        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            conn.close()

        # Create Entry fields for Username and Password
        canvas = tk.Canvas(edit_window, width=400, height=300)
        canvas.pack()

        canvas.create_text(100, 50, text="Username:", anchor="e", font=("Arial", 12))
        entry_username = ttk.Entry(edit_window)
        entry_username.insert(0, user[0])  # Set the current username
        canvas.create_window(220, 50, window=entry_username, width=180)

        canvas.create_text(100, 100, text="Password:", anchor="e", font=("Arial", 12))
        entry_password = ttk.Entry(edit_window, show="*")
        entry_password.insert(0, user[1])  # Set the current password
        canvas.create_window(220, 100, window=entry_password, width=180)

        # Function to save edited details
        def save_changes():
            new_username = entry_username.get()
            new_password = entry_password.get()

            if not new_username or not new_password:
                messagebox.showerror("Error", "Both fields are required.")
                return

            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", 
                            (new_username, new_password, user_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User details updated successfully.")
                edit_window.destroy()
                # Reload manage users window
                self.manage_users()


        # Save changes button
        btn_save = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        canvas.create_window(200, 200, window=btn_save, width=120)








    def edit_workout_type_window(self, type_id):
        # Create a new window to edit workout type details
            edit_window = tk.Toplevel()
            edit_window.title("Edit Workout Type")
            edit_window.geometry("400x300")

            # Fetch workout type details from the database
            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM workout_types WHERE id = %s", (type_id,))
                workout_type = cursor.fetchone()
                conn.close()

            # Create Entry field for Workout Type Name
            canvas = tk.Canvas(edit_window, width=400, height=300)
            canvas.pack()

            canvas.create_text(100, 50, text="Workout Type Name:", anchor="e", font=("Arial", 12))
            entry_name = ttk.Entry(edit_window)
            entry_name.insert(0, workout_type[0])  # Set the current workout type name
            canvas.create_window(220, 50, window=entry_name, width=180)

            # Function to save edited details
            def save_changes():
                new_name = entry_name.get()

                if not new_name:
                    messagebox.showerror("Error", "Workout Type Name is required.")
                    return

                conn = self.db_connection.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE workout_types SET name = %s WHERE id = %s", 
                                (new_name, type_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Workout Type details updated successfully.")
                    edit_window.destroy()
                    # Reload manage workout types window
                    self.manage_worktype()

            # Save changes button
            btn_save = ttk.Button(edit_window, text="Save Changes", command=save_changes)
            canvas.create_window(200, 150, window=btn_save, width=120)




    def edit_exercise_window(self, exercise_id):
        # Create a new window to edit exercise details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Exercise")
        edit_window.geometry("400x300")

        # Fetch exercise details from the database
        conn = self.db_connection.connect_db()
        exercise = None
        workout_types = []
        if conn:
            cursor = conn.cursor()
            # Fetch exercise details
            cursor.execute("SELECT name, workout_type_id FROM exercise_types WHERE id = %s", (exercise_id,))
            exercise = cursor.fetchone()

            # Fetch available workout types
            cursor.execute("SELECT id, name FROM workout_types")
            workout_types = cursor.fetchall()
            conn.close()

        if not exercise:
            messagebox.showerror("Error", "Exercise not found.")
            edit_window.destroy()
            return

        # Extract current details
        current_name, current_workout_type_id = exercise

        # Create canvas for layout
        canvas = tk.Canvas(edit_window, width=400, height=300)
        canvas.pack()

        # Exercise Name
        canvas.create_text(100, 50, text="Exercise Name:", anchor="e", font=("Arial", 12))
        entry_name = ttk.Entry(edit_window)
        entry_name.insert(0, current_name)  # Set the current exercise name
        canvas.create_window(220, 50, window=entry_name, width=180)

        # Workout Type Dropdown
        canvas.create_text(100, 100, text="Workout Type:", anchor="e", font=("Arial", 12))
        workout_type_var = tk.StringVar(value=str(current_workout_type_id))
        dropdown_workout_type = ttk.Combobox(edit_window, textvariable=workout_type_var, state="readonly")
        dropdown_workout_type["values"] = [f"{wt[0]} - {wt[1]}" for wt in workout_types]
        dropdown_workout_type.pack()
        canvas.create_window(220, 100, window=dropdown_workout_type, width=180)

        # Function to save edited details
        def save_changes():
            new_name = entry_name.get()
            selected_workout_type = workout_type_var.get().split(" - ")[0]  # Extract type ID

            if not new_name or not selected_workout_type:
                messagebox.showerror("Error", "All fields are required.")
                return

            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE exercise_types 
                    SET name = %s, workout_type_id = %s 
                    WHERE id = %s
                """, (new_name, selected_workout_type, exercise_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Exercise details updated successfully.")
                edit_window.destroy()
                # Reload manage exercise window
                self.manage_Exercise()

        # Save Changes Button
        btn_save = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        canvas.create_window(200, 200, window=btn_save, width=120)





    def main_dashboard(self, user_id):
        self.window.destroy()  # Destroy the previous window
        self.window = tk.Tk()
        self.window.resizable(False, False)  # Disable resizing
        self.window.title("FitJourney Dashboard")

        # Window dimensions
        window_width = 400
        window_height = 300

        # Center the window
        position_x = (self.window.winfo_screenwidth() // 2) - (window_width // 2)
        position_y = (self.window.winfo_screenheight() // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Add a canvas to set the background image
        canvas = tk.Canvas(self.window, width=window_width, height=window_height)
        canvas.pack(fill="both", expand=True)

        # Load the background image
        bg_image = Image.open("images/background.jpg")  # Replace with your image path
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # High-quality resizing
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Add the image to the canvas
        canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

        # Add text and buttons directly to the canvas
        canvas.create_text(
            window_width // 2, 50, 
            text="Welcome to FitJourney!", 
            font=("Arial", 18, "bold"), 
            fill="black"
        )

        # Add buttons to the canvas
        btn_log_workout = ttk.Button(self.window, text="Log Workout", command=lambda: self.log_workout(user_id))
        btn_view_progress = ttk.Button(self.window, text="View Progress", command=lambda: self.plot_progress(user_id))
        btn_logout = ttk.Button(self.window, text="Logout", command=lambda: self.logout_and_redirect())

        # Place buttons on the canvas
        canvas.create_window(window_width // 2, 120, window=btn_log_workout)
        canvas.create_window(window_width // 2, 170, window=btn_view_progress)
        canvas.create_window(window_width // 2, 220, window=btn_logout)

        self.window.mainloop()


   
    def log_workout(self, user_id):
        def save_log():
            # Retrieve input values
            workout_type = combobox_workout_type.get()
            exercise_type = combobox_exercise_type.get()
            duration = entry_duration.get()
            reps = entry_reps.get()  # Retrieve reps value
            fitness_goal = combobox_fitness_goal.get()
            weight = entry_weight.get()
            height = entry_height.get()

            # Validate input fields
            if not all([workout_type, exercise_type, duration, reps, fitness_goal, weight, height]):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                duration = float(duration)
                reps = int(reps)  # Validate reps as an integer
                weight = float(weight)
                height = float(height)
            except ValueError:
                messagebox.showerror("Error", "Duration, Reps, Weight, and Height must be numbers.")
                return

            # Destroy the log_window only after successful retrieval and validation
            log_window.destroy()

            # Calculate calories (considering reps)
            calories = self.calculate_calories(workout_type, duration, reps)

            # Save data to the database
            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO logs (user_id, workout_type, exercise_type, duration, reps, calories, fitness_goal, weight, height, date_logged) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())",
                    (user_id, workout_type, exercise_type, duration, reps, calories, fitness_goal, weight, height),
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Workout logged successfully!")

        def update_exercises(event):
            selected_workout_type = combobox_workout_type.get()

            # Retrieve exercises based on selected workout type
            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.name
                    FROM exercise_types e
                    JOIN workout_types w ON e.workout_type_id = w.id
                    WHERE w.name = %s
                """, (selected_workout_type,))
                exercises = cursor.fetchall()
                conn.close()

            # Populate combobox with exercises
            if exercises:
                exercise_names = [exercise[0] for exercise in exercises]  # Extract exercise names from the result
                combobox_exercise_type['values'] = exercise_names
                combobox_exercise_type.set(selected_workout_type)  # Set the current exercise type value
            else:
                combobox_exercise_type['values'] = []  # Clear the list if no exercises are found


        # Create a new window
        log_window = tk.Toplevel()
        log_window.resizable(False, False)  # Disable resizing
        canvas = self.setup_window_with_background(log_window, "Log Workout", 500, 550, "images/background.jpg")

        x_center = 250  # Center alignment for canvas

        # Add input fields
        canvas.create_text(x_center, 40, text="Workout Type:", anchor="center", font=("Arial", 12))
        combobox_workout_type = ttk.Combobox(log_window, values=["Chest", "Back", "Legs", "Arms", "Cardio"])
        combobox_workout_type.bind("<<ComboboxSelected>>", update_exercises)
        canvas.create_window(x_center, 60, window=combobox_workout_type, width=250)

        canvas.create_text(x_center, 90, text="Exercise Type:", anchor="center", font=("Arial", 12))
        combobox_exercise_type = ttk.Combobox(log_window)
        canvas.create_window(x_center, 120, window=combobox_exercise_type, width=250)

        canvas.create_text(x_center, 160, text="Duration (mins):", anchor="center", font=("Arial", 12))
        entry_duration = ttk.Entry(log_window)
        canvas.create_window(x_center, 190, window=entry_duration, width=250)

        canvas.create_text(x_center, 220, text="Reps:", anchor="center", font=("Arial", 12))
        entry_reps = ttk.Entry(log_window)  # New input field for reps
        canvas.create_window(x_center, 250, window=entry_reps, width=250)

        canvas.create_text(x_center, 300, text="Fitness Goal:", anchor="center", font=("Arial", 12))
        combobox_fitness_goal = ttk.Combobox(log_window, values=["Lose Weight", "Build Muscle", "Stay Fit"])
        canvas.create_window(x_center, 330, window=combobox_fitness_goal, width=250)

        canvas.create_text(x_center, 370, text="Weight (kg):", anchor="center", font=("Arial", 12))
        entry_weight = ttk.Entry(log_window)
        canvas.create_window(x_center, 400, window=entry_weight, width=250)

        canvas.create_text(x_center, 440, text="Height (cm):", anchor="center", font=("Arial", 12))
        entry_height = ttk.Entry(log_window)
        canvas.create_window(x_center, 470, window=entry_height, width=250)

        save_button = ttk.Button(log_window, text="Save", command=save_log)
        canvas.create_window(x_center, 510, window=save_button)

#### Update `calculate_calories` Method


    def calculate_calories(self, workout_type, duration, reps):
        # Base calories burned calculation
        base_calories_per_min = {
            "Chest": 6,
            "Back": 8,
            "Legs": 7,
            "Arms": 5,
            "Cardio": 10,
        }
        reps_factor = reps * 0.1  # Assume each rep adds 0.1 calories (adjust based on requirements)
        calories = base_calories_per_min.get(workout_type, 5) * duration + reps_factor
        return round(calories, 2)

    # Plot Progress
        # Plot Progress
        # Plot Progress with Responsiveness



        
    def plot_progress(self, user_id):
        progress_window = tk.Toplevel()
        progress_window.title("Workout Progress")
        progress_window.resizable(True, True)  # Allow resizing
        progress_window.geometry("900x750")
        progress_window.minsize(900, 600)

        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            
            # Query to get the log data
            cursor.execute(
                "SELECT id, date_logged, workout_type, duration, calories, fitness_goal, weight, height, reps FROM logs WHERE user_id = %s ORDER BY date_logged ASC",
                (user_id,)
            )
            data = cursor.fetchall()

            # Query to count the number of logs
            cursor.execute(
                "SELECT COUNT(*) FROM logs WHERE user_id = %s",
                (user_id,)
            )
            log_count = cursor.fetchone()[0]  # Fetch the count result

            conn.close()

            if not data:
                messagebox.showinfo("No Data", "No progress data to display.")
                progress_window.destroy()
                return

            # Display the log count
            log_count_label = ttk.Label(progress_window, text=f"Total Logs: {log_count}")
            log_count_label.pack(pady=10)

            # Extract data for the plot
            log_ids, dates, workout_types, durations, calories, fitness_goals, weights, heights, reps = zip(*data)

            # Main container frame
            main_frame = ttk.Frame(progress_window)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Frame for Plot
            plot_frame = ttk.Frame(main_frame)
            plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))

            # Matplotlib plot
            fig = Figure(figsize=(5, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(dates, durations, label="Duration (mins)", marker='o', linestyle='-', color='blue')
            ax.plot(dates, calories, label="Calories Burned", marker='o', linestyle='--', color='red')
            ax.set_title("Workout Progress Over Time", fontsize=10)
            ax.set_xlabel("Date", fontsize=9)
            ax.set_ylabel("Metrics", fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(True)

            # Embed plot in tkinter
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Frame for Table
            table_frame = ttk.Frame(main_frame)
            table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Create a canvas to add scrolling
            canvas_table = tk.Canvas(table_frame)
            canvas_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar for the canvas
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas_table.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas_table.configure(yscrollcommand=scrollbar.set)

            # Create the table (Treeview) widget
            tree = ttk.Treeview(canvas_table, columns=("ID", "Date", "Workout Type", "Duration", "Calories", "Goal", "Weight", "Height", "Reps"), show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            # Define columns and headings
            tree.heading("ID", text="ID")
            tree.heading("Date", text="Date")
            tree.heading("Workout Type", text="Workout Type")
            tree.heading("Duration", text="Duration (mins)")
            tree.heading("Calories", text="Calories")
            tree.heading("Goal", text="Fitness Goal")
            tree.heading("Weight", text="Weight (kg)")
            tree.heading("Height", text="Height (cm)")
            tree.heading("Reps", text="Reps")

            # Adjust column width
            tree.column("ID", width=50)
            tree.column("Date", width=150)
            tree.column("Workout Type", width=150)
            tree.column("Duration", width=100)
            tree.column("Calories", width=100)
            tree.column("Goal", width=100)
            tree.column("Weight", width=100)
            tree.column("Height", width=100)
            tree.column("Reps", width=100)

            # Insert logs into the treeview table
            for i, log_id in enumerate(log_ids):
                tree.insert("", "end", values=(log_id, dates[i], workout_types[i], durations[i], calories[i], fitness_goals[i], weights[i], heights[i], reps[i]))

            # Functions for editing and deleting logs
            def edit_log():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a log entry to edit.")
                    return

                selected_log_id = tree.item(selected_item)["values"][0]  # Get selected log ID
                self.edit_log_entry(user_id, selected_log_id, progress_window)

            def delete_log():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a log entry to delete.")
                    return

                selected_log_id = tree.item(selected_item)["values"][0]  # Get selected log ID
                response = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the log entry with ID {selected_log_id}?")
                if response:
                    self.delete_log_entry(selected_log_id, user_id, progress_window)

            # Add buttons for editing and deleting
            btn_edit_log = ttk.Button(progress_window, text="Edit Log", command=edit_log)
            btn_delete_log = ttk.Button(progress_window, text="Delete Log", command=delete_log)

            # Position the buttons
            btn_edit_log.pack(side=tk.LEFT, padx=10, pady=10)
            btn_delete_log.pack(side=tk.LEFT, padx=10, pady=10)

            # Add a Back button to close the progress window
            def go_back():
                progress_window.destroy()

            btn_back = ttk.Button(progress_window, text="Back", command=go_back)
            btn_back.pack(side=tk.BOTTOM, padx=10, pady=10)

            progress_window.mainloop()







    def edit_log_entry(self, user_id, log_id, progress_window):
        # Create a new window for editing the log entry
        edit_window = tk.Toplevel()
        edit_window.resizable(False, False)
        edit_window.title("Edit Log")

        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT workout_type, exercise_type, duration, reps, calories, fitness_goal, weight, height FROM logs WHERE id = %s AND user_id = %s", (log_id, user_id))
            data = cursor.fetchone()
            conn.close()

        if not data:
            messagebox.showerror("Error", "Log entry not found.")
            return

        workout_type, exercise_type, duration, reps, calories, fitness_goal, weight, height = data

        # Add form fields to edit log details
        canvas = self.setup_window_with_background(edit_window, "Edit Log", 500, 550, "images/background.jpg")

        x_center = 250  # Center alignment for canvas

        canvas.create_text(x_center, 40, text="Workout Type:", anchor="center", font=("Arial", 12))
        combobox_workout_type = ttk.Combobox(edit_window, values=["Chest", "Back", "Legs", "Arms", "Cardio"])
        combobox_workout_type.set(workout_type)  # Set the current value
        canvas.create_window(x_center, 60, window=combobox_workout_type, width=250)

        canvas.create_text(x_center, 90, text="Exercise Type:", anchor="center", font=("Arial", 12))
        combobox_exercise_type = ttk.Combobox(edit_window)
        combobox_exercise_type.set(exercise_type)  # Set the current value
        canvas.create_window(x_center, 120, window=combobox_exercise_type, width=250)

        # Function to update exercises based on selected workout type
        def update_exercises(event):
            selected_workout_type = combobox_workout_type.get()

            # Retrieve exercises based on selected workout type
            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.name
                    FROM exercise_types e
                    JOIN workout_types w ON e.workout_type_id = w.id
                    WHERE w.name = %s
                """, (selected_workout_type,))
                exercises = cursor.fetchall()
                conn.close()

            # Populate combobox with exercises
            if exercises:
                exercise_names = [exercise[0] for exercise in exercises]  # Extract exercise names from the result
                combobox_exercise_type['values'] = exercise_names
                combobox_exercise_type.set(exercise_type)  # Set the current exercise type value
            else:
                combobox_exercise_type['values'] = []  # Clear the list if no exercises are found

        combobox_workout_type.bind("<<ComboboxSelected>>", update_exercises)
        update_exercises(None)  # Initial update for exercise types

        canvas.create_text(x_center, 160, text="Duration (mins):", anchor="center", font=("Arial", 12))
        entry_duration = ttk.Entry(edit_window)
        entry_duration.insert(0, duration)
        canvas.create_window(x_center, 190, window=entry_duration, width=250)

        canvas.create_text(x_center, 220, text="Reps:", anchor="center", font=("Arial", 12))
        entry_reps = ttk.Entry(edit_window)
        entry_reps.insert(0, reps)
        canvas.create_window(x_center, 250, window=entry_reps, width=250)

        canvas.create_text(x_center, 300, text="Fitness Goal:", anchor="center", font=("Arial", 12))
        combobox_fitness_goal = ttk.Combobox(edit_window, values=["Lose Weight", "Build Muscle", "Stay Fit"])
        combobox_fitness_goal.set(fitness_goal)
        canvas.create_window(x_center, 330, window=combobox_fitness_goal, width=250)

        canvas.create_text(x_center, 370, text="Weight (kg):", anchor="center", font=("Arial", 12))
        entry_weight = ttk.Entry(edit_window)
        entry_weight.insert(0, weight)
        canvas.create_window(x_center, 400, window=entry_weight, width=250)

        canvas.create_text(x_center, 440, text="Height (cm):", anchor="center", font=("Arial", 12))
        entry_height = ttk.Entry(edit_window)
        entry_height.insert(0, height)
        canvas.create_window(x_center, 470, window=entry_height, width=250)

        def save_edited_log():
            new_workout_type = combobox_workout_type.get()
            new_exercise_type = combobox_exercise_type.get()
            new_duration = entry_duration.get()
            new_reps = entry_reps.get()
            new_fitness_goal = combobox_fitness_goal.get()
            new_weight = entry_weight.get()
            new_height = entry_height.get()

            # Validate input fields
            if not all([new_workout_type, new_exercise_type, new_duration, new_reps, new_fitness_goal, new_weight, new_height]):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                new_duration = float(new_duration)
                new_reps = int(new_reps)
                new_weight = float(new_weight)
                new_height = float(new_height)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for duration, reps, weight, and height.")
                return

            conn = self.db_connection.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE logs
                    SET workout_type = %s, exercise_type = %s, duration = %s, reps = %s, calories = %s, fitness_goal = %s, weight = %s, height = %s
                    WHERE id = %s AND user_id = %s
                """, (new_workout_type, new_exercise_type, new_duration, new_reps, new_duration * 5, new_fitness_goal, new_weight, new_height, log_id, user_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Log updated successfully.")
                edit_window.destroy()

                # Close the progress window and reload it
                progress_window.destroy()
                self.plot_progress(user_id)  # Reopen with updated data

        # Add Save button
        btn_save = ttk.Button(edit_window, text="Save Changes", command=save_edited_log)
        canvas.create_window(x_center, 510, window=btn_save, width=250)

        edit_window.mainloop()





    def delete_log_entry(self, log_id, user_id, progress_window):
        conn = self.db_connection.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs WHERE id = %s", (log_id,))
            conn.commit()
            conn.close()

        messagebox.showinfo("Success", "Log deleted successfully.")

        # Close the progress window and reload it
        progress_window.destroy()
        self.plot_progress(user_id)  # Reopen with updated data



    # # Calorie Calculation
    # def calculate_calories(self, workout_type, duration):
    #     calorie_rates = {
    #         "Chest": 10,
    #         "Legs": 12,
    #         "Back": 9,
    #         "Arms": 8,
    #     }
    #     return calorie_rates.get(workout_type, 5) * duration


if __name__ == "__main__":
    app = FitJourneyApp()
    app.run()
