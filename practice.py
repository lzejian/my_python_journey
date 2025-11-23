
if __name__ == '__main__':
    N = int(input())
    my_list = input().split()
    new_my_list = list(map(int,(my_list[1:3])))
    actual_list = []
    if my_list[0] == "insert":
        actual_list.extend(new_my_list)
    print(actual_list)
        