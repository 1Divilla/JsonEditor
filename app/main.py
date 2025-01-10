# %% imports
import tkinter as tk
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
        edit_menu.add_command(label="Toggle Treview", accelerator="X")
    
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
    
        # Set in window
        self.config(menu=menu_bar)

#%% Content
    def create_widgets(self):
        print("")
# %% Execute
if __name__ == "__main__":
    app = App()
    app.mainloop()
