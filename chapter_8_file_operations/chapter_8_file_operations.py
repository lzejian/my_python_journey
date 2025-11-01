"""
演示对文件的操作
"""

# 打开文件 （形式是open（"路径"，"方式",....））
# f = open(r"E:/python/python self learning/test.txt","r",encoding = "UTF-8")
   # 前两个是必须有的要素，所以位置传参，encoding不是必须的，也不是第三个，所以是关键字传参。r是让里面的转义字符失效。

# 读取文件 - read （读取的结果为字符串）
# print(f"文件的前10个字节是:{f.read(10)}") # 读取前10个字节 君の前前前世から
# print(f"文件的读取全部内容是:{f.read()}")  # 读取的是上个文件之后剩下的！僕は君を探し始めたよそのぶきっちょな笑い方をめがけて、やってきたんだよ

# 读取文件 - readlines 【读取全部行，并变成列表，一行是一个元素】
# print(f"文件变成列表后是:{f.readlines()}") # ['  君の前前前世から僕は君を探し始めたよ\n', 'そのぶきっちょな笑い方をめがけて\n]
# print(f"line对象的内容是{type(f.readlines())}") # 结果是list

# 读取文件 - readline （会读取一行）
# line1 = f.readline()
# line2 = f.readline()
# print(f"第一行文件的内容是:{line1}")
# print(f"第二行文件的内容是:{line2}")

# for循环读取文件行
# for line in f:
#     print(f"for循环遍历后每一行的内容是:{line}")

# 文件的关闭 （如果不关闭文件，那么文件将持续的被python占用，不能更改。）
# f.close() # 程序关闭

# with open语法操作文件 (输入操作之后自动关闭文件，可以对文件进行改动。)
# with open(r"E:\python\python self learning\test.txt","r",encoding = "utf-8") as f:
#     for line in f:
#         print(f"for循环遍历后每一行的内容是:{line}")

"""
test
"""
# 方法一
# f = open ("E:\python\python self learning\word.txt","r",encoding = "utf-8")
#     # print((f.readlines())) 错误：因为这相当于调用了一次文本，直接把指针给调到了文本最后面。
# list1 = f.readlines()
# count  = 0 
# for x in list1: # 这句话的意思是，x就是直接变成了list1当中的每一个变量，对每一个在list1中的元素，都赋值x一个一个操作。
#     # count += list1.count("itheima") 错误：count前面并非只能放列表，也可以放列表中的元素例如字符串。
#     count += x.count("itheima") # 结果一共是6个
# f.close()
# print(f"一共有{count}个元素")
# # 方法二

# with open("E:\python\python self learning\word.txt","r",encoding = "utf-8") as f:
#     lines = f.read()
# print(f"一共有{lines.count("itheima")}个元素")

# 总之，在list列表里count查找元素，只能找完全一模一样的元素，但是在str字符串中找，可以在母字符串中找小字符串。


"""
演示文件的写入 w模式
"""
# 打开文件 - 创造一个不存在的文件
import time

f = open(r"F:\visual studio code\python\python self learning\day 6 对文件的操作/write.txt","w",encoding = "UTF-8")

# write 写入 
f.write("hello,world!!!") # 会将内容写入缓冲区，不放在硬盘里，从time函数里就能看见。
# time.sleep(600000) # 让程序运行600秒，程序不结束，write内容就一直在内存不放入硬盘中。

# flush 刷新 （内容写入到硬盘中）
# f.flush()
# time.sleep(600000) # 让程序待机，也能发现内容已经进入硬盘了

# close 关闭 （close函数自带flush功能）
f.close()

# 打开一个存在的文件
f = open(r"F:\visual studio code\python\python self learning\day 6 对文件的操作/write.txt","w",encoding = "UTF-8")

# write写入 flush刷新 # close关闭
f.write("愛してる")
f.write("君をずっと")  # 结果是"愛してる君をずっと，在一个f.write中写入的内容会覆盖掉之前的内容。连续写会将内容追加在后面。
# f.flush()  # 这句可以不写，因为close自带flush功能
f.close()   
# w 模式下，如果文件不存在，则会创建一个文件
# w 模式下，如果文件存在，则会清空原有内容。


"""
演示文件的写入 a模式
"""
# f = open(r"E:\python\python self learning\append.txt","a",encoding = "UTF-8")
# f.write("君をずっと")
# f.flush()
# f.write("愛してる")
# ｆ.close()
# a模式下，如果文件不存在，则会创建一个文件。
# a模式下，如果文件存在，则会追加一个文件。




