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
        
        self.protocol("WM_DELETE_WINDOW", lambda: st.close(self))

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
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command= lambda: st.save())
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command= lambda: st.save_as())
        file_menu.add_separator()
        file_menu.add_command(label="Close", accelerator="Ctrl+Q", command= lambda: st.close(self))

    
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
        # Principal Frame
        self.principal_frame = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.principal_frame.pack(fill=tk.BOTH, expand=True)

        # File Explorer Panel (Left)
        self.file_explorer_frame = tk.Frame(self.principal_frame)

        # Treeview and scrollbar
        tree_scrollbar = ttk.Scrollbar(self.file_explorer_frame, orient="vertical")
        tree_scrollbar.pack(side="left", fill="y")
        self.treeview = ttk.Treeview(
            self.file_explorer_frame,
            yscrollcommand=tree_scrollbar.set
        )
        self.treeview.pack(side="left", fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.treeview.yview)
        self.file_explorer_frame.pack(fill=tk.BOTH, expand=True)
        self.principal_frame.add(
            self.file_explorer_frame,
            width=tls.read_config_file("principal_frame"),
            minsize=170
        )

        # Right Panel
        self.right_paned = tk.PanedWindow(self.principal_frame, orient=tk.VERTICAL)

        # Top Table
        self.top_table_frame = tk.Frame(self.right_paned)

        top_scrollbar = ttk.Scrollbar(self.top_table_frame, orient="vertical")
        self.top_table = ttk.Treeview(
            self.top_table_frame,
            columns=("Name", "Value", "Type"),
            show="headings",
            yscrollcommand=top_scrollbar.set
        )
        top_scrollbar.config(command=self.top_table.yview)

        self.top_table.heading("Name", text="Name", anchor="w")
        self.top_table.column("Name", minwidth=100, stretch=True)
        self.top_table.heading("Value", text="Value", anchor="w")
        self.top_table.column("Value", minwidth=100, stretch=True)
        self.top_table.heading("Type", text="Type", anchor="w")
        self.top_table.column("Type", minwidth=100, stretch=True)

        self.top_table.pack(side="left", fill=tk.BOTH, expand=True)
        top_scrollbar.pack(side="right", fill="y")

        self.right_paned.add(
            self.top_table_frame,
            height=tls.read_config_file("top_table"),
            minsize=150
        )

        # Bottom Table
        bottom_table_frame = tk.Frame(self.right_paned)

        bottom_scrollbar = ttk.Scrollbar(bottom_table_frame, orient="vertical")
        self.bottom_table = ttk.Treeview(
            bottom_table_frame,
            columns=("Name", "Value", "Type"),
            show="headings",
            yscrollcommand=bottom_scrollbar.set
        )
        bottom_scrollbar.config(command=self.bottom_table.yview)

        self.bottom_table.heading("Name", text="Name", anchor="w")
        self.bottom_table.column("Name", minwidth=70, stretch=True)
        self.bottom_table.heading("Value", text="Value", anchor="w")
        self.bottom_table.column("Value", minwidth=70, stretch=True)
        self.bottom_table.heading("Type", text="Type", anchor="w")
        self.bottom_table.column("Type", minwidth=70, stretch=True)

        self.bottom_table.pack(side="left", fill=tk.BOTH, expand=True)
        bottom_scrollbar.pack(side="right", fill="y")

        self.right_paned.add(bottom_table_frame, minsize=150)

        # Add right panel to principal frame
        self.principal_frame.add(self.right_paned, minsize=250)
        
    def binds(self):
        # File shortcuts
        self.bind("<Control-o>", lambda event: st.open_file(self.treeview))
        self.bind("<Control-O>", lambda event: st.open_file(self.treeview))
        self.bind("<Control-s>", lambda event: st.save())
        self.bind("<Control-S>", lambda event: st.save())
        self.bind("<Control-Shift-s>", lambda event: st.save_as())
        self.bind("<Control-Shift-S>", lambda event: st.save_as())   
        self.bind("<Control-q>", lambda event: st.close(self))
        self.bind("<Control-Q>", lambda event: st.close(self))
        
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
        self.top_table.bind("<Button-1>", lambda event: tls.on_table_click(self, event, self.top_table))
        self.bottom_table.bind("<Button-1>", lambda event: tls.on_table_click(self, event, self.bottom_table))   

# %% Execute
if __name__ == "__main__":
    app = App()
    app.mainloop()
