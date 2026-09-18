# Example 1
class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Woof!")

dog = Dog()
dog.sound()


# Example 2
class Animal:
    def move(self):
        print("Animal moves")

class Bird(Animal):
    def move(self):
        print("Bird flies")

bird = Bird()
bird.move()


# Example 3
class Person:
    def introduce(self):
        print("I am a person")

class Student(Person):
    def introduce(self):
        print("I am a student")

student = Student()
student.introduce()


# Example 4
class Vehicle:
    def start(self):
        print("Vehicle starts")

class Car(Vehicle):
    def start(self):
        print("Car starts with a key")

car = Car()
car.start()


# Example 5
class Shape:
    def draw(self):
        print("Drawing a shape")

class Circle(Shape):
    def draw(self):
        print("Drawing a circle")

circle = Circle()
circle.draw()