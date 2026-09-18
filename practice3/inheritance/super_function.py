# Example 1
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university

student = Student("Alice", "KBTU")

print(student.name)
print(student.university)


# Example 2
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

dog = Dog("Buddy", "Labrador")

print(dog.name)
print(dog.breed)


# Example 3
class Vehicle:
    def start(self):
        print("Vehicle starts")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car starts")


car = Car()
car.start()


# Example 4
class Person:
    def introduce(self):
        print("I am a person")

class Student(Person):
    def introduce(self):
        super().introduce()
        print("I am a student")

student = Student()
student.introduce()


# Example 5
class Parent:
    def __init__(self, age):
        self.age = age

class Child(Parent):
    def __init__(self, age, name):
        super().__init__(age)
        self.name = name

child = Child(18, "Alice")

print(child.age)
print(child.name)