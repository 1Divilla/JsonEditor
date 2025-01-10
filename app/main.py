# %% imports
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# Configurar la apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Crear la ventana principal
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JsonEditor")
        self.after(10, self.center_window)
        
        self.create_menu()
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_menu(self):
        # create menu
        menu_bar = tk.Menu(self)
    
        # file
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", accelerator="Ctrl+O")
        file_menu.add_command(label="Save", accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Close", accelerator="Ctrl+Q")
    
        # edit
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Toggle Treeview", accelerator="X")
    
        # view
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_command(label="Full Screen", accelerator="F11")
        
        # help
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", accelerator="Ctrl+H")
        help_menu.add_command(label="About", accelerator="F1")
    
        # set in window
        self.config(menu=menu_bar)

    def create_widgets(self):
        # create principal_frame
        principal_frame = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        principal_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ffile Explorer
        treeview = ttk.Treeview(principal_frame)
        treeview.heading("#0", text="File Explorer", anchor="w")
        root_node = treeview.insert("", "end", text="Project", open=True)
        treeview.insert(root_node, "end", text="file1.json")
        treeview.insert(root_node, "end", text="file2.json")
        
        principal_frame.add(treeview, minsize=200)
        
        # tables
        right_paned = tk.PanedWindow(principal_frame, orient=tk.VERTICAL)
        
        # top Table
        top_table = ttk.Treeview(right_paned, columns=("Column 1", "Column 2"), show="headings")
        top_table.heading("Column 1", text="Column 1")
        top_table.heading("Column 2", text="Column 2")
        top_table.insert("", "end", values=("Row 1", "Value 1"))
        top_table.insert("", "end", values=("Row 2", "Value 2"))
        right_paned.add(top_table, minsize=200)
        
        # bottom Table
        bottom_table = ttk.Treeview(right_paned, columns=("Column A", "Column B"), show="headings")
        bottom_table.heading("Column A", text="Column A")
        bottom_table.heading("Column B", text="Column B")
        bottom_table.insert("", "end", values=("Item 1", "Data A"))
        bottom_table.insert("", "end", values=("Item 2", "Data B"))
        right_paned.add(bottom_table, minsize=200)
        
        # add right_paned to principal_frame
        principal_frame.add(right_paned, minsize=200)


# %% Execute
if __name__ == "__main__":
    app = App()
    app.mainloop()
