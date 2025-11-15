"""
数据容器
"""
# 简单来说就是把数据放在一个容器里，方便管理和操作。
# 1. 列表 2. 元组 3. 字典 4. 集合 5. 字符串
###########################################################
"""
list列表
"""
# 定义一个列表
my_list = ["lzejian",666,True]
# 函数---list() 把一个**“可迭代对象” (Iterable)--也就是一个容器（为了遍历for循环搭配）** 变成列表
# list("lzejian", 666, True)是错误的。list() 只能接受一个参数---例如一整个元组或字符串。
print(my_list)
print(type(my_list))  # <class 'list'>

# 列表的嵌套
my_list2 = [[1,2,3],[4,5,6]]
print(my_list)
print(type(my_list)) # <class 'list'>

# 列表索引
# 列表取出的方法就是列表[]，从0开始依次+1，也可以反过来-1，-2，-3---取列表中排后面的好取。
print(my_list[0])  # lzejian
print(my_list[1])  # 666
print(my_list[2])  # True
# 超出范围内的取不出来
print(my_list[23])  # IndexError: list index out of range
# 负数索引
print(my_list[-1])  # True
# 嵌套索引
print(my_list2[0])  # [1, 2, 3]
print(my_list2[0][2])  # 3
#################################################
"""
list列表的常用方法
"""
#* 方法就是一种特定数据类型的特殊函数，所以它也是以return结尾，可以用变量接收结果。
mylist = ["lzejian","liyibing","cguazhan"]
# 1.查找某元素在列表下的索引
number = mylist.index("liyibing")
print("liyibing的索引是：", number)  # liyibing的索引是： 1
  # 查找某元素在列表下的索引，如果不存在则报错
  # number = mylist.index("junjiewu")  # ValueError: 'junjiewu1' is not in list
# 2.修改特定下标的索引值
mylist[0] = "junjiewu"
print(mylist) # ['junjiewu', 'liyibing', 'cguazhan']
# 3.在指定下标位置插入新元素
mylist.insert(1, "lzejian")
print(mylist)  # ['junjiewu', 'lzejian', 'liyibing', 'cguazhan']
# 4.在列表的尾部追加单个元素
mylist.append("lzejian")
print(mylist)  # ['junjiewu', 'lzejian', 'liyibing', 'cguazhan', 'lzejian']
# 5.在列表的尾部追加多个元素
mylist.extend(["uyojiaqi", 666])
print(mylist)  # ['junjiewu', 'lzejian', 'liyibing', 'cguazhan', 'lzejian', 'uyojiaqi', 666]
# 6.删除指定下标索引的元素
mylist = ["lzejian","liyibing","cguazhan"]
del mylist[0]
print(mylist)  # ['liyibing', 'cguazhan']
mylist = ["lzejian","liyibing","cguazhan"]
element = mylist.pop(0)  
# pop()默认删除最后一个元素,pop的功能是1.取出选择值再return出来 2.列表该索引的元素删除。可以用element来存储结果。
print(f"通过pop方法删除的元素后的列表是:{mylist},取出的元素是：{element}")
# 7.删除某元素在列表的第一个匹配项
mylist = ["lzejian","liyibing","cguazhan","lzejian","lzejian"]
mylist.remove("lzejian")
print(mylist) # ['liyibing', 'cguazhan', 'lzejian', 'lzejian']
# 8.清空列表
mylist.clear()
print(mylist)  # []
# 9.统计某元素在列表中出现的次数
mylist = ["lzejian","liyibing","cguazhan","lzejian","lzejian"]
count = mylist.count("lzejian")
print(f"lzejian在列表中出现的次数是：{count}")  # lzejian在列表中出现的次数是：3
# 10.统计列表中所有元素的个数
count = len(mylist)
print(f"列表中所有元素的个数是：{count}")  # 列表中所有元素的个数是：5

"""
test
"""
age = [21,25,21,23,22,20]
age.append(31)
age_2 = [29,33,30]
age.extend(age_2)
# 取第一个元素
num_1 = age[0]
# 取最后一个元素
num_2 = age[-1]
element = age.pop()
print(element)
print(age)
index = age.index(31)
print(index)

"""
列表的遍历
"""
# 1. for循环遍历
def for_item():
    mylist = [1, 2, 3, 4, 5]
    for item in mylist:
        print(f"for循环的遍历结果是: {item}")  # 1 2 3 4 5
# 2. while循环遍历
def while_item():
    mylist = [1, 2, 3, 4, 5]
    index = 0 # 定义一个变量标记列表索引值的下标
    # 通过index变量取出对应下标的元素
    while index < len(mylist):
        element = mylist[index]
        print(f"while循环的遍历结果是: {element}")
        index += 1
while_item()
# 如果是 result = while_item()，则会返回None，因为while_item函数没有返回值。也就是print函数会报错。这就是return的作用
# 解决方法就是在函数中添加return语句，返回一个值。

###################################################
"""
小测试
"""
my_list_1 = [1,2,3,4,5,6,7,8,9,10]
my_list_2 = []
def even_take():
    index = 0
    while index < len(my_list_1):
        if my_list_1[index] % 2 == 0:
            my_list_2.append(my_list_1[index])
        index += 1
    for x in my_list_2:
        print(x)
even_take()

###########################################
"""
元组
"""
# 1.定义一个元组
t1 = ("lzejian", 666, True)
t2 = ()
t3 = tuple() # t2,t3都是空元组,区别是t3是面向对象
print(f"t1的类型是：{type(t1)},它的内容是{t1}")
print(f"t2的类型是：{type(t2)},它的内容是{t2}")
print(f"t3的类型是：{type(t3)},它的内容是{t3}")
# 2.定义单个元素的元组
t4 = ("lzejian",) # 注意逗号,元组单个元素必须加逗号
# 3.元组的嵌套
t5 = (1, 2, 3, (4, 5, 6))  # 元组中嵌套了一个元组
t6 = (1, 2, 3, [4, 5, 6])  # 元组中嵌套了一个列表
# 4.元组的操作 index
t7 = ((1, 2, 3), (4, 5, 6))  
search = t7[1][2]
print(f"t7的第二个元组的第三个元素是：{search}")  # t7的第二个元组的第三个元素是：6
t8 = (1, 2, 3, 4, 5, 6)
index = t8.index(6) # t7用这个索引不出来
print(f"6在t8中的索引是：{index}")  # 6在t7中的索引是：5
# 5.元组的操作 count
t8 = (1, 2, 3, 3, 3, 3)
count = t8.count(3)
print(f"3在t8中出现的次数是：{count}")  # 3在t8中出现的次数是：4
# 6.元组的操作 len
length = len(t8)
print(f"t8的长度是：{length}")  # t8的长度是：6
# 7.元组的遍历
# 7.1. for循环遍历
t8 = (1, 2, 3, 4, 6,7)
for item in t8:
    print(f"for循环遍历的结果是：{item}")  # 1 2 3 4 6 7
# 7.2. while循环遍历
index = 0
while index < len(t8):
    element = t8[index]
    print(f"while循环遍历的结果是：{element}")  # 1 2 3 4 6 7
    index += 1
# 8.元组的不可变性
# 元组是不可变的，不能修改元组中的元素,但是可以修改元组中的列表元素
t10 = (1, 2, 3, [4, 5, 6])
t10[2][0] = 7  # TypeError: 'tuple' object does not support item assignment
t10[3][0] = "lzejian"
print(f"修改后的元组是：{t10}")  # 修改后的元组是：(1, 2, 3, [lzejian, 5, 6])

"""
test
"""
information = ("周杰伦",11,["football","music"])
index = information.index(11)
print(f"年龄所在位置是{index}")
name = information[0]
print(f"姓名是{name}")
# infor2 = del.information[2][0] del只能直接删除，不能用赋值变量
# infor2 = information[2].pop(0)  选出元组中你想删除的元素，找到列表的下标，然后用pop方法删除
del information[2][0]
print(f"兴趣爱好是{information[2][0]}")
infor3 = information[2].append("coding")  # 选出元组中你想加入的元素，找到列表的下标，然后用append方法添加
infor3 = information[2].insert(1, "coding")  # 选出元组中你想加入的元素，找到列表的下标，然后用insert方法添加
print(f"兴趣爱好是{information}")
"""
总而言之，就是在元组的后面写上列表的下标，就可以对列表进行操作了。
"""



"""
字符串string
"""
# 字符串和元组一样也是无法修改的，只可以存储字符串

# 定义一个字符串
my_str = "itheima and itcast"
# 通过下标索引取值
value = my_str[2]
value2 = my_str[-16] # 空格也算是变量
print(f"从字符串取下标为2的元素，它的值是{value}，取下标是-16的元素，它的值是{value2}")
# my_str[2] = "H" 操作不了，因为字符串不可更改
# index 方法
my_str = "itheima and itcast"
value = my_str.index("and i")
print(f"字符串and的下标索引是{value}") # 字符串and的下标索引是8，因为在itheima对应0123456，7对应空格，8对应and的a，index查找的是子字符串的起始位置。
# replace 方法
new_my_str = my_str.replace("it","程序") # 所有的it都换成了程序。
print(f"替换之后是{new_my_str}") # 用这个方法并不代表改变了原来的字符串，只是新增了一个字符串。
# split 方法
my_str = "hello python itheima itcast"
new_my_str = my_str.split(" ") # 参数填你要分割的东西
print(f"通过split方法分割后的字符串为{new_my_str},它的类型是{type(new_my_str)}") # split分割后会得到一个新的列表！
#* strip 方法
my_str = " itheima and  itcast "
new_my_str = my_str.strip()
print(f"不传参数的字符串得到的是没有前后空格的{new_my_str}")
my_str = "12itheima and  itcast21"
new_my_str = my_str.strip("12")
print(f"传了参数\"12\"的字符串得到的是没有\"12\"的{new_my_str}")  # 删除12时不是按照12顺序，而是两个字符"1""2"来删除前后的字符。
text_left = "    lzejian"
text_right = "lzejian    "

#* lstrip() 只管左边
print(f"lstrip: '{text_left.lstrip()}'")   # 输出: 'lzejian'
print(f"lstrip: '{text_right.lstrip()}'")  # 输出: 'lzejian    ' (右边不动)

print("---")

#* rstrip() 只管右边
print(f"rstrip: '{text_left.rstrip()}'")   # 输出: '    lzejian' (左边不动)
print(f"rstrip: '{text_right.rstrip()}'")  # 输出: 'lzejian'

# 统计字符串某个字符串的出现次数
my_str = " itheima and  itcast "
num = my_str.count("t")
print(f"t在字符串出现的次数是{num}")
# 统计字符串长度
length = len(my_str)
print(f"字符串的长度是{length}")
# 循环遍历 for
for item in my_str:
    print(f"字符串的for循环遍历是{item}")
# 循环遍历 while
index = 0 
my_str = " itheima and  itcast "
length = len(my_str)
while index < length: # 这里必须是小于而不是等于，是因为length是字符串的长度，也就是里面每一个字符的总和，而index代表的是每一个字符的下标，相当于index = length -1,所以必须小于。
    element = my_str[index]
    print(f"字符串的for循环遍历是{element}")
    index += 1
"""
test
"""
a_str = "itheima itcast boxuegu"
num = a_str.count("it")
print(f"一共有{num}个it字符在字符串里")
b_str = a_str.replace(" ","|")
print(f"替换后的结果是{b_str}")
c_list = b_str.split("|")
print(f"修改后的结果是{c_list}") # split就是把所有的符号换成","分割开来，并且变成列表的形式，可以增删。


"""
集合（当我们需要一个乱序的，元素不可重复但类型多样的数据存储，就可以使用集合。）
"""
# 定义一个集合
my_set1 = {"传智教育","黑马程序员","IT黑马","传智教育","黑马程序员","IT黑马","传智教育","黑马程序员","IT黑马"}
my_set2 = set()
print(f"my_set1输出的内容是{my_set1},它的类型是{type(my_set1)}") # 集合不支持重复元素，并且里面的元素显示都是乱序的，所以也没有下标
print(f"my_set2输出的内容是{my_set2},它的类型是{type(my_set2)}") # 空集就是set()
# 添加新元素
my_set1.add("python")
print(f"my_set1输出的内容是{my_set1}")
# 移除元素
my_set1.remove("python")
print(f"my_set1输出的内容是{my_set1}")
# 随机取出一个元素
# my_set1.pop("黑马程序员") # 错误写法，set.pop不允许加参数
my_set1.pop()
print(f"my_set1输出的内容是{my_set1}")
# 清空集合
my_set1.clear()
print(f"my_set1输出的内容是{my_set1}") # 结果是set()，意味着空集没有元素了。
# 取2个集合的差集
my_set1 = {1,2,3}
my_set2 = {1,5,6}
my_set3 = my_set1.difference(my_set2)
print(f"my_set3输出的内容是{my_set3}") # 上边的操作比如添加移除，都是对原有的集合改变了元素，但是取差集不会影响到两个元素，所以需要一个变量来接受差集
# 消除2个集合的差集
my_set1 = {1,2,3}
my_set2 = {1,5,6}
my_set1.difference_update(my_set2)
print(f"my_set1输出的内容是{my_set1}") # 在1中消除了两个集合的交集元素，并且改变了集合本身，2保持不变。
print(f"my_set2输出的内容是{my_set2}") # 2保持不变
# 2个集合合并，并集
my_set1 = {1,2,3}
my_set2 = {1,5,6}
my_set3 = my_set1.union(my_set2)
print(f"my_set1输出的内容是{my_set1}")
print(f"my_set2输出的内容是{my_set2}")
print(f"my_set3输出的内容是{my_set3}") # 并集1和2不变，会并成一个集合所以需要一个变量接收新集合，里面重复的元素自动消失。
# 统计集合的元素数量
my_set1 = {"传智教育","黑马程序员","IT黑马","传智教育","黑马程序员","IT黑马","传智教育","黑马程序员","IT黑马"}
print(f"my_set1的集合元素数量是{len(my_set1)}")
# 集合的遍历（只有for，因为while需要下标，集合是乱序没有下标）
my_set1 = {"传智教育","黑马程序员","IT黑马","传智教育","黑马程序员","IT黑马","传智教育","黑马程序员","IT黑马"}
for element in my_set1:
    print(f"集合遍历的结果是{element}")

"""
test（把一个重复列表变成集合）
"""
my_list = ["黑马程序员","传智播客","黑马程序员","传智播客","itheima","itcast","itheima","itcast","best"]
set_empty = set()
for x in my_list:
    print(f"通过for循环遍历列表的结果是{x}")
    set_empty.add(x)
    # set_new = set_empty.add(x)是错误的写法！！！add函数添加完元素直接返回到原来的集合或列表，即使设置新的变量也无济于事，这是python的固定语法！
print(f"最终的结果是{set_empty}")



"""
演示对序列进行切片操作
"""

# 对list进行切片，从1开始，从4结束，步长为1
my_list = [1,2,3,4,5,6]
result1 = my_list[0:4]  # 因为步长为1，默认值就是1，所以可以不用写步长。
print(f"结果是{result1}") # [1,2,3,4] ,起始为下标，结束为下标减一，因为结束不带本下标索引值。
# 对tuple进行切片，从头开始，到最后结束，步长为1
my_tuple = (1,2,3,4,5,6)
result2 = my_tuple[::1]
print(f"结果是{result2}")
# 对str进行切片，从头开始，到最后结束，步长为2
my_str = "lzejian"
result3 = my_str[::2]
print(f"结果是{result3}")
# 对str进行切片，从头开始，到最后结束，步长-1
my_str = "lzejian"
result4 = my_str[::-1]
print(f"结果是{result4}")
# 对列表进行切片，从3开始，到1结束，步长-1
my_list = [0,1,2,3,4,5,6]
index1 = my_list.index(3)
index2 = my_list.index(1)
result5 = my_list[index1:index2 - 1:-1] # 这里第二个变量不可以忘了- 1，因为终止值是不包含本身的，它包含到本身 + 1
print(f"结果是{result5}")
# 对元组进行切片，从头开始，到尾结束，步长为 -2
my_tuple = (1,2,3,4,5,6)
result6 = my_tuple[::-2]
print(f"结果是{result6}")
"""
切片得到的都是新的元组，字符串，列表。因为元组，字符串都是不可更改的。
"""

"""
test
"""
my_str = "万过薪月，员序程马黑来，nohtyp学"
index1 = my_str.index("黑")
index2 = my_str.index("月")
result1 = my_str[index1:index2 + 1:-1]
print(f"结果是{result1}")

my_str = "万过薪月，员序程马黑来，nohtyp学"
# result1 = my_str[5:10:-1]  # 这种方式错误的原因是因为5：10是正序，而-1是倒序，所以不会显示任何结果，冲突了
result1 = my_str[5:10] [::-1] # 这种方式就是先给它排序好，再倒序，可以在一行进行操作。
print(f"结果是{result1}")

my_str = "万过薪月，员序程马黑来，nohtyp学"
result1 = my_str.split("，")[1].replace("来","")[::-1]
"""
result1 = my_str.split("，")[1].replace("来","")[::-1] ,这些变换都可以在一行完成！
"""
print(f"结果是{result1}")

"""
演示数据容器字典的定义
"""
# 字典是没有下标值的，也不允许重复，重复就覆盖
# 定义一个字典，基本形式 {key:value，key:value,...},每一个key:value是一对键对值
my_dictionary = {"王力宏": 99,"周杰伦" : 88,"林俊杰": 77}
# 定义一个空字典
my_dict = {}
my_dict = dict()
# 定义重复key的字典
my_dict = {"王力宏": 99,"王力宏": 88,"周杰伦" : 88,"林俊杰": 77}
print(f"重复key的字典是{my_dict}") # 重复key的字典会按照后面的更新掉前面的数据，也就是一个key对应一个value
# 从字典中基于key获取value值
my_dict = {"王力宏": 99,"周杰伦" : 88,"林俊杰": 77}
score = my_dict["周杰伦"]
print(f"周杰伦的分数是{score}")
# 定义嵌套字典
my_dict = {"王力宏":{
           "数学":99,"英语":88,"语文":77} ,
           "周杰伦" : {
           "数学":45,"英语":78,"语文":41},
           "林俊杰": {
           "数学":12,"英语":56,"语文":82}} # 就是{key:{key:value}}的形式
# 从嵌套字典中获取数据
score = my_dict["王力宏"]["英语"]
print(f"王力宏的英语分数是{score}")

# 演示字典的常规操作
my_dict = {"王力宏": 99,"周杰伦" : 88,"林俊杰": 77}
# 新增元素
my_dict["张信哲"] = 66 # 形式就是my_dict[key] = value
print(f"新增元素后的字典是{my_dict}")
# 更新元素
my_dict["王力宏"] = 4545
print(f"更新元素后的字典是{my_dict}")
# 删除元素
score = my_dict.pop("王力宏")
print(f"删除后的字典是{my_dict}，删除的分数是{score}")
# 清空元素
my_dict.clear()
print(f"清空后的字典是{my_dict}")
# 获取全部的key
my_dict = {"王力宏": 99,"周杰伦" : 88,"林俊杰": 77}
keys = my_dict.keys()
print(keys) # 特殊注意，keys取得的是全部的key，没有value
# 遍历字典 # 方法1
for key in keys:
    print(f"字典里的key有{key}") 
# 遍历字典 # 方法2
for key in my_dict:
    print(f"字典2里的key有{key}")
# 统计字典内的元素数量
print(f"字典里的元素数量为{len(my_dict)}") # 一个key:value为一个元素。

"""
test
"""

staff_infor_dict = {
    "王力宏":{"部门":"科技部","工资":3000,"级别":1},
    "周杰伦":{"部门":"市场部","工资":5000,"级别":2},
    "林俊杰":{"部门":"市场部","工资":7000,"级别":3},
    "张学友":{"部门":"科技部","工资":4000,"级别":1},
    "刘德华":{"部门":"市场部","工资":6000,"级别":2},
}
print("全体员工当前信息如下 :")
print(staff_infor_dict)
keys = staff_infor_dict.keys()
for key in keys:
    level = staff_infor_dict[key]["级别"] # 仅仅是赋值，不改变字典本身，在这里也可以理解成把staff_infor_dict[key]["级别"]写的美观一点。
    if level == 1:
       staff_infor_dict[key]["级别"] += 1 # 这里为什么不用level += 1，因为level只是被赋予了一个值"2"，但是原字典中级别并没有改变。
       staff_infor_dict[key]["工资"] += 1000
print("全体1级员工升级1级后信息如下 :")
print(staff_infor_dict)

"""
演示数据容器的通用功能
"""
my_list = [1,2,3,4,5]
my_tuple = (1,2,3,4,5)
my_str = "abcdefg"
my_set = {1,2,3,4,5}
my_dict = {"key1":1,"key2":2,"key3":3,"key4":4,"key5":5}

# len元素个数
# max最大元素
print(f"my_list的最大元素是{max(my_list)}")
print(f"my_tuple的最大元素是{max(my_tuple)}")
print(f"my_str的最大元素是{max(my_str)}")
print(f"my_set的最大元素是{max(my_set)}")
print(f"my_dict的最大元素是{max(my_dict)}")
# min最小元素
print(f"my_list的最小元素是{min(my_list)}")
print(f"my_tuple的最小元素是{min(my_tuple)}")
print(f"my_str的最小元素是{min(my_str)}")
print(f"my_set的最小元素是{min(my_set)}")
print(f"my_dict的最小元素是{min(my_dict)}")
# 类型转换 容器转列表
print(f"元组容器转列表的结果是：{list(my_tuple)}")
print(f"字符串容器转列表的结果是：{list(my_str)}")
print(f"集合容器转列表的结果是：{list(my_set)}")
print(f"字典容器转列表的结果是：{list(my_dict)}")
# 类型转换 容器转元组
print(f"列表容器转元组的结果是：{tuple(my_list)}")
print(f"字符串容器转元组的结果是：{tuple(my_str)}")
print(f"集合容器转元组的结果是：{tuple(my_set)}")
print(f"字典容器转元组的结果是：{tuple(my_dict)}")
# 类型转换 容器转字符串 输出的字面量是"[1,2,3,4,5]"这种形式
print(f"列表容器转字符串的结果是：{str(my_list)}") # 结果是[1,2,3,4,5]
print(f"元组容器转字符串的结果是：{str(my_tuple)}")
print(f"集合容器转字符串的结果是：{str(my_set)}")
print(f"字典容器转字符串的结果是：{str(my_dict)}")
# 类型转换 容器转集合
print(f"列表容器转集合的结果是：{set(my_list)}")
print(f"字符串容器转集合的结果是：{set(my_tuple)}")
print(f"集合容器转集合的结果是：{set(my_str)}")
print(f"字典容器转集合的结果是：{set(my_dict)}")
# sorted 排序
my_list = [3,2,1,4,5]
my_tuple = (5,8,12,456,16)
my_str = "bfsjzqw"
my_set = {63,15,31,12,3}
my_dict = {"key2":1,"key6":2,"key5":3,"key7":4,"key1":5}
print(f"列表容器排序的结果是：{sorted(my_list)}")
print(f"元组容器排序的结果是：{sorted(my_tuple)}")
print(f"字符串容器排序的结果是：{sorted(my_str)}")
print(f"集合容器排序的结果是：{sorted(my_set)}")
print(f"字典容器排序的结果是：{sorted(my_dict)}")

print(f"列表容器反向排序的结果是：{sorted(my_list,reverse = True)}") # 反向排序的reverse = True在括号里面。
print(f"元组容器反向排序的结果是：{sorted(my_tuple,reverse = True)}")
print(f"字符串容器反向排序的结果是：{sorted(my_str,reverse = True)}")
print(f"集合容器反向排序的结果是：{sorted(my_set,reverse = True)}")
print(f"字典容器反向排序的结果是：{sorted(my_dict,reverse = True)}")



"""
演示字符串比大小
"""
# abd比较abc
print(f"abd与abc的大小结果是{"abd" > "abc"}")
# a比较ab
print(f"a与ab的大小结果是{"a" > "ab"}")
# a比较A
print(f"a与A的大小结果是{"a" > "A"}")
# key1比较key2
print(f"key1与key2的大小结果是{"key1" < "key2"}")