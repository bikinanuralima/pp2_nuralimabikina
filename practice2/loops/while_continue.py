#example1
i = 0
while i < 6:
    i += 1
    if i % 2 != 0:
        continue
    print(f"Even number: {i}")
#example2
val = 0
while val < 5:
    val += 1
    if val == 3:
        continue
    print(f"Value: {val}")
#example3 
numbers = [5, -2, 10, -8, 15]
idx = 0
while idx < len(numbers):
    num = numbers[idx]
    idx += 1
    if num < 0:
        continue
    print(f"Positive number: {num}")
#example4
phrases = ["python", "", "code", "", "loops"]
i = 0
while i < len(phrases):
    text = phrases[i]
    i += 1
    if not text:
        continue
    print(f"Valid text: {text}")
#example5
n = 0
while n < 10:
    n += 1
    if n % 3 == 0:
        continue
    print(f"Number: {n}")