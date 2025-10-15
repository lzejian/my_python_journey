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

"""
字符串格式化
"""
# 字符串格式化并非真的格式化，而是另一种拼接方式，形为："%s" %(变量)
# %s为占位置，%（变量）就是把变量存储的内容替换到刚刚的占的位置，多个变量依次排列。
# 常用占位符:%s,%d,%f.分别为字符串，整形，浮点型。

# 例：通过占位符完成数字和整形，字符串的拼接
company = "amazon"
set_up_year = 1994
stock_price = 219.93
message = "%s,which is founded in %d with a stock price of %f." %(company,set_up_year,stock_price)
print(message)
print(f"{company},which is founded in {set_up_year} with a price a of {stock_price:.2f}")

# 总结，感觉不如print(f"变量")来的容易，还是用f-string更直接。
# .2f为精度控制保留小数点两位，自动四舍五入，用法是{变量:.2f}。.2%为百分比。
# 10.2f为219.93这个6位字符加上4个空格单位，一般用来对齐。

# 练习
name = "amazon"
stock_price = 219.93
stock_price_daidy_growth_factor = 1.1
growth_day = 7
final_stock_price = stock_price * stock_price_daidy_growth_factor ** growth_day

print(f"公司:{name},股价为{stock_price},每日增长系数是{stock_price_daidy_growth_factor},当经过了{growth_day}后，股价为{final_stock_price:.2f}")


"""
input语句
获取键盘的输入信息
"""
name = input("请告诉我你的身份") # input（）里面自带print的功能
print(f"わかった、あなたは{name}")

# 输入数字类型
num = input("你的银行卡密码是：")

# 输出类型
print(f"你的银行卡类型是{type(num)}") # input输出的类型永远是str，但可以通过变更变量类型来改变。

# 改变类型
num = int(num)
print(f"你的银行卡类型是{type(num)}") # 你的银行卡类型是<class 'int'>



"""
布尔类型，数字类型中的一种，一共有整数型，浮点型，复数型，布尔型4种。
"""
bool_1 = True
bool_2 = False
print(f"bool的字面量有:{bool_1}和{bool_2}。它们的类型分别是{type(bool_1)}和{type(bool_2)}")


# 比较运算符
# == != > < >= <=
"""
比较运算符的使用
"""
# num1= 10
# num2= 5
# print(f"num1 != num2的结果是{num1 != num2}")
# 比较运算符的结果就是布尔类型的True和Flase

"""
if else判断使用
"""


print("欢迎来到黑马儿童游乐场，儿童免费，成人收费")
age = input("请输入你的年龄：")
print(f"{age}岁")
# 需要把age变为整数类型，input输出的内容默认是字符串。
if int(age) >= 18:
    print("你已经成年了，需要补票10元")
else:
    print("你还是个孩子，可以免费游玩")
print("助您玩的愉快")


# print("欢迎来到黑马动物园。")
# height = int(input("请输入你的身高（单位：cm）："))
# if height > 120:
#     print("您的身高超过120cm，可以乘坐过山车")
#     print("祝您玩的愉快")
# else:
#     print("您的身高未超过120cm,不可以乘坐过山车")
#     print("祝您玩的愉快")

# if elif else语句

if int(input("请输入你想的数字：")) == 10:
    print("你猜对啦！")
elif int(input("不对你猜错了，再猜一次：")) == 10:
    print("你猜对啦！可以的")
elif int(input("不对你猜错了，再猜最后一次：")) == 10:
     print("你猜对啦！还行吧")
else:
    print("你真笨，三次都没猜对！答案是10")

# 
# name = input("请输入你的名字:")
# print(f"{name}")
