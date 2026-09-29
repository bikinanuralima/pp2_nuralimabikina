#1
def squares(n):
    for i in range(n + 1):
        yield i * i


for number in squares(5):
    print(number)
#2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


n = int(input("Enter n: "))

print(",".join(str(number) for number in even_numbers(n)))
#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


for number in divisible_by_3_and_4(50):
    print(number)
#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


for number in squares(2, 6):
    print(number)
#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


for number in countdown(5):
    print(number)