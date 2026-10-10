
import os
import shutil

source = "sample.txt"
copy_file = "sample_copy.txt"
backup_file = "sample_backup.txt"

# Copy a file
if os.path.isfile(source):
    shutil.copy(source, copy_file)
    shutil.copy2(source, backup_file)
    print("Copy and backup created!")

# Safely delete a file
file_to_delete = "sample_copy.txt"

if os.path.isfile(file_to_delete) and os.access(file_to_delete, os.W_OK):
    os.remove(file_to_delete)
    print("File deleted successfully!")
else:
    print("File does not exist or cannot be deleted.")

print("Backup is preserved.")