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
        
            


    