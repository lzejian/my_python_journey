# map规则 ---映射，把前项的效果映射到后面的字面量上
my_list = input().split()
new_my_list = list(map(int,my_list[1:]))
**注意**
map是迭代器，是一种规则，它必须要加上存储器才行。


--------------------------------------------------------

# range函数 ---范围
range(10)虽然也是包头不包尾，但是也是实打实的10个数字（0~9）

--------------------------------------------------------


# hash()函数 --- 数据的“数字指纹” (Digital Fingerprint)
t = (1, 2)
print(hash(t))  # 输出一个唯一的整数，例如 371308...

# **核心逻辑**
# 作用：给对象生成一个唯一的整数 ID，常用于快速比较或作为字典的 Key。

# **关键限制 (必考点)**
# 只能用于【不可变类型】(Immutable Types)：
# ✅ 元组 (tuple)、字符串 (str)、数字 (int) -> 这里的指纹是固定的。
# ❌ 列表 (list)、字典 (dict) -> 报错 TypeError: unhashable type。
#    (因为列表是可变的，内容变了指纹就会变，所以系统拒绝给它算 hash)


--------------------------------------------------------


# join()函数 --- 字符串“胶水” (String Glue)
words = ["Hello", "World"]
print("-".join(words))    # 输出: "Hello-World"
print("".join(words))     # 输出: "HelloWorld" (无缝拼接，算法题常用)

# **核心逻辑**
# 公式： "胶水".join(碎片列表)
# 作用：把列表变成字符串。它是 split() 的反义词。
# split: 字符串 -> 列表 ✂️
# join:  列表 -> 字符串 🧪

# **关键限制 (必考点)**
# 列表里的元素必须全都是【字符串(str)】！
# ❌ nums = [1, 2, 3] -> "-".join(nums) 报错 TypeError
# ✅ 解决方案：配合 map() 使用
#    "-".join(map(str, nums)) -> "1-2-3"


--------------------------------------------------------


# 对称差集 (Symmetric Difference) --- 取两边的“独家”元素
s1 = {1, 2, 3}
s2 = {2, 3, 4}

# 写法 1：使用方法 (Method)
print(s1.symmetric_difference(s2))  # 输出 {1, 4}

# 写法 2：使用运算符 (Operator) -> 最推荐！🐍
print(s1 ^ s2)                      # 输出 {1, 4}

# **核心逻辑**
# 也就是：(A ∪ B) - (A ∩ B) 或者 (A - B) ∪ (B - A)
# 记忆口诀：两个集合“找不同”。
# 符号记忆：^ (异或符号)，在计算机里代表“不一样就是 True (1)”。


--------------------------------------------------------

# 字符串大小写判断 (Case Checking)
s_upper = "PYTHON"
s_lower = "python"

# 4. 判断是否全是大写 🔍
print(s_upper.isupper())  # 输出: True
print(s_lower.isupper())  # 输出: False

# 5. 判断是否全是小写 🔍
print(s_lower.islower())  # 输出: True
print(s_upper.islower())  # 输出: False

# **核心逻辑**
# 这些方法返回的是布尔值 (Boolean): True 或 False。
# 区别记忆：
# .upper() 是“动作”，把字变大。
# .isupper() 是“问题”，问是不是大写。

# 6. 大小写互换 (Case Swapping)
s = "Hi Python"
print(s.swapcase())   # 输出: "hI pYTHON"

# **核心逻辑**
# 作用：大写变小写，小写变大写。
# 场景：专门用于 "Swap Case" 这类题目，一行代码顶十行逻辑！
# 注意：它也是返回新字符串，不会修改原字符串。

--------------------------------------------------------

# 逻辑判断函数 --- any() 和 all()

# 1. any() --- 只要有一个 True 就算赢 🥉
# 场景：检查“是否存在”、“有没有”。
print(any([False, True, False]))  # -> True
# 实战：字符串里有没有数字？
has_digit = any(c.isdigit() for c in s)

# 2. all() --- 必须全都是 True 才算赢 🥇
# 场景：检查“是否全部符合”、“大家都是”。
print(all([True, True, True]))    # -> True
print(all([True, False, True]))   # -> False (有一个老鼠屎就坏了一锅粥)
# 实战：字符串是不是纯由数字组成？
all_digits = all(c.isdigit() for c in s)

# **核心逻辑**
# any:  OR 逻辑 (或者) -> 只要有一个符合。
# all:  AND 逻辑 (并且) -> 必须全部符合。
# 它们都有“短路机制”，一旦结果确定就会立刻停止，非常快。

--------------------------------------------------------

# Python 字符串与循环进阶笔记 🚀

## 1. 换行符 `\n` (Newline)
* **本质**：一个看不见的“回车”指令。
* **用途**：
    1.  **打印分行**：`print("A\nB")`
    2.  **拼接胶水**：用它把列表变成竖排文本。
        ```python
        lines = ["Line 1", "Line 2"]
        print("\n".join(lines)) 
        # 结果：
        # Line 1
        # Line 2
        ```

## 2. 排版神器 `textwrap`
* **场景**：需要把长文本自动切分、换行时。
* **用法**：
    ```python
    import textwrap
    # fill = 切割 + 拼接 (最省事)
    print(textwrap.fill(long_string, width=50))
    ```

## 3. Range 的魔法步长 (Step) 🪄

`range(start, stop, step)` 是处理“间隔”和“倒序”的神器。

### A. 正向跳跃 (每隔 N 个取一个)
* **公式**：`range(0, len(s), N)`
* **逻辑**：从头开始，每次跳 N 步。
* **实战**：每 5 个字切一刀。
    ```python
    # 假设 s = "ABCDEFGHIJ", N = 5
    for i in range(0, len(s), 5):
        print(s[i : i+5]) 
    # i 依次为 0, 5。自动切片 s[0:5], s[5:10]
    ```

### B. 反向倒车 (倒序每隔 N 个) ⚠️
* **公式**：`range(len(s)-1, -1, -N)`
* **逻辑**：**从尾巴开始**，倒着跳，**直到 -1 停止**。
* **参数详解**：
    * `start`: `len(s)-1` (最后一个字符的下标)
    * `stop`: `-1` (为了能取到下标 0，必须写 -1)
    * `step`: `-1` (倒着一个一个走) 或 `-2` (倒着跳着走)
* **实战**：倒着打印字符串。
    ```python
    s = "Hello"
    # 从下标 4 开始，走到 -1 停，每次减 1
    for i in range(len(s)-1, -1, -1):
        print(s[i]) # 依次打印 o, l, l, e, H
    ```

### 💡 极简替代方案：切片 (Slicing)
如果你不需要在循环里做复杂逻辑，只想单纯把字符串倒过来，切片比 `range` 更简单：
* **正向跳跃**：`s[::2]` (每隔 2 个)
* **倒序全取**：`s[::-1]` (经典倒序)
* **倒序跳跃**：`s[::-2]` (倒着每隔 2 个)

--------------------------------------------------------

# Assuming we have: list_i (array), set_a, and set_b

# Option 1: Calculate separately and subtract (推荐：逻辑最清晰)
# (Total Positive) - (Total Negative)
print(sum(1 for x in list_i if x in set_a) - sum(1 for x in list_i if x in set_b))

# Option 2: Calculate using +1 and -1 (和你的思路一致)
# (Sum of 1s) + (Sum of -1s)
print(sum(1 for x in list_i if x in set_a) + sum(-1 for x in list_i if x in set_b))

--------------------------------------------------------

# 🐍 Python 字符串格式化与进制转换学习笔记

## 1. 循环遍历的陷阱 🔄
* **错误示范**：`for i in n:` (如果 `n` 是整数)
    * **原因**：整数 (int) 是不可迭代的（就像一个苹果不能被当作一串葡萄一个一个摘）。
* **正确做法**：`for i in range(1, n+1):`
    * **原理**：使用 `range()` 生成一个数字序列。

## 2. 进制转换：函数 vs f-string ⚖️

### A. 使用内置函数 (自带前缀)
* `bin(10)` -> `'0b1010'` (二进制)
* `oct(10)` -> `'0o12'` (八进制)
* `hex(10)` -> `'0xa'` (十六进制)
* **特点**：适合调试，但包含 `0b`, `0o`, `0x` 前缀，通常需要切片处理 (`[2:]`)。

### B. 使用 f-string 格式化 (推荐 ⭐️)
在 f-string 中使用冒号 `:` 加上指令，可以自动**去除前缀**并控制**大小写**。

```python
n = 10
print(f"{n:b}")  # 输出: 1010 (Binary)
print(f"{n:o}")  # 输出: 12   (Octal)
print(f"{n:x}")  # 输出: a    (Hex, 小写)
print(f"{n:X}")  # 输出: A    (Hex, 大写)

-------------------------------------------------------- 

