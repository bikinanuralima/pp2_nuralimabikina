
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# 1. map(): square every number
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# 2. filter(): select even numbers
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# 3. reduce(): calculate the sum
total = reduce(lambda x, y: x + y, numbers)
print("Sum:", total)

# Another reduce example: calculate the product
product = reduce(lambda x, y: x * y, numbers)
print("Product:", product)

# 4. Type checking
value = "123"
print("Is string:", isinstance(value, str))

# 5. Type conversion
number = int(value)
decimal = float(value)
text = str(number)

print(number, type(number))
print(decimal, type(decimal))
print(text, type(text))