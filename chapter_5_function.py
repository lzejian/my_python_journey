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