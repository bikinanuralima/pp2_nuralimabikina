
# 1. enumerate(): get index and value
students = ["Alice", "Bob", "Charlie"]

for index, student in enumerate(students, start=1):
    print(index, student)

# 2. zip(): combine two lists
names = ["Alice", "Bob", "Charlie"]
grades = [90, 85, 95]

for name, grade in zip(names, grades):
    print(name, ":", grade)

# 3. Convert paired lists into a dictionary
student_grades = dict(zip(names, grades))
print(student_grades)