# Reading a file
with open("example.txt", "r") as file:
    # Read the entire file
    content = file.read()
    
    # Read line by line
    file.seek(0) # Go back to start of file
    lines = file.readlines() # Returns list of lines
    
    # Read line by line using a loop
    file.seek(0)
    for line in file:
        print(line.strip())
        
# Writing to a file
with open("output.txt", "w") as file:  # This will overwrite any existing content
    file.write("Hello world!\n")
    file.write("Another line!\n")
    
# Appending to a file
with open("output.txt", "a") as file:
    file.write("This line is appended\n")
    
# 'r' - Read (default)
# 'w' - Write (overwrites)
# 'a' - Append
# 'x' - Exclusive creation
# 'b' - Binary mode
# 't' - Text mode (default)
# '+' - Read and write mode (can be combined with 'r', 'w', or 'a')
# Examples:
# 'r+' - Read and write, starting at beginning
# 'w+' - Read and write, overwriting file
# 'a+' - Read and write, appending to file

# Working with CSV files
import csv

with open("data.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
        
data = [
    ["Name", "Age", "City"],
    ["Alice", "25", "London"],
    ["Bob", "30", "Paris"]
]
with open("output.csv", "w", newline="") as file:  # newline="" prevents extra blank lines between rows when writing CSV files
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)
    
# Working with JSON files
import json

with open("data.json", "r") as file:
    data = json.load(file)
    
json_data = {"name": "Alice", "age": 25}
with open("output.json", "w") as file:
    json.dump(json_data, file, indent=4)
    
# Error handling with files
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Permission denied!")
    
# Context Managers (with statement)
# The 'with' statement ensures file is properly closed
# even if an error occurs