# Example 1
class Father:
    def drive(self):
        print("I can drive")

class Mother:
    def cook(self):
        print("I can cook")

class Child(Father, Mother):
    pass

child = Child()
child.drive()
child.cook()


# Example 2
class Teacher:
    def teach(self):
        print("I can teach")

class Researcher:
    def research(self):
        print("I can research")

class Professor(Teacher, Researcher):
    pass

professor = Professor()
professor.teach()
professor.research()


# Example 3
class Flyer:
    def fly(self):
        print("I can fly")

class Swimmer:
    def swim(self):
        print("I can swim")

class Duck(Flyer, Swimmer):
    pass

duck = Duck()
duck.fly()
duck.swim()


# Example 4
class Writer:
    def write(self):
        print("I can write")

class Singer:
    def sing(self):
        print("I can sing")

class Artist(Writer, Singer):
    pass

artist = Artist()
artist.write()
artist.sing()


# Example 5
class Computer:
    def use_computer(self):
        print("I can use a computer")

class Programmer:
    def code(self):
        print("I can code")

class Developer(Computer, Programmer):
    pass

developer = Developer()
developer.use_computer()
developer.code()