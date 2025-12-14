"""
题目: List Comprehensions (列表推导式与坐标组合)
来源: HackerRank - Basic Data Types
日期: 2025-12-15
作者: lzejian

解题思路:
1. 目标：找出所有可能的 [i, j, k] 坐标组合，其中 0 <= i <= x, 0 <= j <= y, 0 <= k <= z。
2. 限制条件：过滤掉那些 i + j + k 等于 n 的组合。
3. 演进过程：
   - 最初我想用三层嵌套 for 循环 (Nested Loops) 来遍历，像"密码锁"一样一层层转动。
   - 然后在最内层用 if 判断和 (sum) 是否等于 n。
   - 为了符合题目要求并简化代码，我使用了**列表推导式 (List Comprehension)**。
4. 列表推导式公式：`[ 输出结果 for 变量 in 范围 ... if 过滤条件 ]`。
   它把多层循环和判断压缩成了一行，非常 Pythonic！
"""

if __name__ == '__main__':
    x = int(input())
    y = int(input())
    z = int(input())
    n = int(input())

    # --- 方法 1: 列表推导式 (推荐，一行搞定) ---
    # 这里的逻辑顺序是：
    # 1. for i... 
    # 2. for j... 
    # 3. for k... 
    # 4. if i+j+k != n (检查) 
    # 5. 生成 [i, j, k] (打包)
    result = [[i, j, k] for i in range(x + 1) for j in range(y + 1) for k in range(z + 1) if i + j + k != n]
    
    print(result)

    # --- 方法 2: 普通循环写法 (仅作为逻辑参考/草稿) ---
    # my_list = []
    # for i in range(x + 1):
    #     for j in range(y + 1):
    #         for k in range(z + 1):
    #             if i + j + k != n:
    #                 my_list.append([i, j, k])
    # print(my_list)