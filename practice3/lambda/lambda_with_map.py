# Example 1
numbers = [1, 2, 3, 4]
result = list(map(lambda x: x * 2, numbers))
print(result)


# Example 2
numbers = [1, 2, 3, 4]
result = list(map(lambda x: x * x, numbers))
print(result)


# Example 3
numbers = [5, 10, 15]
result = list(map(lambda x: x + 1, numbers))
print(result)


# Example 4
names = ["alice", "bob", "tom"]
result = list(map(lambda x: x.upper(), names))
print(result)


# Example 5
numbers = [10, 20, 30]
result = list(map(lambda x: x / 10, numbers))
print(result)