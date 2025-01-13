# %% imports
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
# local
import shortcuts as st

# %% Code
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JsonEditor")
        self.minsize(1040, 600)
        self.geometry("1040x600")
        self.after(40, self.center_window(1040, 600))
        
        self.create_menu()
        self.shortcuts()
        self.create_widgets()
        
    def center_window(self, w, h):
        """Center the window on the screen."""
        self.update_idletasks()
        
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        
    def create_menu(self):
        # create menu
        menu_bar = tk.Menu(self)
    
        # file
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command= lambda: st.open_file())
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
        edit_menu.add_command(label="Toggle Treeview", accelerator="Alt+T")
    
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
        
        # File Explorer with Entry
        file_explorer_frame = tk.Frame(principal_frame)
        file_explorer_entry = tk.Entry(file_explorer_frame)
        file_explorer_entry.pack(fill=tk.X, pady=(2, 4))
        
        treeview = ttk.Treeview(file_explorer_frame)
        treeview.heading("#0", text="File Explorer", anchor="w")
        root_node = treeview.insert("", "end", text="Project", open=True)
        treeview.insert(root_node, "end", text="file1.json")
        treeview.insert(root_node, "end", text="file2.json")
        treeview.pack(fill=tk.BOTH, expand=True)
        
        file_explorer_frame.pack(fill=tk.BOTH, expand=True)
        principal_frame.add(file_explorer_frame, width=170, minsize=170)
        
        # tables
        right_paned = tk.PanedWindow(principal_frame, orient=tk.VERTICAL)
        
        # top Table
        top_table = ttk.Treeview(right_paned, columns=("Column 1", "Column 2"), show="headings")
        top_table.heading("Column 1", text="Column 1")
        top_table.heading("Column 2", text="Column 2")
        top_table.column("Column 1", width=100, stretch=False)
        top_table.column("Column 2", width=150, stretch=False)
        top_table.insert("", "end", values=("Row 1", "Value 1"))
        top_table.insert("", "end", values=("Row 2", "Value 2"))
        right_paned.add(top_table, height=400, minsize=150)
        
        # bottom Table
        bottom_table = ttk.Treeview(right_paned, columns=("Column A", "Column B"), show="headings")
        bottom_table.heading("Column A", text="Column A")
        bottom_table.heading("Column B", text="Column B")
        bottom_table.column("Column A", width=120, stretch=False)
        bottom_table.column("Column B", width=180, stretch=False)
        bottom_table.insert("", "end", values=("Item 1", "Data A"))
        bottom_table.insert("", "end", values=("Item 2", "Data B"))
        right_paned.add(bottom_table, minsize=150)
        
        # add right_paned to principal_frame
        principal_frame.add(right_paned, minsize=150)
        
    
    def shortcuts(self):
        # File shortcuts
        self.bind("<Control-o>", lambda event: st.open_file())
        self.bind("<Control-O>", lambda event: st.open_file())
        self.bind("<Control-s>", lambda event: print("Save file m"))
        self.bind("<Control-S>", lambda event: print("Save file M"))
        self.bind("<Control-Shift-s>", lambda event: print("Save file as"))
        self.bind("<Control-Shift-S>", lambda event: print("Save file as"))
        self.bind("<Control-q>", lambda event: self.destroy())
        self.bind("<Control-Q>", lambda event: self.destroy())
        
        # Edit shortcuts
        self.bind("<Control-z>", lambda event: print("Undo action"))
        self.bind("<Control-Z>", lambda event: print("Undo action"))
        self.bind("<Control-y>", lambda event: print("Redo action"))
        self.bind("<Control-Y>", lambda event: print("Redo action"))
        self.bind("<Alt-t>", lambda event: print("Toggle Treeview"))
        self.bind("<Alt-T>", lambda event: print("Toggle Treeview"))
        
        # View shortcuts
        self.bind("<Control-plus>", lambda event: print("Zoom in"))
        self.bind("<Control-minus>", lambda event: print("Zoom out"))
        self.bind("<Control-0>", lambda event: print("Reset zoom"))
        self.bind("<F11>", lambda event: print("Toggle full screen"))
        
        # Help shortcuts
        self.bind("<Control-h>", lambda event: print("Open documentation"))
        self.bind("<Control-H>", lambda event: print("Open documentation"))
        self.bind("<F1>", lambda event: print("About application"))
        
        # Window info
        self.bind("<Control-i>", lambda event: self.window_info())
        self.bind("<Control-I>", lambda event: self.window_info())
        
    def window_info(self):
        # Tamaño de la ventana
        width = self.winfo_width()
        height = self.winfo_height()
    
        # Posición de la ventana
        x = self.winfo_x()
        y = self.winfo_y()
    
        # Estado de la ventana
        state = self.state()  # 'normal', 'iconic', 'withdrawn'
    
        # Información de la geometría
        geometry = self.geometry()
    
        # Información de pantalla completa
        fullscreen = "Yes" if self.attributes("-fullscreen") else "No"
        
        # Imprimir la información
        print(f"Información de la ventana:")
        print(f"  Tamaño: {width}x{height}")
        print(f"  Posición: ({x}, {y})")
        print(f"  Estado: {state}")
        print(f"  Geometría: {geometry}")
        print(f"  Pantalla completa: {fullscreen}")

# %% Execute
if __name__ == "__main__":
    app = App()
    app.mainloop()
