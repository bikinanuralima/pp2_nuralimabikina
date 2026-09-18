# Example 1
class Animal:
    def eat(self):
        print("I can eat")

class Dog(Animal):
    pass

dog = Dog()
dog.eat()


# Example 2
class Vehicle:
    def move(self):
        print("Vehicle is moving")

class Car(Vehicle):
    pass

car = Car()
car.move()


# Example 3
class Person:
    def speak(self):
        print("I can speak")

class Student(Person):
    pass

student = Student()
student.speak()


# Example 4
class Animal:
    def breathe(self):
        print("I can breathe")

class Cat(Animal):
    def meow(self):
        print("Meow!")

cat = Cat()
cat.breathe()
cat.meow()


# Example 5
class Employee:
    def work(self):
        print("I am working")

class Manager(Employee):
    def manage(self):
        print("I am managing")

manager = Manager()
manager.work()
manager.manage()