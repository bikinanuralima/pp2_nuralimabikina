#example1
def my_function(fname):# fname is a parameter
    print(fname+ " Refsnes")
my_function("Emil")#"Emil" is an argument
my_function("Tobias")
my_function("Linus")

#example2
def my_function(fname,lname):
    print(fname+" "+lname)
my_function("Emil","Refsnes")

#example3
def my_function(name="friend"):
    print("Hello",name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#example4
def my_function(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)

my_function("dog", name = "Buddy", age = 5)

#example5
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

#example6
def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)

#example7
def my_function(name, /): #ONLY positional arguments
  print("Hello", name)

my_function("Emil")

#example8
def my_function(*, name): #Keyword-Only Arguments
  print("Hello", name)

my_function(name = "Emil")

#example9
def my_function(a, b, /, *, c, d): #Combining Positional-Only and Keyword-Only
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)