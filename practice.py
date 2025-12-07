import textwrap

def wrap(string, max_width):
    result_list = []
    for i in range(0,len(string),max_width):
        result_list.append(string[i:i + max_width])
    return "\n".join(result_list)
        
    return str
if __name__ == '__main__':
    string, max_width = input(), int(input())
    result = wrap(string, max_width)
    print(result)

m,n = input().split()
list_i = list(map(int,input().split()))
list_a = input().split()
set_a = set(map(int,list_a))
list_b = input().split()
set_b = set(map(int,list_b))
count_a = 0
count_b = 0
for x in set_a:
    for y in list_i:
        if y == x:
            count_a += 1
for z in set_b:
    for y in list_i:
        if y == z:
            count_b += 1
if count_a >= count_b:
    print(count_a - count_b)
else:
    print(count_b - count_a)


