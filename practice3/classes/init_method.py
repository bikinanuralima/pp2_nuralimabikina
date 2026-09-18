# Example 1
class Student:
    def greet(self):
        print("Hello!")

student = Student()
student.greet()


# Example 2
class Calculator:
    def add(self, a, b):
        return a + b

calculator = Calculator()
print(calculator.add(5, 3))


# Example 3
class Person:
    def introduce(self, name):
        print("My name is", name)

person = Person()
person.introduce("Alice")


# Example 4
class Dog:
    def bark(self):
        print("Woof!")

    def eat(self):
        print("The dog is eating")

dog = Dog()
dog.bark()
dog.eat()


# Example 5
class Student:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print("My name is", self.name)

student = Student("Nuralima")
student.introduce()