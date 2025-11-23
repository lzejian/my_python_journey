# map规则 ---映射，把前项的效果映射到后面的字面量上
my_list = input().split()
new_my_list = list(map(int,my_list[1:]))
**注意**
map是迭代器，是一种规则，它必须要加上存储器才行。

# range函数 ---范围
range(10)虽然也是包头不包尾，但是也是实打实的10个数字（0~9）