
if __name__ == '__main__':
    N = int(input())
    my_list = input().split()
    new_my_list = list(map(int,(my_list[1:3])))
    actual_list = []
    if my_list[0] == "insert":
        actual_list.extend(new_my_list)
    print(actual_list)


n = int(input())
my_list = input().split()
t = tuple(map(int,my_list))
print(t)
print(hash(t))

first = input()
last = input()

my_str = "itheima and 2itcast"
for item in my_str:
    print(f"字符串的for循环遍历是{type(item)}")


def swap_case(s):
    l = []
    for i in s:
        if i.isupper():
            i.lower()
            l.append(i)
        elif i.islower():
            i.upper()
            l.append(i)
        else:
            l.append(i)
        s = "".join(l)           
    return s

if __name__ == '__main__':
    s = input()
    result = swap_case(s)
    print(result)


   