# Example 1
numbers = [5, 2, 8, 1, 3]
result = sorted(numbers, key=lambda x: x)
print(result)


# Example 2
words = ["apple", "cat", "banana", "dog"]
result = sorted(words, key=lambda x: len(x))
print(result)


# Example 3
students = [
    ("Alice", 20),
    ("Bob", 18),
    ("Tom", 22)
]

result = sorted(students, key=lambda x: x[1])
print(result)


# Example 4
numbers = [1, 5, 3, 9, 2]
result = sorted(numbers, key=lambda x: x, reverse=True)
print(result)


# Example 5
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 95},
    {"name": "Tom", "grade": 75}
]

result = sorted(students, key=lambda x: x["grade"])
print(result)