# %% imports
from tkinter import filedialog, messagebox
import json
# local


# %% Code
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=(("All Files", "*.*"),
                  ("Text Files", "*.txt"), 
                  ("JSON Files", "*.json"), 
                  ("Saved Files", "*.sav"),
                  )
    )

    if file_path:
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r') as file:
                    data_json = json.load(file)
                    print("JSON file content:", json.dumps(data_json, indent=4))
                    return data_json
            elif file_path.endswith('.sav'):
                with open(file_path, 'rb') as file:
                    data_sav = file.read()
                    data_sav = data_sav.decode('utf-8').replace('\r\n', '\n')
                    data_sav = json.loads(data_sav)
                    print("Parsed .sav file content:", json.dumps(data_sav, indent=4))
                    return data_sav
            else:
                with open(file_path, 'r') as file:
                    data_txt = file.read()
                    print("Text file content:", data_txt)
                    return data_txt
        except FileNotFoundError:
            messagebox.showerror("Error", f"The file {file_path} was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"The file {file_path} is not a valid JSON file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file: {e}")