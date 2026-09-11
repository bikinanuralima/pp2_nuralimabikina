#example1
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"Fruit: {fruit}")
#example2
for char in "Python":
    print(f"Letter: {char}")
#example3
for x in range(1, 6):
    print(f"Number: {x}")
#example4
for even in range(2, 11, 2):
    print(f"Even step: {even}")
#example5
person = {"name": "Alice", "age": 22, "city": "Almaty"}
for key, value in person.items():
    print(f"{key}: {value}")