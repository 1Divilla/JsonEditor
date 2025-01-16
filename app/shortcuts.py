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

                treeview.heading("#0", text=os.path.basename(file_path), anchor="w")

                for item in treeview.get_children():
                    treeview.delete(item)

                def insert_items(parent, d):
                    if isinstance(d, dict):
                        for key, value in d.items():
                            node = treeview.insert(parent, "end", text=key, values=(str(value) if not isinstance(value, (dict, list)) else ""))
                            if isinstance(value, (dict, list)):
                                insert_items(node, value)
                    elif isinstance(d, list):
                        for index, item in enumerate(d):
                            node = treeview.insert(parent, "end", text=f"[{index}]", values=(str(item) if not isinstance(item, (dict, list)) else ""))
                            if isinstance(item, (dict, list)):
                                insert_items(node, item)

                insert_items("", data_json)
        except FileNotFoundError:
            messagebox.showerror("Error", f"The file {file_path} was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"The file {file_path} is not a valid JSON file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file:\n\n{e}")
            


def toggle_fullscreen(app):
    is_fullscreen = app.attributes("-fullscreen")
    app.attributes("-fullscreen", not is_fullscreen)
    button_text = "Salir de Pantalla Completa" if not is_fullscreen else "Pantalla Completa"
    app.toggle_button.config(text=button_text)
    
def reset_view():
    if tls.read_config_file("principal_frame")!=170:
        tls.write_config_file("principal_frame", 170)
    if tls.read_config_file("top_table")!=400:
        tls.write_config_file("top_table", 400)
    if tls.read_config_file("font_size")!=12:
        tls.write_config_file("font_size", 12)

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

            
        
def zoom_in():
    if tls.read_config_file("font_size")<32:
        tls.write_config_file("font_size", tls.read_config_file("font_size")+1)
        
def zoom_out():
    if tls.read_config_file("font_size")>6:
        tls.write_config_file("font_size", tls.read_config_file("font_size")-1)