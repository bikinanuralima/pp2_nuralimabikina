#example1
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    if fruit == "banana":
        continue
    print(fruit)
#example2
for i in range(1, 10):
    if i % 2 != 0:
        continue
    print(f"Even: {i}")
#example3
word = "python"
for letter in word:
    if letter in "aeiou":
        continue
    print(f"Consonant: {letter}")
#example4
dataset = [12, -5, 20, -1, 35]
for data in dataset:
    if data < 0:
        continue
    print(f"Valid data entry: {data}")
#example5
words = ["hi", "python", "a", "code", "ok"]
for word in words:
    if len(word) < 3:
        continue
    print(f"Long word: {word}")