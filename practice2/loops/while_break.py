#example1
i = 1
while i <= 10:
    if i == 5:
        break
    print(i)
    i += 1
#example2
numbers = [3, 7, 12, 19, 21]
idx = 0
target = 12
while idx < len(numbers):
    if numbers[idx] == target:
        print(f"Found {target} at index {idx}")
        break
    idx += 1
#example3
count = 0
while True:
    print(f"Looping {count}")
    count += 1
    if count >= 3:
        break
#example4 
words = ["hello", "world", "STOP", "python"]
i = 0
while i < len(words):
    if words[i] == "STOP":
        print("Encountered stop command")
        break
    print(f"Processing: {words[i]}")
    i += 1
#example5
score = 10
while score < 100:
    if score > 50:
        print("Threshold exceeded, stopping.")
        break
    score += 15