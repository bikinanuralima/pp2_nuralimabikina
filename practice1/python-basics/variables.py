#example1
x = 5
y = "John"
print(x)
print(y)
#example2
x = 5
y = "John"
print(x)
print(y)
#example3
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
print(x,y,z)
#example4
x = 5
y = "John"
print(type(x))
print(type(y))
#example5
x = "John"
# is the same as
x = 'John'
#example6
a = 4
A = "Sally"
#A will not overwrite a
#example7
#legal variable names:
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"
#example8
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
x = y = z = "Orange"
print(x)
print(y)
print(z)
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)
#example9
x = "Python is awesome"
print(x)
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)
x = 5
y = 10
print(x + y)
x = 5
y = "John"
print(x, y)
#example10
#globalvariables
#1
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()
#2
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)
#3
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
#4
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)

