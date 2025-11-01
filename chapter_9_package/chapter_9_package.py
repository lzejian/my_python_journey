"""
演示捕获异常
"""

# 基本捕获语法
# try:  # 可能出现异常的地方
#     f = open(r"E:\python\python self learning\error.txt","r",encoding = "UTF-8")
# except: # 如果出现了异常该怎么办
#     print("出现异常了，文件不存在，我将以\"w\"模式打开它。")

# # 捕获指定异常
# try:
#     print(Name)
# except NameError as a:
#     print("捕获到指定异常----变量未定义的异常")

# # 捕获多个异常
# try:
#     1/0
# except(NameError,ZeroDivisionError) as b:
#     print("捕获到多个异常----除零异常或变量未定义异常")
    
# # 捕获所有异常
# try:
#     f = open(r"E:\python\python self learning\error.txt","w",encoding = "UTF-8")
# except Exception as c:
#     print("出现异常了")
# else:
#     print("我是else，没有出现任何异常，开心")
# finally:
#     print("我是finally，不管有没有异常，都得执行我这个程序，一般是f.close()这种结尾写的程序")
#     f.close()

"""
演示异常的传递性
"""

# 定义一个有异常的函数
# def func1():
#     print("func1开始执行") # 正常运行到这里
#     1/0
#     print("func1执行结束")
# # 定义一个无异常的函数
# def func2():
#     print("func2开始执行") 
#     func1()  # 正常运行到这
#     print("func2结束执行")
# def main():
#     # func2() # 如果执行这个，最后结果就是执行1/0报错的结果
#     try:
#         func2()  # 正常运行，找func2
#     except Exception as a :
#         print(f"程序报错的异常信息是：{a}")

# main()


"""演示python模块的导入"""

# 模块就是一个代码文件以.py结尾存放在python自己的编译器中，例如import.time的time就是time.py

# 使用import导入time模块使用sleep功能的函数
# import time # ctrl+左键点击time就可以看到内置的函数了
# print("你好")
# time.sleep(5)
# print("我好")  # 5秒后显示我好。

# 使用from导入time的sleep功能
# from time import sleep
# print("你好")
# sleep(5)
# print("我好") # 这种写法可以不写模块time，直接写time中的函数sleep

# 使用*导入time函数的全部功能
# from time import *
# print("你好")
# sleep(5)
# print("我好") # 这种写法和import time功能相同，但是不用写time

# # 使用as给功能加别名，为了简化某些太长的函数名
# from time import sleep as sl

# print("你好")
# sl(5)
# print("我好")
"""----------------分割线-----------------"""
# import time as t

# print("你好")
# t.sleep(5)
# print("我好")


"""自定义模块导入使用"""

# 自定义模块导入使用
# 1. 在当前目录下创建一个文件，命名为mymodule.py
# 2. 在mymodule.py中编写一些函数
# import my_module1
# my_module1.test(1, 2)  # 调用my_module1中的test函数，传入参数1和2
# from my_module1 import test  # 从my_module1模块中导入test函数
# test(3, 4)  # 调用导入的test函数，传入参数3和4

# 导入不同模块的同名功能
# from my_module1 import test
# from my_module2 import test
# test(9,1)  # 同一个函数名的功能，调用的会是最后一个模块里的内容。

# __main__变量
# 写法为 if __name__ == "__main__": 写在test(1, 2)my_module1.py里
    # test(1, 2)
# 这种写法的作用是，当这个模块被直接运行时，__name__的值为"__main__"，而当这个模块被其他模块导入时，__name__的值为模块名。
# 这样可以避免在导入时执行不必要的代码。
# from my_module1 import test
# test(1, 2)

# __all__变量
# 在my_module1.py和my_module2.py中定义__all__变量，指定哪些函数可以被导入,它只对使用from ... import *语句有效。把*换成函数就无效了
# from my_module1 import *
# test1(5, 6)
# test2(7, 8)   # test2函数不会被导入，因为my_module1.py中定义了__all__变量，只导入了test1函数。from my_module1 import test2就没问题了。



"""
演示python的包
"""
# 创建一个包，包的目录结构如下：
# mypackage/
# ├── __init__.py
# ├── my_module1.py
# └── my_module2.py


# 导入自定中的模块并使用
# from my_package import my_module3
# from my_package import my_module4
# my_module3.infor_print1()  # 调用my_module3中的infor_print1函数
# my_module4.infor_print2()  # 调用my_module4中的infor_print2函数
# from my_package import my_module3, my_module4
# my_module3.infor_print1()  # 调用my_module3中的infor_print1函数
# my_module4.infor_print2()  # 调用my_module4中的infor_print2函数

# 通过__all__变量控制import *
from my_package import *
my_module3.infor_print1()  # 调用my_module3中的infor_print1函数
#  my_module4.infor_print2()  # 此时就会报错，因为my_module4没有在__all__中定义
