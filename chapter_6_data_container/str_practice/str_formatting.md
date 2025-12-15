"""
题目: String Formatting (字符串格式化与对齐)
来源: HackerRank - Strings
日期: 2025-12-16
作者: lzejian

解题思路:
1. 目标：将数字 1 到 n 打印出来，每一行包含四个部分：十进制(Decimal)、八进制(Octal)、十六进制(Hexadecimal)、二进制(Binary)。
2. 对齐要求：每一列都需要根据"二进制形式的宽度"进行右对齐，中间用一个空格隔开。
3. 关键难点 (Pitfalls)：
   - **宽度计算**：如果使用 `len(bin(n))`，会包含 '0b' 前缀，导致宽度偏大（空格太多）。
   - **解决方法**：使用 `len(f"{n:b}")` 只获取纯数字部分的长度。
4. 格式化技巧 (f-string)：
   - 语法：`{变量:{宽度}{类型}}`
   - 类型代码：`d` (十进制), `o` (八进制), `X` (大写十六进制), `b` (二进制)。
   - **显式优于隐式**：虽然十进制默认不需要 `d`，但为了和后面保持队形统一，写上 `d` 更好。
"""

def print_formatted(number):
    # 1. 计算宽度 (Width Calculation)
    # 注意：不要用 len(bin(number))，因为那会把 '0b' 也算进去 (比如 0b10 长度是4)
    # 使用 f"{number:b}" 直接拿到不带前缀的二进制字符串 (比如 10 长度是2)
    width = len(f"{number:b}")

    # 2. 遍历打印 (Loop & Print)
    for i in range(1, number + 1):
        # 使用 f-string 进行统一格式化
        # {i:{width}d} -> 这里的 d 代表 Decimal，虽然是默认值，但写上表示强调"十进制"
        # 花括号中间的空格 " " 就是题目要求的 Single Space
        print(f"{i:{width}d} {i:{width}o} {i:{width}X} {i:{width}b}")

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)