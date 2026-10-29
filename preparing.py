#Part 1
#1.1 ★ Predict the value (and the type).
#a) (13-4)/(12*12) b) int(7.9) + round(7.9) c) 5*"3" d) -7//2 and -7%3 e) float(round(7.2)) f) 7/2*2
#a)0,0625(float) b)15.0 (float) c)33333 (string). d)-3(int) and -1(int) e)7.0 (float) f)7.0 (float)
#1.2 ★ Slicing. For s = "programming", what are s[2:8], s[::-3], s[-4:], s[8:2:-2] and len(s[3:3])?
#'ogramm', 'gmrr', 'ming', 'imr', 0
s = "programming"

print(s[2:8], s[::-3], s[-4:], s[8:2:-2])

#1.3 ★ Write. Read an integer from the user. Print zero, positive even, positive odd or negative.
a=int(input())
if (a==0):
    print('zero')
elif (a>0 and a%2==0):
    print("positive even")
elif (a>0 and a%2==1):
    print("positive odd")
elif (a<0 and a%2==0):
    print("negative even")
else:
    print("negative odd")

#1.4 ★ Swap. After x = 3, y = 5, x = y, y = x, what are x and y? 
# Fix it in two ways: with a temp variable, and without one.
x=3
y=5
b=x
x=y
y=b
print("x=",x,"y=",y)
#1.5 ★ Input trap. The user types 3 and then 4. 
# What does a = input(); b = input(); print(a + b) print? Change it to print 3 + 4 = 7.
a=int(input())
b=int(input())
print(a,"+", b , "=", a+b)
#1.6
x = 15
if x > 10: print("a")
elif x > 5: print("b")
if x > 12: print("c")
else: print("d")
#output: a ,c
#Part2
#2.1
n = 20; count = 0
while n > 1:
    if n % 2 == 0: n //= 2
    else: n = 3*n + 1
    count += 1
print(count, n)
#output 7,1
#2.2
total = 0
for i in range(2, 20, 3):
    if total > 20: break
    total += i
print(total, i)
#output : 26,14
#2.3
def sum_35(n):
    sum=0
    for i in range (n):
        if (i%3==0 or i%5==0):
            sum=sum+i
    i=i+1
    print(sum)
sum_35(10)
#2.4 ★★ Write. longest_run(s) returns the length of the longest run of one repeated character. 
# For example, "aabbbcbb" gives 3, and "" gives 0.
def longest_run(s):
    longest = 0
    current = 0
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            current += 1
        else:
            current = 1
        if current > longest:
            longest = current
    print(longest)
longest_run("aabbbccd")
#2.5 ★★ Write. min_max(L) returns the tuple (smallest, largest) of a non-empty list. 
# Don’t use min or max.
def min_max(L):
    min=max=L[0]
    for el in L:
        if el<min:
            min=el
        if el>max:
            max=el
    print (min,max)
min_max([4,-2,9,0])
#2.6 ★★ Write.
#a) count_chars(s) returns a dict mapping each character to its count.
#b) most_common_chars(d) returns the tuple (list_of_chars_with_highest_count, count).
def count_chars(s):
    d = {}
    for ch in s:
        if ch in d: d[ch] += 1
        else: d[ch] = 1
    return d

def most_common_chars(d):
    hi = max(d.values())
    return ([k for k, v in d.items() if v == hi], hi)
#2.7 ★★ Write. Given

#python
#G = {'Ana': {'mq':[5,4,4], 'ps':[10,9,9]},
 #    'Bob': {'mq':[6,7,8], 'ps':[8,9,10]},
  #   'Eric':{'mq':[3],      'ps':[0]}}

#write best_student(G, what), which returns the name of the student with the highest average for what.

#2.8 ★ Predict.

#python
#d = {'a':1, 'b':2}; d['c'] = 3; del(d['a'])
#print('b' in d, 2 in d, list(d.values()), list(d.keys()))

#2.9 ★★ Write. merge_dicts(d1, d2) returns a new dict. 
#Keys present in both dicts get their values added, and the originals stay unchanged.

#2.10 ★★★ Hashing. Use the lecture’s hash: sum the letter positions (a=1, b=2, …) and take % 16. 
#Compute the slots for "Bob", "Eric", "Ben" and "Kate". What do you notice? 
#Then explain why a list can’t be a dict key.
