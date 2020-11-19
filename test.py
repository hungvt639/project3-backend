a = [
    {"ab": 1},
    {"ab": 3},
    {"ab": 9},
    {"ab": 4},
    {"ab": 7},
    {"ab": 6},
]

b = [1,2,3,4,5]

m = [i for i in b]
print(m)

def k(value):
    return value['ab']

print(k(a[2]))

x = sum([k(i) for i in a])
print(x)