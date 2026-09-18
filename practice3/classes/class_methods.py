# Example 1
class Student:
    def __init__(self, name):
        self.name = name

student = Student("Alice")
print(student.name)


# Example 2
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Bob", 20)
print(person.name)
print(person.age)


# Example 3
class Car:
    def __init__(self, brand):
        self.brand = brand

car = Car("Toyota")
print(car.brand)


# Example 4
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

book = Book("Harry Potter", "J.K. Rowling")
print(book.title)
print(book.author)


# Example 5
class Phone:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

phone = Phone("Apple", 500000)
print(phone.brand)
print(phone.price)