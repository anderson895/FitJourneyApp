import tkinter as tk
from tkinter import messagebox
import pymysql

class Connections:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "fitjourney",
        }
        self.connection = None  # To hold the database connection object

    # Establish database connection
    def connect_db(self):
        try:
            self.connection = pymysql.connect(**self.db_config)
            return self.connection
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Could not connect to the database:\n{e}")
            return None

    # Close database connection
    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
            except pymysql.MySQLError as e:
                messagebox.showwarning("Warning", f"Error closing the database connection:\n{e}")
            finally:
                self.connection = None
