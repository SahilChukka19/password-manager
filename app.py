import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database.db_handler import add_password, retrieve_passwords, update_password, delete_password, authenticate_user, register_user
from session_manager import SessionManager

# Initialize session
session = SessionManager()

# Toggle password visibility for any Entry widget
def toggle_password(entry, button):
    if entry.cget("show") == "*":
        entry.config(show="")
        button.config(text="Hide")
    else:
        entry.config(show="*")
        button.config(text="Show")

# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()

    user_id = authenticate_user(username, password)
    if user_id:
        session.set_user(user_id)
        messagebox.showinfo("Login Successful", "Welcome!!!")
        login_window.withdraw()
        open_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Register function
def register():
    def save_user():
        username = new_username_entry.get()
        password = new_password_entry.get()

        if username and password:
            register_user(username, password)
            messagebox.showinfo("Registration Successful", "You can login now!")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    register_window = tk.Toplevel(login_window)
    register_window.title("Register")

    new_username_label = tk.Label(register_window, text="Username")
    new_username_label.pack(pady=5)
    new_username_entry = tk.Entry(register_window, width=40)
    new_username_entry.pack(pady=5)

    new_password_label = tk.Label(register_window, text="Password")
    new_password_label.pack(pady=5)
    new_password_entry = tk.Entry(register_window, width=40, show="*")  # Masked input
    new_password_entry.pack(pady=5)

    toggle_button = tk.Button(register_window, text="Show Password", command=lambda: toggle_password(new_password_entry, toggle_button))
    toggle_button.pack(pady=5)

    register_button = tk.Button(register_window, text="Register", command=save_user)
    register_button.pack(pady=10)

# Add password to database
def add_password_to_db():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    user_id = session.get_user()
    add_password(user_id, website, username, password)
    messagebox.showinfo("Success", "Password added successfully")

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    update_password_list()

# Edit password
def edit_password():
    selected_item = password_listbox.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a password to edit.")
        return

    item_data = password_listbox.item(selected_item, 'values')
    website, username, password = item_data[:3]

    def save_changes():
        new_website = edit_website_entry.get()
        new_username = edit_username_entry.get()
        new_password = edit_password_entry.get()

        user_id = session.get_user()
        update_password(user_id, website, username, new_website, new_username, new_password)
        messagebox.showinfo("Success", "Password updated successfully.")
        edit_window.destroy()
        update_password_list()

    # Open edit window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Password")

    tk.Label(edit_window, text="Website").pack(pady=5)
    edit_website_entry = tk.Entry(edit_window, width=40)
    edit_website_entry.insert(0, website)
    edit_website_entry.pack(pady=5)

    tk.Label(edit_window, text="Username").pack(pady=5)
    edit_username_entry = tk.Entry(edit_window, width=40)
    edit_username_entry.insert(0, username)
    edit_username_entry.pack(pady=5)

    tk.Label(edit_window, text="Password").pack(pady=5)
    edit_password_entry = tk.Entry(edit_window, width=40, show="*")
    edit_password_entry.insert(0, password)
    edit_password_entry.pack(pady=5)

    toggle_button = tk.Button(edit_window, text="Show Password", command=lambda: toggle_password(edit_password_entry, toggle_button))
    toggle_button.pack(pady=5)

    tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

# Delete password
def delete_password_entry():
    selected_item = password_listbox.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a password to delete.")
        return

    item_data = password_listbox.item(selected_item, 'values')
    website, username, _ = item_data[:3]

    user_id = session.get_user()
    delete_password(user_id, website, username)
    messagebox.showinfo("Success", "Password deleted successfully.")
    update_password_list()

# Update password list
def update_password_list():
    for row in password_listbox.get_children():
        password_listbox.delete(row)

    user_id = session.get_user()
    passwords = retrieve_passwords(user_id)
    for password in passwords:
        password_listbox.insert("", tk.END, values=password)

# Open main application
def open_main_app():
    def logout():
        session.clear()
        root.destroy()
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        login_window.deiconify()

    global root, website_entry, username_entry, password_entry, password_listbox
    root = tk.Tk()
    root.title("Password Manager")

    logout_button = tk.Button(root, text="Logout", command=logout)
    logout_button.pack(pady=10)

    website_label = tk.Label(root, text="Website")
    website_label.pack(pady=5)
    website_entry = tk.Entry(root, width=40)
    website_entry.pack(pady=5)

    username_label = tk.Label(root, text="Username")
    username_label.pack(pady=5)
    username_entry = tk.Entry(root, width=40)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, width=40, show="*")
    password_entry.pack(pady=5)

    toggle_button = tk.Button(root, text="Show Password", command=lambda: toggle_password(password_entry, toggle_button))
    toggle_button.pack(pady=5)

    add_button = tk.Button(root, text="Add Password", width=20, command=add_password_to_db)
    add_button.pack(pady=10)

    edit_button = tk.Button(root, text="Edit Password", width=20, command=edit_password)
    edit_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Password", width=20, command=delete_password_entry)
    delete_button.pack(pady=5)

    password_listbox = ttk.Treeview(root, columns=("Website", "Username", "Password", "Date Added"), show="headings")
    password_listbox.heading("Website", text="Website")
    password_listbox.heading("Username", text="Username")
    password_listbox.heading("Password", text="Password")
    password_listbox.heading("Date Added", text="Date Added")
    password_listbox.pack(pady=10)

    update_password_list()

    root.mainloop()

# Login screen initialization
def create_login_window():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, width=40)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, width=40, show="*")  # Masked input
    password_entry.pack(pady=5)

    toggle_button = tk.Button(login_window, text="Show Password", command=lambda: toggle_password(password_entry, toggle_button))
    toggle_button.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=10)

    register_button = tk.Button(login_window, text="Register", command=register)
    register_button.pack(pady=5)

    login_window.mainloop()

# Start the application
create_login_window()
