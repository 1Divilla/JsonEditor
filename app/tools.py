# %% imports
import json
import os
# local
import entry_popup as ep

# %% Code

def insert_items(treeview, parent, data):
    if isinstance(data, dict):
        for key, value in data.items():
            node = treeview.insert(parent, "end", text=key, values=(str(value) if not isinstance(value, (dict, list)) else ""))
            if isinstance(value, (dict, list)):
                insert_items(treeview, node, value)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            node = treeview.insert(parent, "end", text=f"[{index}]", values=(str(item) if not isinstance(item, (dict, list)) else ""))
            if isinstance(item, (dict, list)):
                insert_items(treeview, node, item)
            
def on_principal_resize(self, event):
    write_config_file("principal_frame", self.principal_frame.sash_coord(0)[0])
    
def on_right_paned_resize(self, event):
    write_config_file("top_table", self.top_table.winfo_height())
    
def read_config_file(variable):
    project_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    config_file_path = os.path.join(project_dir, 'config.json')
    
    try:
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            
            if variable in config_data:
                return config_data[variable]
            else:
                print(f"Error: The key '{variable}' is not found in the configuration file.")
                return None
    except FileNotFoundError:
        print(f"Error: The configuration file was not found at {config_file_path}.")
        return None
    except json.JSONDecodeError:
        print("Error: The configuration file is not a valid JSON.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    
def show_content_file(self, event):
    # select table
    if read_config_file("current_table") == "top":
        table = self.top_table
    elif read_config_file("current_table") == "bottom":
        table = self.bottom_table
        
    # delete table
    table.delete(*table.get_children())

    selected_items = self.treeview.selection()
    
    # get selected name
    for item in selected_items:
        item_data = self.treeview.item(item)
        selected_item = item_data.get("text")
        print(f"selected item: {selected_item}")

    try:
        # load file
        with open(read_config_file("path"), 'r') as file:
            data_file = json.load(file)

            def find_key_all(data, key):
                if isinstance(data, dict):
                    if key in data:
                        return data[key]
                    for k, v in data.items():
                        result = find_key_all(v, key)
                        if result is not None:
                            return result
                elif isinstance(data, list):
                    for item in data:
                        result = find_key_all(item, key)
                        if result is not None:
                            return result
                return None

            # get content selected name
            selected_data = find_key_all(data_file, selected_item)
            print(selected_data)
            if selected_data is None:
                print(f"Error: The key '{selected_item}' is not found in the JSON.")
                return

            table["columns"] = ("Name", "Value", "Type")
            table.heading("#0", text="", anchor="w")
            table.heading("Name", text="Name", anchor="w")
            table.heading("Value", text="Value", anchor="w")
            table.heading("Type", text="Type", anchor="w")
            table.column("#0", width=0, stretch=False)
            table.column("Name", anchor="w")
            table.column("Value", anchor="w")
            table.column("Type", anchor="w")

            # Función recursiva para extraer todos los elementos descendientes
            def process_items(key, value):
                value_type = type(value).__name__
                display_value = str(value)
                return (key, display_value, value_type)

            def insert_all_items(parent, data, parent_key=""):
                if isinstance(data, dict):
                    for k, v in data.items():
                        full_key = f"{parent_key}.{k}" if parent_key else k
                        if isinstance(v, (dict, list)):
                            insert_all_items(parent, v, full_key)
                        else:
                            name, value, value_type = process_items(full_key, v)
                            table.insert(parent, "end", text="", values=(name, value, value_type))
                elif isinstance(data, list):
                    for index, item in enumerate(data):
                        full_key = f"{parent_key}[{index}]"
                        if isinstance(item, (dict, list)):
                            insert_all_items(parent, item, full_key)
                        else:
                            name, value, value_type = process_items(full_key, item)
                            table.insert(parent, "end", text="", values=(name, value, value_type))
                else:  # Caso cuando el valor no es ni un diccionario ni una lista
                    name, value, value_type = process_items(parent_key, data)
                    table.insert(parent, "end", text="", values=(name, value, value_type))

            # Insertar el nodo seleccionado y todos los niveles inferiores
            insert_all_items("", selected_data)

            print("Datos insertados con éxito.")

    except Exception as e:
        print(f"Unexpected error: {e}")
def update_treeview(treeview, file_path, data):
    for item in treeview.get_children():
        treeview.delete(item)
        
    treeview.heading("#0", text=os.path.basename(file_path), anchor="w")
    
    insert_items(treeview, "", data)
                
def write_config_file(variable, value):
    project_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    config_file_path = os.path.join(project_dir, 'config.json')
    
    try:
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as config_file:
                config_data = json.load(config_file)
        else:
            config_data = {}
        
        config_data[variable] = value
        
        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        print(f"The value of '{variable}' has been updated to '{value}'.")
    
    except FileNotFoundError:
        print(f"Error: The configuration file was not found at {config_file_path}.")
    except json.JSONDecodeError:
        print("Error: The configuration file is not a valid JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")