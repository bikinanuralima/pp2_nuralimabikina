import re
text=input()
result=re.findall(r"[0-9]",text)
print(result)

from datetime import datetime
date1 = datetime(2026, 10, 5, 12, 0, 0)
date2 = datetime(2026, 10, 31, 10, 30, 0)
difference = date1 - date2

print(difference)
