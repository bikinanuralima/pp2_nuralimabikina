#1
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
#2
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
#3
from datetime import datetime

now = datetime.now()

without_microseconds = now.replace(microsecond=0)

print("Current datetime:", now)
print("Without microseconds:", without_microseconds)
#4
from datetime import datetime

date1 = datetime(2026, 9, 29, 12, 0, 0)
date2 = datetime(2026, 9, 29, 10, 30, 0)

difference = date1 - date2
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)