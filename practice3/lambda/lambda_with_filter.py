# Example 1
numbers = [1, 2, 3, 4, 5, 6]
result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)


# Example 2
numbers = [1, 2, 3, 4, 5, 6]
result = list(filter(lambda x: x % 2 != 0, numbers))
print(result)


# Example 3
numbers = [10, 15, 20, 25, 30]
result = list(filter(lambda x: x > 20, numbers))
print(result)


# Example 4
words = ["cat", "elephant", "dog", "computer"]
result = list(filter(lambda x: len(x) > 3, words))
print(result)


# Example 5
numbers = [-5, 2, -1, 7, -3]
result = list(filter(lambda x: x > 0, numbers))
print(result)