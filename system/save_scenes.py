# This script reads a JSON object as text from standard input,
# and when the object is complete via the closing brace, it finds the "abbrev" field,
# using that value as a filename to save the object. The script loops until stdin is closed.
# Save these instructions as a comment in the script.

import json
import sys

def save_json_object(json_text):
    try:
        # Load the JSON object from the text
        json_object = json.loads(json_text)
        
        # Retrieve the "abbrev" field to use as filename
        filename = json_object.get("abbrev", "default") + ".json"
        
        # Save the JSON object to a file
        with open(filename, 'w') as file:
            json.dump(json_object, file, indent=4)
        
        print(f"JSON object saved as {filename}")
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    json_buffer = ""
    brace_balance = 0

    print("Please input your JSON objects:")

    while True:
        try:
            line = input()
            json_buffer += line
            
            # Count the opening and closing braces to ensure the object is complete
            brace_balance += line.count('{') - line.count('}')
            
            # Check if the JSON object is complete
            if brace_balance == 0 and json_buffer.strip().endswith('}'):
                save_json_object(json_buffer)
                json_buffer = ""
                
        except EOFError:
            if json_buffer.strip():
                save_json_object(json_buffer)
            break

