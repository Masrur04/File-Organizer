import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# Define file categories
CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Music': ['.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css'],
    'Others': []
}

def organize_folder(folder_path):
    folder_path = Path(folder_path)
    for item in os.listdir(folder_path):
        item_path = folder_path / item

        # Skip if it's a directory
        if item_path.is_dir():
            continue

        # Get file extension
        file_ext = item_path.suffix.lower()

        # Find the appropriate category
        found_category = None
        for category, extensions in CATEGORIES.items():
            if file_ext in extensions:
                found_category = category
                break
        if not found_category:
            found_category = 'Others'

        # Create category folder if it doesn't exist
        category_folder = folder_path / found_category
        category_folder.mkdir(exist_ok=True)

        # Move the file
        target_path = category_folder / item

        # Handle duplicates
        if target_path.exists():
            base, ext = os.path.splitext(item)
            counter = 1
            while target_path.exists():
                new_name = f"{base}_{counter}{ext}"
                target_path = category_folder / new_name
                counter += 1

        shutil.move(str(item_path), str(target_path))

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        try:
            organize_folder(folder_selected)
            messagebox.showinfo("Success", f"Organized files in:\n{folder_selected}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# GUI Setup
app = tk.Tk()
app.title("File Organizer")
app.geometry("300x150")
app.resizable(False, False)

label = tk.Label(app, text="Organize Files by Category", font=("Arial", 14))
label.pack(pady=10)

button = tk.Button(app, text="Select Folder", command=select_folder, font=("Arial", 12))
button.pack(pady=20)

app.mainloop()
