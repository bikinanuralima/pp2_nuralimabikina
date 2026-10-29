import os
with open("log.txt","w") as f:
    f.write("I can do it"+"\n")

with open("log.txt","r") as f:
    content=f.read()
    print(content)

with open("log.txt","a") as f:
    f.write("full mark")
with open("log.txt","r") as f:
    content=f.read()
    print(content)
path="practice6"
if os.path.exists():
    print("Filename", os.path.basename(path))
    print("Directory",os.path.dirname(path))
else:
    print("it does not exist")
os.rename("log.txt","log_old.txt")
os.remove("log_old.txt")