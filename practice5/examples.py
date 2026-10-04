import re
# 1.REGEX FUNCTIONS
text = "My phone numbers are 87071234567 and 87771234567."

# search() - finds the first match
result = re.search(r"\d+", text)
print("search():", result.group())


# findall() - finds all matches
result = re.findall(r"\d+", text)
print("findall():", result)


# split() - splits the string using a pattern
text2 = "apple,banana;orange grape"
result = re.split(r"[,; ]", text2)
print("split():", result)


# sub() - replaces matches
text3 = "My phone number is 87071234567"
result = re.sub(r"\d", "*", text3)
print("sub():", result)

# 2. METACHARACTERS

# . - any character
text = "cat cot cut"
print(". :", re.findall(r"c.t", text))

# ^ - beginning of string
text = "Hello world"
print("^ :", re.findall(r"^Hello", text))

# $ - end of string
print("$ :", re.findall(r"world$", text))

# [] - one character from a set
text = "cat bat rat dog"
print("[] :", re.findall(r"[cbr]at", text))

# | - OR
text = "I like cats and dogs"
print("| :", re.findall(r"cats|dogs", text))

# () - group
text = "apple banana orange"
print("() :", re.findall(r"(apple|banana)", text))


# 3. SPECIAL SEQUENCES

text = "Room 25, floor 3."

# \d - digit
print(r"\d :", re.findall(r"\d", text))

# \D - non-digit
print(r"\D :", re.findall(r"\D+", text))

# \w - word character
text = "hello_123!"
print(r"\w :", re.findall(r"\w+", text))

# \W - non-word character
print(r"\W :", re.findall(r"\W+", text))

# \s - whitespace
text = "Hello world Python"
print(r"\s :", re.findall(r"\s", text))

# \S - non-whitespace
print(r"\S :", re.findall(r"\S+", text))

# \b - word boundary
text = "cat scatter cat"
print(r"\b :", re.findall(r"\bcat\b", text))


# ==========================================
# 4. QUANTIFIERS
# ==========================================

# * - zero or more
text = "a ab abb abbb"
print("* :", re.findall(r"ab*", text))

# + - one or more
print("+ :", re.findall(r"ab+", text))

# ? - zero or one
text = "color colour"
print("? :", re.findall(r"colou?r", text))

# {n} - exactly n times
text = "123 1234 12345"
print("{n} :", re.findall(r"\d{4}", text))

# {n,m} - from n to m times
text = "1 12 123 1234 12345"
print("{n,m} :", re.findall(r"\d{2,4}", text))