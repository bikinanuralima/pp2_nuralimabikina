def count_chars(s):
    d = {}
    for ch in s:
        if ch in d: d[ch] += 1
        else: d[ch] = 1
    return d

def most_common_chars(d):
    hi = max(d.values())
    return ([k for k, v in d.items() if v == hi], hi)