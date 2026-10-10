import os

path = "Practice6"
extension = ".py"

print("Files with extension", extension)

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(extension):
            print(os.path.join(root, file))