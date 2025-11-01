"""
演示while循环的基础应用
"""
i = 0
while i < 100:
    print("小美我喜欢你")
    i += 1
    
# 练习从1+到100
i = 1
j = i + 1
sum = i + j
while i < 99:
    j = j + 1 
    sum = sum + j
    print(sum)
    i  = i + 1
    
# 标准答案   
sum = 0
i = 1
while i <= 100:
    sum += i
    i += 1
print(sum)

####################################
"""
演示while循环的基础案例 --猜数字
"""
import random
num = random.randint(1,100)
# 首先定义一个无限循环的入口和出口
flag = True
# 非常重要！！所谓的记录一共输入了几次，就是看程序跑到猜测之后经历了几次
count = 0
# 无限循环开始，while True
while flag:
    # 猜测一个数字
    guess_number = int(input("请输入你猜测的数字"))
    # 非常重要！！在这里我刚刚猜测了一次，所以count就是1，以此类推2，3...
    count += 1
    if guess_number == num:
        print(f"你猜的非常正确，答案就是{num}")
        # 因为猜测正确，程序终止，设置一个出口也就是Flase，这样它再次走到while的时候和True对不上。
        flag = False
    else:
        if guess_number < num:
            print("你猜测的数字小了")
        else:
            print("你猜测的数字大了")
# 从循环里跳出，最后的输出结果应该与while同层级。因为无论在while下哪里写print都是在循环内部，会一直循环直到终止
print(f"是的结果就是{num}，你一共猜了{count}次")

##############################      
"""
演示while循环的嵌套使用--向小美表白
"""
# 外层变量：表白100天的控制
# 内层变量：每天送10朵玫瑰的控制

i = 1
while i <= 100:
    # 表白循环100次成功。
    print(f"今天是第{i}天，开始表白")
    # 每天送10朵玫瑰花,内层循环。
    j = 1
    while j <= 10:
        print(f"送小美{j}朵玫瑰花")
        j += 1
    i += 1
print(f"今天是表白的第{i - 1}天，表白成功")

######################################
"""
练习案例 --九九乘法表
"""
# 设置外层循环的控制变量
i = 1
while i <= 9:
    # 设置内层循环的控制变量
    j = 1
    while j <= i:
        # 告诉程序输出结果不换行，print()默认输出结果为("结果1，结果2，...",end = "\n")，改变end = "\t"意味程序不换行，因为\n被替换了。并且保持间隔\t。
        print(f"{i} * {j}  = {i * j}",end = "\t") 
        # 等于 print(f"{i} * {j}  = {i * j}\t",end = "")
        j += 1
    i += 1
    # 让每一行输出结束自动换行
    print()
    
##########################################

"""
for循环语法格式
"""
# for 临时变量 in 被处理的数据集（严格来说叫序列类型，例如字符串，列表，元组集合等）:
name  = "lzejian"
for x in name:
    print(x)
# 数一数有几个a，itheima is a brand of itcast
name = "itheima is a brand of itcast"
# 定义一个变量，用来数有多少个a
count = 0
for x in name:
    if x == "a":
        count += 1
print(f"一共出现了{count}次的a")

########################################

"""
演示python中range语句的用法
"""
# range语句1
for x in range(5):
    print(x)
# 结果为01234，默认从0开始数5个数

# range语句2
for x in range(0,5):
    print(x)
# 结果同上，从0开始到4结束

# range语句3
for x in range(2,10,2):
    print(x)
# 结果为2468，最后一个数是间隔的距离。

# 送10次玫瑰花
for x in range(10):
    print("送玫瑰花")
# * x每取到一次range里的数据，就执行一次下面的程序，这才是for循环的精髓。

######################################

"""
python里for循环临时变量的作用域
"""
# 我赋予了i = 1的值，i是个变量
i = 1
# i被强制赋予了值！它在下一个语句里被强制赋予了range(10)的数字，相当于告诉编译器i = 0！！
for i in range(10):
    print(i)

######################################

"""
for循环的嵌套演示
"""
# 设置一个变量，为了最后的print输出符合规范
total_days = 100
for i in range(1,total_days + 1):
    print(f"今天是喜欢小美的第{i}天")
    for j in range(1,11):
        print(f"送小美{j}朵玫瑰")
    print(f"第{i}天表白结束")
print(f"总共表白{total_days}天，表白成功")

##############################################

"""
for循环--99乘法表
"""   
i = 1
j = 1
# 设置外层循环，使行数为9
for i in range(1,10):
    #* 设置内层循环，让该行的数字和小于该行的整数每个都乘一遍。所以是 num <= i!!!!!!
    for j in range(1,i+1):
        print(f"{i}* {j} = {i * j}",end = "\t")
    print()
    
#############################################
"""
continue and break --语法与嵌套
"""
# continue的作用就是不执行下方的代码，但不影响循环。
for i in range(1,6):
    print("皇马")
    continue
    print("巴萨")
# break的作用是中止所在循坏。
for i in range(1,6):
    print("皇马")
    break
    print("巴萨")
# continue 嵌套
for i in range(1,6):
    print("皇家马德里")
    for x in range(1,6):
        print("巴塞罗那")
        continue
        print("拜仁慕尼黑")
    print("国际米兰")
# break 嵌套
for i in range(1,6):
    print("皇家马德里")
    for x in range(1,6):
        print("巴塞罗那")
        break
        print("拜仁慕尼黑")
    print("国际米兰")
#* 总结，continue 和 break都是只作用于位置所在的循环，无法影响到外层循环。
#* 区别CON是终止下方的语句，break是终止所在循环。
       
############################################
"""
练习案例--发工资
"""
# 某公司账户余额1w，给20名员工发工资
# 员工编号1-20，按顺序领取，每人1000
# 领工资时，按绩效分数（随机生成）1-10分领取，小于5分不领取，跳过该员工。
# 工资发完结束就不发了。
# 我的答案
import random
salary = 10000
i = 1
for i in range(1,21):
    num = random.randint(1,10)
    if salary == 0:
        print("工资发完了，请下个月再领取。")
        break
    else:
        if num < 5:
            print(f"员工{i},绩效分{num},低于5,不发工资，下一位")
        else:
            print(f"向员工{i}发放工资1000元,账户余额还剩{salary-1000}")
            salary -= 1000

# 标准答案（更好）
import random
money = 10000
for i in range(1,21):
    # 设置随机数字，如果在外部那就会在循环内固定循环数字。
    num = random.randint(1,10)
    # 小于5则continue终止此次循环，直接进入下一次循环
    if num < 5:
        print(f"员工{i},绩效分{num},低于5,不发工资，下一位")
        continue
    if money >= 1000:
        money -= 1000
        print(f"向员工{i}发放工资1000元,账户余额还剩{money}")
    else:
        print("工资发完了，请下个月再领取。")
        break
#* 代码的层级越少越简洁，并且也要随时应对突然的变故。
#* 我的代码美中不足是ifelse用了两层，并且salary == 0仅在salary为1000的倍数时有效，万一多个500就不管用了。

        
        
        
    
    
