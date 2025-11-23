my_str = "员万过薪月,员序程马黑来,nohtyp学"
# my_str_1 = my_str[my_str.index("黑"):my_str.index(","):-1]
# print(my_str_1)

# my_str_2 = my_str.split(",")[1].strip("来")[::-1]
# print(my_str_2)

my_str_2 = my_str.split(",")[2][-2::-1]+my_str[-1]
print(my_str_2)


my_dict = {"key1":1,"key2":2,"key3":3,"key4":4,"key5":5}
print(f"字典容器转集合的结果是：{set(my_dict)}")

my_dict = {"key2":1,"key6":2,"key5":3,"key7":4,"key1":5}


record = []
for _ in range(int(input())):
    name = input()
    score = float(input())
    r = [name,score]
    students = record.append(r)
print(students)


my_dict = {"王力宏": 99,"周杰伦" : [88,99,110,],"林俊杰": 77}
score = my_dict["周杰伦"]
print(f"周杰伦的分数是{score}")

mylist = ["lzejian","liyibing","cguazhan"]
mylist.reverse()
print(mylist)

if __name__ == '__main__':
    N = int(input())
    my_list = []
    my_list.insert(0,5)
    my_list.insert(1,10)
    my_list.insert(0,6)
    print(my_list)
    my_list.remove(6)
    my_list.append(9)
    my_list.append(1)
    print(sorted(my_list))
    element = my_list.pop()
    my_list.reverse()
    print(my_list)