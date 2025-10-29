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