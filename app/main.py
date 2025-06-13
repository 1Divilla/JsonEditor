# %% Imports
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
# Local
import shortcuts as st
import tools as tls

# %% Code
class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("JsonEditor")
        self.minsize(520, 300)
        self.geometry("1040x600")
        self.center_window(1040, 600)
        
        self.create_widgets() 
        self.create_menu()
        self.binds()
        
        tls.update_treeview(self.treeview, tls.read_config_file("path"), tls.read_config_file("data_file"))
        
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
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command= lambda: st.open_file(self.treeview))
        file_menu.add_command(label="Save", accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command= lambda: st.save_as("sadasd.json", ".txt"))
        file_menu.add_separator()
        file_menu.add_command(label="Close", accelerator="Ctrl+Q", command= lambda: self.destroy())
    
        # edit
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Toggle Table", accelerator="Alt+T", command= lambda: st.toggle_treeview())
    
        # view
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", accelerator="Ctrl++", command= lambda: st.zoom_in())
        view_menu.add_command(label="Zoom Out", accelerator="Ctrl+-", command= lambda: st.zoom_out())
        view_menu.add_command(label="Reset View", accelerator="Ctrl+0", command= lambda: st.reset_view(self))
        view_menu.add_separator()
        view_menu.add_command(label="Full Screen", accelerator="F11", command= lambda: st.toggle_fullscreen(self))
        
        # help
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", accelerator="Ctrl+H")
        help_menu.add_command(label="About", accelerator="F1")
    
        # set in window
        self.config(menu=menu_bar)
        
    def create_widgets(self):
        
        # Create principal_frame
        self.principal_frame = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.principal_frame.pack(fill=tk.BOTH, expand=True)
        
        # File Explorer with Entry
        self.file_explorer_frame = tk.Frame(self.principal_frame)
        self.file_explorer_entry = tk.Entry(self.file_explorer_frame)
        self.file_explorer_entry.pack(fill=tk.X, pady=(2, 4))
        
        self.treeview = ttk.Treeview(self.file_explorer_frame)
        self.treeview.pack(fill=tk.BOTH, expand=True)
        
        self.file_explorer_frame.pack(fill=tk.BOTH, expand=True)
        self.principal_frame.add(self.file_explorer_frame, width=tls.read_config_file("principal_frame"), minsize=170)
        
        # tables
        self.right_paned = tk.PanedWindow(self.principal_frame, orient=tk.VERTICAL)
        
        # top Table
        self.top_table = ttk.Treeview(self.right_paned, columns=("Name", "Value", "Type"), show="headings")
        self.top_table.heading("Name", text="Name", anchor="w")
        self.top_table.column("Name", minwidth=100, stretch=True)
        self.top_table.heading("Value", text="Value", anchor="w")
        self.top_table.column("Value", minwidth=100, stretch=True)
        self.top_table.heading("Type", text="Type", anchor="w")
        self.top_table.column("Type", minwidth=100, stretch=True)
        self.right_paned.add(self.top_table, height=tls.read_config_file("top_table"), minsize=150)
        
        # bottom Table
        self.bottom_table = ttk.Treeview(self.right_paned, columns=("Name", "Value", "Type"), show="headings")
        self.bottom_table.heading("Name", text="Name", anchor="w")
        self.bottom_table.column("Name", minwidth=100, stretch=True)
        self.bottom_table.heading("Value", text="Value", anchor="w")
        self.bottom_table.column("Value", minwidth=100, stretch=True)
        self.bottom_table.heading("Type", text="Type", anchor="w")
        self.bottom_table.column("Type", minwidth=100, stretch=True)
        self.right_paned.add(self.bottom_table, minsize=150)
        
        # add right_paned to principal_frame
        self.principal_frame.add(self.right_paned, minsize=150)
        
    def binds(self):
        # File shortcuts
        self.bind("<Control-o>", lambda event: st.open_file(self.treeview))
        self.bind("<Control-O>", lambda event: st.open_file(self.treeview))
        self.bind("<Control-s>", lambda event: print("Save file m"))
        self.bind("<Control-S>", lambda event: print("Save file M"))
        self.bind("<Control-Shift-s>", lambda event: st.save_as("sadasd.json", "asdasd"))
        self.bind("<Control-Shift-S>", lambda event: st.save_as("sadasd.json", "asdasd"))   
        self.bind("<Control-q>", lambda event: self.destroy())
        self.bind("<Control-Q>", lambda event: self.destroy())
        
        # Edit shortcuts
        self.bind("<Control-z>", lambda event: print("Undo action"))
        self.bind("<Control-Z>", lambda event: print("Undo action"))
        self.bind("<Control-y>", lambda event: print("Redo action"))
        self.bind("<Control-Y>", lambda event: print("Redo action"))
        self.bind("<Alt-t>", lambda event: st.toggle_treeview())
        self.bind("<Alt-T>", lambda event:  st.toggle_treeview())
        
        # View shortcuts
        self.bind("<Control-plus>", lambda event: st.zoom_in())
        self.bind("<Control-minus>", lambda event: st.zoom_out())
        self.bind("<Control-0>", lambda event: st.reset_view(self))
        self.bind("<F11>", lambda event: st.toggle_fullscreen(self))
        
        # Help shortcuts
        self.bind("<Control-h>", lambda event: print("Open documentation"))
        self.bind("<Control-H>", lambda event: print("Open documentation"))
        self.bind("<F1>", lambda event: print("About application"))
        
        # Others
        self.principal_frame.bind("<B1-Motion>", lambda event: tls.on_principal_resize(self, event))
        self.right_paned.bind("<B1-Motion>", lambda event: tls.on_right_paned_resize(self, event))
        self.treeview.bind("<<TreeviewOpen>>", lambda event: self.treeview.selection_remove(self.treeview.selection()))
        self.treeview.bind("<<TreeviewClose>>", lambda event: self.treeview.selection_remove(self.treeview.selection()))
        self.treeview.bind("<<TreeviewSelect>>", lambda event: tls.show_content_file(self, event) if self.treeview.selection() else None)
        self.top_table.bind("<Double-1>", lambda event: tls.on_double_click(self, event, self.top_table))
        self.bottom_table.bind("<Double-1>", lambda event: tls.on_double_click(self, event, self.bottom_table))
        self.bind("<Configure>", lambda event: tls.on_window_resize(self, event))
        self.top_table.bind("<B1-Motion>", lambda event: tls.on_column_resize(self, self.top_table))
        self.bottom_table.bind("<B1-Motion>", lambda event: tls.on_column_resize(self, self.bottom_table))

# %% Execute
if __name__ == "__main__":
    app = App()
    app.mainloop()
