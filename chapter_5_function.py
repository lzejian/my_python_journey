"""
函数的定义
"""
# def 函数名(参数):
#     函数体
#     return返回值
def check():
    print("请出示你的收款码！")

check()
###############################
"""
演示函数的传参
"""
# 定义函数的形式参数x,y
def add(x,y):
    result = x + y
    print(f"{x}+{y}的结果是{result}")
# 执行函数的实际参数5，6
add(5,6)
#################################
"""
函数传参的练习
"""
def temp(x):
    if x<=37.5:
        print(f"您的体温正常，小于{x}度，可以进入")
    else:
        print(f"你的体温是{x}度，需要隔离！")
temp(45)
##################################
"""
函数返回值的演示
"""
def add(x,y):
    result = x + y
    return result
r = add(5,6)
print(r)
#* 简而言之，当我需要这个函数产生的结果时，我就需要这个return来接收它
#* 当我只需要这个函数完成动作即可，就不需要return把值返还出来给我用。像上面的print一样

#####################################
"""
函数的None返回值
"""
def add(x,y):
    result = x + y
    # if 这里我不写 return result
r = add(5,6)
print(r)
print(type(r))
# 输出值为None.因为不写默认为return None
# 类型为Nonetype
# None 可以用于if判断
def check_age(x):
    if x > 18:
        return "success"
    # return丢出一个值"success"，也是产生了一个结果,它可以写任何值。
    else:
        return None
result = check_age(16)
# result = check_age(16) = None = flase,任何非None的值都是True
if not result:
    print("未满18周岁，不得进入")

# none也可以用于存储空的值
name = None

########################################
"""
演示对函数进行文档说明---规范美观
"""
# 定义函数，进行文档说明
def add(x,y):
    """
    1.add函数是两个参数相加的函数。
    2.param x:用来存放第一个函数的参数
      param y:用来存放第二个函数的参数
    3.:return:函数返回值的说明
    """
    # 函数体
    result = x + y
    return result
add(5,6)

###############################
"""
演示函数的嵌套调用
"""
# 定义一个准备嵌套的函数f2
def function_2():
    print("-----2-----")
# 定义一个被嵌套的函数f1
def function_1():
    print("-----1-----")
    function_2()
    print("-----3-----")
function_1()
# 调用f_1，先输出f_1的内容，再调用f_2，有逻辑的一个一个来。

#######################################

"""
函数中变量的作用域
"""
# 局部变量
def test_1():
    num = 100
    print(f"{num}")
test_1()
print(f"{num}")
# 局部变量就是只在函数内生效，出去就失效的变量。

# 全局变量
num = 200
def test_2():
    print(num)
def test_3():
    print(num)
test_2()
test_3()
print(num)
# 全局变量设置在函数外，函数随意使用后出去也是可以使用。

# global关键字，把局部变为全局变量
num = 100
def test_4():
    if num > 100:
        return "pass"
    else:
        return None
def test_5():
    global num
    num = 5000
    print(num)
test_5()
r = test_4()
if not r:
    print("reject")
else:
    print("okpass")
#* 程序是自上向下走的，并非我设置了一个global，最开始的global就变成了5000，谨记！！！

########################################
"""
综合案例 ---ATM机
"""

money = 5000000
flag = True
def main_menu():
    print("-----------主菜单--------------")
    print(f"您好,{name},欢迎来到银行ATM,请选择操作")
    print(f"查询余额\t[输入1]")
    print(f"存款\t[输入2]")
    print(f"取款\t[输入3]")
    print(f"退出\t[输入4]")
    num = int(input("请输入您的选择:"))
    return num
def check_balance():
    print(f"您的余额还剩{money}")
def deposit():
    x = int(input("请输入您想存的金额数量:"))
    global money
    money += x
    print(f"您的余额还剩{money}元")
def withdraw():
    global money
    #* global如果有多个相同变量，那么它必须放在第一个相同变量前！这是python的规则。
    y = int(input("请输入您想取的金额数量:"))
    if money - y < 0:
        print("您取的金额大于存储金额，请重试")
    else:
        money -= y
        print(f"您的余额还剩{money}元")
def exit_program():
    print(f"好的，程序将会退出。")
# 函数定义完成开始写循环条件
name = input("请输入你的姓名:")
while flag:
    num = main_menu()
    if num == 1:
        check_balance()
        continue
    if num == 2:
        deposit()
        continue
    if num == 3:
        withdraw()
        continue
    if num == 4:
        exit_program()
        break
    else:
        print("输入结果错误，程序将退出。")
        break
    




    




