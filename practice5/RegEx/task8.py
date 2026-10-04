import re
text=input("Enter a string: ")
result = re.split(r"(?=[A-Z])",text)
print(result)