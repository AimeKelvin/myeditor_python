import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

class MyEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("MyEditor - Advanced Text Editor")
        self.root.geometry("1000x600")

        self.theme = "light"  # Default theme
        self.file_path = None

        # Split layout (Treeview for folders, Text Area)
        self.main_pane = tk.PanedWindow(self.root, orient="horizontal")
        self.main_pane.pack(fill="both", expand=True)

        # File Explorer
        self.folder_frame = tk.Frame(self.main_pane, width=250, bg="#f0f0f0")
        self.folder_frame.pack(fill="y", side="left")
        self.folder_tree = ttk.Treeview(self.folder_frame)
        self.folder_tree.pack(fill="both", expand=True)
        self.folder_tree.bind("<<TreeviewOpen>>", self.open_file_from_tree)

        # Text Editor Area
        self.text_area = scrolledtext.ScrolledText(self.main_pane, wrap="word", undo=True, font=("Consolas", 12))
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind("<KeyRelease>", self.highlight_syntax)

        self.main_pane.add(self.folder_frame)
        self.main_pane.add(self.text_area)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Theme Menu
        theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        theme_menu.add_command(label="Light Mode", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.change_theme("dark"))
        self.menu_bar.add_cascade(label="Theme", menu=theme_menu)

    def highlight_syntax(self, event=None):
        text = self.text_area.get("1.0", "end-1c")
        self.text_area.tag_remove("keyword", "1.0", tk.END)
        
        lexer = PythonLexer()
        tokens = lex(text, lexer)

        for token_type, value in tokens:
            if "Keyword" in str(token_type):
                start_index = self.text_area.search(value, "1.0", stopindex=tk.END)
                if start_index:
                    end_index = f"{start_index}+{len(value)}c"
                    self.text_area.tag_add("keyword", start_index, end_index)

        self.text_area.tag_config("keyword", foreground="blue")

    def change_theme(self, theme):
        self.theme = theme
        if theme == "dark":
            self.text_area.config(bg="#2d2d2d", fg="#ffffff", insertbackground="white")
            self.folder_frame.config(bg="#1e1e1e")
            self.folder_tree.config(bg="#1e1e1e", fg="white")
        else:
            self.text_area.config(bg="white", fg="black", insertbackground="black")
            self.folder_frame.config(bg="#f0f0f0")
            self.folder_tree.config(bg="white", fg="black")

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Python Files", "*.py"), ("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", file.read())
            self.file_path = file_path

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))
            self.file_path = file_path

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_tree.delete(*self.folder_tree.get_children())  # Clear previous items
            self.populate_tree(folder_path, "")

    def populate_tree(self, directory, parent):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            is_folder = os.path.isdir(item_path)
            node = self.folder_tree.insert(parent, "end", text=item, open=False)
            if is_folder:
                self.populate_tree(item_path, node)

    def open_file_from_tree(self, event):
        selected_item = self.folder_tree.selection()
        if selected_item:
            file_name = self.folder_tree.item(selected_item, "text")
            file_path = os.path.join(os.getcwd(), file_name)
            if os.path.isfile(file_path):
                self.open_file(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    editor = MyEditor(root)
    root.mainloop()
