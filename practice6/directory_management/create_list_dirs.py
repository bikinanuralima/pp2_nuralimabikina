
import os

# 1. Create nested directories
os.makedirs("Practice6/data/input", exist_ok=True)
print("Directories created!")

# 2. List all items in a directory
path = "Practice6"

print("\nAll items:")
print(os.listdir(path))

# 3. List only directories
print("\nDirectories:")
for item in os.listdir(path):
    full_path = os.path.join(path, item)
    if os.path.isdir(full_path):
        print(item)

# 4. List only files
print("\nFiles:")
for item in os.listdir(path):
    full_path = os.path.join(path, item)
    if os.path.isfile(full_path):
        print(item)

# 5. List all files and folders recursively
print("\nAll directories and files:")
for root, dirs, files in os.walk(path):
    print("Directory:", root)
    print("Subdirectories:", dirs)
    print("Files:", files)