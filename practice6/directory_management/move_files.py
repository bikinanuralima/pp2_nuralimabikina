
import os
import shutil

os.makedirs("Practice6/source", exist_ok=True)
os.makedirs("Practice6/destination", exist_ok=True)

source = "Practice6/source/example.txt"
copied = "Practice6/destination/example_copy.txt"
moved = "Practice6/destination/example.txt"

# Create a sample file if it does not exist
with open(source, "w", encoding="utf-8") as file:
    file.write("This is a sample file.")

# Copy the file
shutil.copy2(source, copied)
print("File copied!")

# Move the file
shutil.move(source, moved)
print("File moved!")

print("Destination files:", os.listdir("Practice6/destination"))