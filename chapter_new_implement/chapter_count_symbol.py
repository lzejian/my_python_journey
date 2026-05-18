"""
运算符的注意点
"""
x = input() # 5
y = input() # 3
print(f"x + y = {x + y}, x - y = {x - y}")
# 得出的结果是TypeError: unsupported operand type(s) for -: 'str' and 'str'，因为input输出的结果是字符串。

x = int(input())
y = int(input())
print(f"x + y = {x + y}, x - y = {x - y}")
# 还是有小陷阱，这个只能运算整数，而不能运算小数。

x = float(input())
y = float(input())
# 这个就能运行整数和小数点了。
# 特殊的如果想运行更多的数学相关的数字或者公式，需要import math库
"""
练习
"""
# 1.计算三个整数的平均数
a = int(input())

# 2.计算梯形面积
Upper_base = float(input())
Lower_base = float(input())
Height = float(input())
print(f"梯形的面积是{(Upper_base + Lower_base) * Height / 2 } ")
#* 首字母不要大写的变量，因为大写的变量是应用到类里的。

# 3.输入⚪的半径，得出面积和周长
import math 
radius = float(input())
perimetre = 2 * math.pi * radius
area = math.pi * radius ** 2 
print(f"圆的周长是{perimetre:.2f}，圆的面积是{area:.2f}")

# 4.身体质量指数BMI的计算 = 体重 / 身高的平方
Height = float(input("请输入你的身高"))
Weight = float(input("请输入你的体重"))
print(f"身体质量指数为{Weight / Height / Height :.2f}")

# 逻辑运算符---and,or,not
n = int(input("请输入你的数字"))

print(f"{n}在10~20之间:",n >= 10 and n <= 20)
# 也可以写成 print(f"{n}在10~20之间:",10 <= n <= 20)