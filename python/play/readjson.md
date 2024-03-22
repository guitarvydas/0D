Sure, here's an example of Python code that reads a JSON file and converts its contents into an internal data structure:

```python
import json

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
filename = 'example.json'
result = read_and_convert_json_file(filename)
if result is not None:
    print("Data structure:", result)
```

In this code:

- The `read_and_convert_json_file` function takes the filename as input, opens the file in read mode, reads its contents, and then uses `json.loads()` to convert the JSON data into a Python data structure.
- It handles two exceptions: `FileNotFoundError` in case the file is not found, and `json.JSONDecodeError` in case there's an error while decoding the JSON data.
- The example usage section demonstrates how to use this function by specifying the filename of the JSON file. If the file is successfully read and parsed, it prints the resulting data structure. Otherwise, it prints an appropriate error message.

---

You can use the `os.path` module in Python to extract the base filename from a path string. Here's how you can do it:

```python
import os

def get_base_filename(filepath):
    base_filename = os.path.basename(filepath)
    return base_filename

# Example usage
filepath = '/path/to/your/directory/filename.txt'
base_filename = get_base_filename(filepath)
print("Base filename:", base_filename)
```

This code will extract the base filename from the `filepath` provided. The `os.path.basename()` function extracts the filename component from the path and returns it. So, if `filepath` is `'/path/to/your/directory/filename.txt'`, the output will be `'filename.txt'`.
