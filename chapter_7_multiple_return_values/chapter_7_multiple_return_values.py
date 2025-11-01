"""
演示函数的多返回值示例
"""
def test_return():
    return 1,"lzejian",2 > 3 # 函数只能返回一个值，但这个值可以是一个元组，所以return的结果是tuple(1,"lzejian",2 > 3)
x,y,z = test_return() # 这一步是解包元组中的值，解包变量数要匹配否则会出错。
a,_,b = test_return() # 如果不想要中间这个值，可以用_表示占位置。
print(x,y,z)
print(a,b)

"""
演示多种传参方式
"""
# 位置传参，就是和参数一对一的放入信息，会按照顺序显示
def user_infor(name, age,gender):
    print(f"用户的名字是{name},年龄是{age}，性别是{gender}")
user_infor("吕泽舰",29,"男")

# 关键字传参
user_infor(age = 29,name = "吕泽舰",gender = "男") # 关键字可以不按照顺序写参数
user_infor("吕泽舰",age = 29,gender = "男") # 如果有位置传参和关键字传参混合，那么最后一个必须是关键字

# 缺省传参 （设置默认值必须放在最后一个，只要最后一个有，前边可有可无）
def user_infor(name, age,gender = "男"): 
    print(f"用户的名字是{name},年龄是{age}，性别是{gender}")
user_infor("吕泽舰",29)               # 可以不写第三个参数，不写就代表参数一直都是"男"
user_infor("单嘉琦",29,gender = "女") # 也可以修改第三个参数，只需要 = 赋值即可

# 不定长 - 位置不定长（不定长*的形式参数会作为元组存在，可以任意写多个参数）
def user_infor(*args):
    print(f"参数*args的类型是{type(args)},输出的内容是{args}") # args不是必须写法，可以写任意值，只是默认这么写
user_infor(1,2,"lzejian",2>3) # 输出的内容是一个元组

# 不定长 - 关键字不定长（不定长**的形式参数会作为字典存在，可以任意写多个参数，但必须是key = value的形式）
def user_infor(**kwargs):
    print(f"参数*args的类型是{type(kwargs)},输出的内容是{kwargs}")
user_infor(name = "吕泽舰",age = 29,addr = "沈阳")

"""
演示函数作为参数传递
"""

# 定义一个函数，接收另一个函数传入参数
def test_func(compute):
    result = compute(1,2) # compute(1,2)是函数的写法 ，这一步的目的是把compute确定为函数，它的结果是一个值
    print(f"compute的类型是{type(compute)},计算结果是{result}")
# 定义一个函数，准备作为参数传入上边的函数
def add(x,y):
    return x + y
# 调用函数
test_func(add) # 相当于把一个计算逻辑当作工具给compute使用，因为compute虽是函数，但没有逻辑。

"""
匿名函数 lambda λ
"""
# lambda函数只能用一次，不可重复使用
# 用法 lambda 传入参数:函数体（只能是一行代码）
def test_func(compute):
    result = compute(1,2) 
    print(f"计算结果是{result}")
test_func(lambda x , y : x + y)

print("计算结果是",(lambda x , y : x + y)(10,20)) 
print((lambda name: f"Hello, {name}")("Python"))  # f"Hello, {name}"可以当作函数体，即使没有任何意义，就是个字面量

# 非常好的例子，理解函数传参
def hello(name):
    print(f"Hello, {name}!")

def call_func(f):
    f("Python")   # 函数可以没有逻辑！！！！这里为什么f可以，但是写123("Python")就不可以，因为诸如整数，列表，字符串这种都不可以当作函数，就是形式不允许。
                  # 而函数的基本形式就是print("hi")，	str(123)，	(lambda x: x+1)(5)，所以f即使没有任何意义，语法也是允许的。
call_func(hello)  # 输出：Hello, Python!

