
# Read and print file contents
with open("sample.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# Count the number of lines
with open("sample.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    print("Number of lines:", len(lines))