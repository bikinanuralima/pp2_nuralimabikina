#example1
age = 25
has_id = True
is_eligible = (age >= 18) and has_id
print(is_eligible)  
#example2
is_admin = False
has_vip_pass = True
can_enter = is_admin or has_vip_pass
print(can_enter) 
#example3
is_online = False
is_offline = not is_online
print(is_offline)
#example4
exam_score = 75
attendance = 90
has_extra_credit = False
passed = (exam_score >= 70 and attendance >= 80) or has_extra_credit
print(passed)
#example5
number = 15
is_in_range = (number > 10) and (number < 20) and not (number == 15)
print(is_in_range)