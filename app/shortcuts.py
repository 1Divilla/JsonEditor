# %% imports
from tkinter import filedialog, messagebox
import json
# local


# %% Code
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )

    if file_path:
        try:
            # Abrir el archivo como JSON
            with open(file_path, 'r') as file:
                data_json = json.load(file)
                print("JSON file content:", json.dumps(data_json, indent=4))
                return data_json
        except FileNotFoundError:
            messagebox.showerror("Error", f"The file {file_path} was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"The file {file_path} is not a valid JSON file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file:\n\n{e}")

