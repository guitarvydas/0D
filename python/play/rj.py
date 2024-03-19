import json
import os

def read_and_convert_json_file(filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            data_structure = json.loads(json_data)
            return data_structure
    except FileNotFoundError:
        print("File not found:", filename)
        return None
    except json.JSONDecodeError as e:
        print("Error decoding JSON in file:", e)
        return None

# Example usage
pathname = '../../../helloworld0d/helloworld0d.drawio.json'
filename = os.path.basename (pathname)
print (filename)
result = read_and_convert_json_file(filename)
if result is not None:
    print("Data structure:", result)
