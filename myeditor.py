import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview
from tkinter.scrolledtext import ScrolledText

class MyEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyEditor - Professional Code Editor")
        self.root.geometry("1200x700")
        self.file_path = None
        self.current_folder = os.getcwd()

        # Apply dark mode theme
        self.style = Style("darkly")

        # Setup layout
        self.setup_ui()

    def setup_ui(self):
        # Sidebar + Editor split
        self.main_pane = tk.PanedWindow(self.root, orient="horizontal")
        self.main_pane.pack(fill="both", expand=True)

        # Sidebar (Folder Tree)
        self.tree_frame = tk.Frame(self.main_pane)
        self.folder_tree = Treeview(self.tree_frame, show="tree")
        self.folder_tree.pack(fill="both", expand=True)
        self.folder_tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.populate_tree(self.current_folder)

        # Editor Area
        self.text_area = ScrolledText(self.main_pane, wrap="word", font=("Consolas", 13))
        self.text_area.pack(fill="both", expand=True)

        self.main_pane.add(self.tree_frame, width=250)
        self.main_pane.add(self.text_area)

        # Menu
        self.build_menu()

    def build_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def open_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.folder_tree.delete(*self.folder_tree.get_children())
            self.populate_tree(folder)

    def populate_tree(self, path, parent=""):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            node = self.folder_tree.insert(parent, "end", text=item, open=False)
            if os.path.isdir(item_path):
                self.populate_tree(item_path, node)

    def on_file_select(self, event):
        selected = self.folder_tree.selection()
        if not selected:
            return
        file_name = self.folder_tree.item(selected, "text")
        parent_id = self.folder_tree.parent(selected)
        folder_path = self.current_folder
        while parent_id:
            folder_path = os.path.join(folder_path, self.folder_tree.item(parent_id)["text"])
            parent_id = self.folder_tree.parent(parent_id)
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path):
            with open(full_path, "r") as f:
                content = f.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
            self.file_path = full_path

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as f:
                f.write(self.text_area.get("1.0", tk.END))

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w") as f:
                f.write(self.text_area.get("1.0", tk.END))
            self.file_path = path

if __name__ == "__main__":
    root = tk.Tk()
    app = MyEditorApp(root)
    root.mainloop()
