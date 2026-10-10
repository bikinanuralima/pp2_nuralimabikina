
# 1. Create a text file and write sample data
with open("sample.txt", "w", encoding="utf-8") as file:
    file.write("Alice\n")
    file.write("Bob\n")
    file.write("Charlie\n")

print("File created successfully!")

# 2. Append new lines
with open("sample.txt", "a", encoding="utf-8") as file:
    file.write("David\n")
    file.write("Emma\n")

# 3. Write a list to a file
students = ["John", "Kate", "Michael"]

with open("students.txt", "w", encoding="utf-8") as file:
    for student in students:
        file.write(student + "\n")

print("Data written successfully!")