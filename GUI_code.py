import os
import stat
import tkinter as tk
from tkinter import filedialog, messagebox
from pwd import getpwuid
from time import ctime
import subprocess

def create_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            open(filename, 'a').close()
            messagebox.showinfo("Success", f"File '{filename}' created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to create file: {e}")

def delete_file():
    filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", ".")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            os.remove(filename)
            messagebox.showinfo("Success", f"File '{filename}' deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to delete file: {e}")

def copy_file():
    source = filedialog.askopenfilename(filetypes=[("All Files", ".")])
    print("Source file path:", source)  # Print source file path for debugging
    if source:
        destination = filedialog.asksaveasfilename(filetypes=[("All Files", ".")])
        print("Destination file path:", destination)  # Print destination file path for debugging
        if destination:
            try:
                with open(source, 'rb') as src_file, open(destination, 'wb') as dest_file:
                    dest_file.write(src_file.read())
                messagebox.showinfo("Success", f"File '{source}' copied to '{destination}' successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to copy file: {e}")

def move_file():
    source = filedialog.askopenfilename(filetypes=[("All Files", ".")])
    print("Source file path:", source)  # Print source file path for debugging
    if source:
        destination = filedialog.asksaveasfilename(filetypes=[("All Files", ".")])
        print("Destination file path:", destination)  # Print destination file path for debugging
        if destination:
            try:
                os.rename(source, destination)
                messagebox.showinfo("Success", f"File '{source}' moved to '{destination}' successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to move file: {e}")

def write_to_file_rewrite():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            with open(filename, 'w') as file:
                subprocess.run(['gedit', '--new-window', '--wait', filename])  # Open file in gedit
            messagebox.showinfo("Success", f"Write to file '{filename}' using gedit.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open gedit: {e}")

def write_to_file_append():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            with open(filename, 'a') as file:
                subprocess.run(['gedit', '--new-window', '--wait', filename])  # Open file in gedit
            messagebox.showinfo("Success", f"Append to file '{filename}' using gedit.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open gedit: {e}")

def write_to_file():
    top = tk.Toplevel()
    top.title("Write Options")

    write_button = tk.Button(top, text="Write to File", command=write_to_file_rewrite)
    write_button.pack()

    append_button = tk.Button(top, text="Append to File", command=write_to_file_append)
    append_button.pack()

def analyze_file():
    filename = filedialog.askopenfilename(filetypes=[("All Files", ".")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            file_stat = os.stat(filename)
            file_type = "Regular File" if stat.S_ISREG(file_stat.st_mode) else "Unknown"
            access_time = ctime(file_stat.st_atime)
            owner = getpwuid(file_stat.st_uid).pw_name
            inode = file_stat.st_ino
            with open(filename, 'r') as file:
                lines = file.readlines()
                num_lines = len(lines)
                num_words = sum(len(line.split()) for line in lines)
                num_chars = sum(len(line) for line in lines)
            messagebox.showinfo("Analysis", f"Analysis for file '{filename}':\n"
                                             f"File Type: {file_type}\n"
                                             f"Last access time: {access_time}\n"
                                             f"Owner: {owner}\n"
                                             f"Inode number: {inode}\n"
                                             f"Number of characters: {num_chars}\n"
                                             f"Number of lines: {num_lines}\n"
                                             f"Number of words: {num_words}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to analyze file: {e}")

def execute_file():
    filename = filedialog.askopenfilename(filetypes=[("Executable Files", ".c;.cpp;.py;.sh;.java;.html")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            if filename.endswith((".c", ".cpp")):
                subprocess.run(['gcc', filename])  # Compile C/C++ file
                subprocess.run(['./a.out'])  # Execute compiled binary
            elif filename.endswith(".py"):
                subprocess.run(['python', filename])  # Run Python file
            elif filename.endswith(".sh"):
                subprocess.run(['bash', filename])  # Run shell script
            elif filename.endswith(".java"):
                subprocess.run(['javac', filename])  # Compile Java file
                java_filename = os.path.splitext(filename)[0] + ".class"
                subprocess.run(['java', java_filename])  # Execute Java class file
            elif filename.endswith(".html"):
                subprocess.run(['xdg-open', filename])  # Open HTML file in default browser
            else:
                messagebox.showinfo("Info", "Unsupported file type.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to execute file: {e}")

def open_file():
    filename = filedialog.askopenfilename(filetypes=[("All Files", ".")])
    print("File path:", filename)  # Print file path for debugging
    if filename:
        try:
            subprocess.run(['xdg-open', filename])  # Open file with default application
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open file: {e}")

def change_file_mode():
    def change_mode():
        selected_mode = mode_var.get()
        mode_bits = 0
        if "Read" in selected_mode:
            mode_bits |= stat.S_IRUSR
        if "Write" in selected_mode:
            mode_bits |= stat.S_IWUSR
        if "Execute" in selected_mode:
            mode_bits |= stat.S_IXUSR

        try:
            os.chmod(filename, mode_bits)
            messagebox.showinfo("Success", f"Changed file mode to {selected_mode}.")
            top.destroy()  # Close the dialog after mode change
        except Exception as e:
            messagebox.showerror("Error", f"Unable to change file mode: {e}")

    filename = filedialog.askopenfilename(filetypes=[("All Files", ".")])
    if filename:
        top = tk.Toplevel()
        top.title("Change File Mode")

        mode_var = tk.StringVar(top)
        mode_var.set("Read and Write")  # Default mode
        modes = ["Read Only", "Write Only", "Read and Write", "Execute Only", "Read and Execute", "Write and Execute", "Read, Write, and Execute"]
        mode_menu = tk.OptionMenu(top, mode_var, *modes)
        mode_menu.pack()

        change_button = tk.Button(top, text="Change Mode", command=change_mode)
        change_button.pack()

        # Disable the dropdown menu until an option is chosen
        mode_menu.configure(state="disabled")

        def enable_dropdown(event):
            mode_menu.configure(state="normal")

        # Bind the enable_dropdown function to the dropdown menu
        mode_menu.bind("<Button-1>", enable_dropdown)

root = tk.Tk()
root.title("File Management Tool")

create_button = tk.Button(root, text="Create File", command=create_file)
create_button.pack()

delete_button = tk.Button(root, text="Delete File", command=delete_file)
delete_button.pack()

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack()

copy_button = tk.Button(root, text="Copy File", command=copy_file)
copy_button.pack()

move_button = tk.Button(root, text="Move File", command=move_file)
move_button.pack()

write_button = tk.Button(root, text="Write to File", command=write_to_file)
write_button.pack()

analyze_button = tk.Button(root, text="Analyze File", command=analyze_file)
analyze_button.pack()

execute_button = tk.Button(root, text="Execute File", command=execute_file)
execute_button.pack()

change_mode_button = tk.Button(root, text="Change File Mode", command=change_file_mode)
change_mode_button.pack()

root.mainloop()