# %% imports
import json
import os
# local
import entry_popup as ep

# %% Code
def delete_entrypopup(self):
    # Check if an EntryPopup exists and destroy it
    if hasattr(self, 'entry_popup') and self.entry_popup:
        try:
            self.entry_popup.destroy()
            self.entry_popup = None
        except Exception as e:
            print(f"Error destroying popup: {e}")

def insert_items(treeview, parent, data):
    # Insert dictionary or list items into the Treeview
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

def on_column_resize(self, table):
    delete_entrypopup(self)
    
    # Initialize previous column widths
    if not hasattr(self, 'prev_column_widths'):
        self.prev_column_widths = {col: table.column(col)["width"] for col in table["columns"]}
        return

    # Check for changes in column widths and update tracking
    for col in table["columns"]:
        try:
            current_width = table.column(col)["width"]
            prev_width = self.prev_column_widths.get(col)

            if current_width != prev_width:
                self.prev_column_widths[col] = current_width
        except Exception as e:
            print(f"Error checking column '{col}': {e}")

def on_double_click(self, event, table):
    delete_entrypopup(self)

    row = table.identify_row(event.y)
    column = table.identify_column(event.x)

    if not row:
        return

    column_index = int(column[1:]) - 1
    # Prevent editing of the "Name" and "Type" columns (indexes 0 and 2)
    if column_index in (0, 2):
        return

    # Get bounding box of the selected cell
    bbox = table.bbox(row, column_index)
    if not bbox:
        return

    x, y, width, height = bbox
    pady = height // 8

    value = table.item(row, 'values')[column_index]

    self.entry_popup = ep.EntryPopup(self, table, row, column_index, value)
    self.entry_popup.place(x=x, y=y, width=width, height=height, anchor='nw')
    
    # Calculate absolute position for the popup
    abs_x = table.winfo_rootx() - self.winfo_rootx() + x
    abs_y = table.winfo_rooty() - self.winfo_rooty() + y

    self.entry_popup.place(
        x=abs_x,
        y=abs_y,
        width=width,
        height=height,
        anchor='nw'
    )
            
def on_principal_resize(self, event):
    delete_entrypopup(self)

    max_column_width = int(self.winfo_width() * 0.8)
    
    # Limit the maximum width of columns
    for col in ["Name", "Value", "Type"]:
        current_width = self.top_table.column(col, "width")
        new_width = min(current_width, max_column_width)
        self.top_table.column(col, width=new_width, minwidth=100, stretch=True)
        
        current_width_bottom = self.bottom_table.column(col, "width")
        new_width_bottom = min(current_width_bottom, max_column_width)
        self.bottom_table.column(col, width=new_width_bottom, minwidth=100, stretch=True)
    
    # Update main configuration
    write_config_file("principal_frame", self.principal_frame.sash_coord(0)[0])
    
def on_right_paned_resize(self, event):
    delete_entrypopup(self)

    write_config_file("top_table", self.top_table.winfo_height())

def on_table_click(self, event, table):
    def handle_click():
        item = table.identify_row(event.y)

        if not hasattr(table, "last_selected_item"):
            table.last_selected_item = ""

        if item:
            if item != table.last_selected_item:
                table.last_selected_item = item
                delete_entrypopup(self)
        else:
            table.selection_remove(*table.selection())

    table.after(1, handle_click)

def on_window_resize(self, event):
    current_w, current_h = self.winfo_width(), self.winfo_height()
    
    if not hasattr(self, 'prev_size'):
        self.prev_size = {'w': current_w, 'h': current_h}
    
    if current_w != self.prev_size['w'] or current_h != self.prev_size['h']:
        if hasattr(self, 'entry_popup') and self.entry_popup:
            try:
                self.entry_popup.destroy()
                self.entry_popup = None
            except Exception as e:
                print(f"Error al destruir popup: {e}")
        
        # Actualizar tamaño previo
        self.prev_size = {'w': current_w, 'h': current_h}

def read_config_file(variable):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(current_dir, '..'))
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
    
    delete_entrypopup(self)

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

            # store maximum lengths
            max_lengths = {"Name": len("Name"), "Value": len("Value")}

            # function to calculate the length of values
            def process_items(key, value):
                value_type = type(value).__name__
                display_value = str(value)
                
                # update maximum length
                max_lengths["Name"] = max(max_lengths["Name"], len(key))
                max_lengths["Value"] = max(max_lengths["Value"], len(display_value))

                return key, display_value, value_type

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
                else:  # case when the value is neither a dictionary nor a list
                    name, value, value_type = process_items(parent_key, data)
                    table.insert(parent, "end", text="", values=(name, value, value_type))

            # insert the selected node and all lower levels
            insert_all_items("", selected_data)

            table.column("Name", width=(max_lengths["Name"] * 2), minwidth=100, stretch=True)
            table.column("Value", width=(max_lengths["Value"] * 8), minwidth=100, stretch=True)
            table.column("Type", width=1, minwidth=100, stretch=True)

            table.update_idletasks()

    except Exception as e:
        print(f"Unexpected error: {e}")
       
def update_treeview(treeview, file_path, data):
    for item in treeview.get_children():
        treeview.delete(item)
        
    treeview.heading("#0", text=os.path.basename(file_path), anchor="w")
    
    insert_items(treeview, "", data)
                
def write_config_file(variable, value):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(current_dir, '..'))
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