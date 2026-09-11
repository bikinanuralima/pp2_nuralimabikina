#example1
i = 1
while i <= 5:
    print(f"Count: {i}")
    i += 1
#example2
countdown = 5
while countdown > 0:
    print(f"T-minus {countdown}")
    countdown -= 1
#example3
total = 0
num = 1
while num <= 5:
    total += num
    num += 1
print(f"Total sum: {total}")
#example4
items = ["apple", "banana", "cherry"]
while items:
    print(f"Removed item: {items.pop(0)}")
#example5
value = 1
while value < 30:
    print(f"Current value: {value}")
    value *= 2