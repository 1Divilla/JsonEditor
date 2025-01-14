# %% imports
import json
import os
# local

# %% Code

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