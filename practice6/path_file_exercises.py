import os
import shutil
import string

# 1. List only directories, only files, and all items
path = "Practice6"

if os.path.exists(path):
    print("Directories:")
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            print(item)

    print("\nFiles:")
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            print(item)

    print("\nAll items:")
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            print("Directory:", os.path.join(root, directory))
        for filename in files:
            print("File:", os.path.join(root, filename))
else:
    print("Path does not exist.")

# 2. Check access to a path
path = "Practice6"

print("\nAccess checks:")
print("Exists:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))

# 3. Check path and find filename and directory
path = "Practice6/file_handling/read_files.py"

if os.path.exists(path):
    print("\nFilename:", os.path.basename(path))
    print("Directory:", os.path.dirname(path))
else:
    print("\nPath does not exist:", path)

# 4. Count lines in a text file
filename = "Practice6/count.txt"

with open(filename, "w", encoding="utf-8") as file:
    file.write("First line\nSecond line\nThird line\n")

with open(filename, "r", encoding="utf-8") as file:
    print("\nNumber of lines:", sum(1 for line in file))

# 5. Write a list to a file
items = ["Apple", "Banana", "Orange"]

with open("Practice6/fruits.txt", "w", encoding="utf-8") as file:
    for item in items:
        file.write(item + "\n")

print("List written to file.")

# 6. Generate 26 files from A.txt to Z.txt
letters_folder = "Practice6/letters"
os.makedirs(letters_folder, exist_ok=True)

for letter in string.ascii_uppercase:
    filename = os.path.join(letters_folder, letter + ".txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write("This is " + letter + ".txt")

print("26 files created.")

# 7. Copy the contents of one file to another
source = "Practice6/fruits.txt"
destination = "Practice6/fruits_copy.txt"

with open(source, "r", encoding="utf-8") as src:
    content = src.read()

with open(destination, "w", encoding="utf-8") as dest:
    dest.write(content)

print("File contents copied.")

# 8. Safely delete a file by path
file_path = "Practice6/fruits_copy.txt"

if os.path.isfile(file_path):
    if os.access(file_path, os.W_OK):
        try:
            os.remove(file_path)
            print("File deleted successfully.")
        except OSError as error:
            print("Could not delete file:", error)
    else:
        print("File is not writable.")
else:
    print("File does not exist or is not a regular file.")