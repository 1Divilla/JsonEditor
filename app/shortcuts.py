# %% imports
from tkinter import filedialog, messagebox
import json
import os
# local
import tools as tls

# %% Code
def open_file(treeview):
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )

    if file_path:
        try:
            with open(file_path, 'r') as file:
                data_json = json.load(file)
                
                # Save data in config.json
                tls.write_config_file("path", file_path)
                tls.write_config_file("data_file", data_json)

                # Actualizar el encabezado y limpiar el treeview
                tls.update_treeview(treeview, file_path, data_json)

        except FileNotFoundError:
            messagebox.showerror("Error", f"The file {file_path} was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"The file {file_path} is not a valid JSON file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file:\n\n{e}")
    else:
        messagebox.showerror("Error", "No file selected. Please select a valid JSON file.")
            
def toggle_fullscreen(self):
    self.state('normal' if self.attributes("-fullscreen") else 'zoomed')
    current_state = self.attributes("-fullscreen")
    self.attributes("-fullscreen", not current_state)
    
def reset_view(self):
    if tls.read_config_file("principal_frame") != 250:
        tls.write_config_file("principal_frame", 250)
        self.principal_frame.paneconfig(self.file_explorer_frame, width=250)

    if tls.read_config_file("top_table") != 1229:
        tls.write_config_file("top_table", 1229)
        self.right_paned.paneconfig(self.top_table, height=1229)

    if tls.read_config_file("font_size") != 12:
        tls.write_config_file("font_size", 12)

    self.update_idletasks()

def save_as(name, content):
    try:
        type_file = f".{name.split('.')[-1]}" if '.' in name else ".json"
        
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=type_file,
            initialfile=name,
            filetypes=[
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

    except Exception as e:
        messagebox.showerror("Save As JSON Error", f"An error occurred while saving:\n{e}")
        
def toggle_treeview():
    if tls.read_config_file("current_table") == "top":
        tls.write_config_file("current_table", "bottom")
    
    elif tls.read_config_file("current_table") == "bottom":
        tls.write_config_file("current_table", "top")
                
def zoom_in():
    if tls.read_config_file("font_size")<32:
        tls.write_config_file("font_size", tls.read_config_file("font_size")+1)
        
def zoom_out():
    if tls.read_config_file("font_size")>6:
        tls.write_config_file("font_size", tls.read_config_file("font_size")-1)