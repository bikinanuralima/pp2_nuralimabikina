#example1
for num in range(1, 10):
    if num == 5:
        break
    print(num)
#example2
names = ["Alice", "Bob", "Charlie", "David"]
for name in names:
    if name == "Charlie":
        print("Target name found!")
        break
    print(f"Checking: {name}")
#example3
for letter in "programming":
    if letter == "a":
        break
    print(letter)
#example4
users = [{"id": 1, "active": True}, {"id": 2, "active": False}, {"id": 3, "active": True}]
for user in users:
    if not user["active"]:
        print(f"First inactive user ID: {user['id']}")
        break
#example5
numbers = [10, 20, 30, 40, 50]
current_sum = 0
for n in numbers:
    current_sum += n
    if current_sum > 50:
        print(f"Sum exceeded limit at {current_sum}")
        break