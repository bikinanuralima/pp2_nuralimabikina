import re
text=input("Enter a camel case string: ")
result=re.sub(r'([A-Z])',r'_\1',text).lower()
print(result)