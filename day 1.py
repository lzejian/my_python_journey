"""
字符串转换
"""
# 将数字类型转换成字符串
num_str = str(11)
print(f"类型是:{type(num_str)}，变量是:'num_str'")  # ""代表print这个函数执行的全部内容，print括号里面如果想出现"num_str"那么必须改成''或者f后接''
print(f'类型是:{type(num_str)}，变量是:"num_str"')  # f后的内容并非一定为""
print(f"类型是:{type(num_str)}，变量是:\"num_str\"") # 加入转义字符\告诉print函数\后面的符号就是个字面量，并非字符串的起始和结束标记

# 将字符串转换成数字
int_num = int("1065071625")
print(f"类型是:{type(int_num)}，变量是:{int_num}") # 如果是int("lzejian1543")这种的就不行了，因为字符串转数字只能里面带数字才可以。

# 将数字和浮点数互相转换
float_num = float(27)
print(f"类型是:{type(float_num)}，变量是:{float_num}")
int_num = int(1996.0127)
print(f"类型是:{type(int_num)}，变量是:{int_num}") # 会省略后面的0127

# 总结：任何类型都可以转换成字符串，但是字符串并不可以随意转换成其他的类型。



"""
标识符 用户在敲代码时，对变量；类；方法编写的名字，叫做标识符
"""
# 规则1 内容限定：只能使用英语，中文，数字，下划线。注意：不可以用数字开头！

# 规则2 大小写敏感
Lzejian = "帅哥"
lzejian = 666
print(Lzejian,lzejian)

# 规则3 不可使用关键字
# 错误示范：class = 1 正确示范: Class = 1

# 命名规范 ： 变量的首字母应小写，做到见名知意。


"""
运算符
"""

# 算数运算符
print(f"1+1 = {1+1}")
print(f"1*1 = {1*1}")
print(f"1-1 = {1-1}")
print(f"9/2 = {9/2}")
print(f"9%2 = {9%2}")    # 取余数
print(f"9//2 = {9//2}")  # 取整除
print(f"9**2 = {9**2}") 

# 赋值运算符: = 
num = 9**2//4
print(num)

# 复合赋值运算符
#就是算数运算符后面加 = ，例如c += a等价于c = c + a

"""
字符串扩展
"""

# 字符串的拼接
print("我的名字是"+"吕泽舰") # 这是字符串中字面量的拼接

# 字符串字面量与变量的拼接
name = "lzejian"
address = "shenyang"
tel = 15541958237 # 数字是不能拼接的，只能拼接字符串。
print("my name is " + name + ",address is "+address)

"""
git
"""
# git add并非是单纯的添加，而是把工作区的内容记录下来，就像打扫屋子我撕了一张海报detele或者搬走一台显示器modify，他会在提交前记录一下这个行为。
# git的核心思想是track changes，所以即使是删除文件也需要记录行为并commit。


















# bool_1 = True
# bool_2 = False
# print(f"bool的字面量有:{bool_1}和{bool_2}。它们的类型分别是{type(bool_1)}和{type(bool_2)}")


# 比较运算符
# == != > < >= <=
"""
比较运算符的使用
"""
# num1= 10
# num2= 5
# print(f"num1 != num2的结果是{num1 != num2}")

# 20


# print("欢迎来到黑马儿童游乐场，儿童免费，成人收费")
# age = input("请输入你的年龄：")
# print(f"{age}岁")
# if int(age) >= 18:
#     print("你已经成年了，需要补票10元")
# else:
#     print("你还是个孩子，可以免费游玩")
# print("助您玩的愉快")


# print("欢迎来到黑马动物园。")
# height = int(input("请输入你的身高（单位：cm）："))
# if height > 120:
#     print("您的身高超过120cm，可以乘坐过山车")
#     print("祝您玩的愉快")
# else:
#     print("您的身高未超过120cm,不可以乘坐过山车")
#     print("祝您玩的愉快")

# if elif else语句

# if int(input("请输入你想的数字：")) == 10:
#     print("你猜对啦！")
# elif int(input("不对你猜错了，再猜一次：")) == 10:
#     print("你猜对啦！可以的")
# elif int(input("不对你猜错了，再猜最后一次：")) == 10:
#      print("你猜对啦！还行吧")
# else:
#     print("你真笨，三次都没猜对！答案是10")

# 
# name = input("请输入你的名字:")
# print(f"{name}")
