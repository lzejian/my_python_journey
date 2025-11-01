"""
演示json数据和python字典列表之间的相互转换
"""
import json # json就是像英语一样可以在不同语言之间传递数据的数据交互格式，它是一种特定格式的字符串

# 准备列表，列表内每个元素都是字典，将其转化位json
J  = [{"name" : "吕泽舰","age" : "29"},{"name" : "单嘉琦","age" : "29"}]
l = json.dumps(J,ensure_ascii = False) # 输入ensure_ascii = Flase之后，name后的内容就会变为中文，不会再是\u5415\u6cfd\u8230
print(f"l的数据类型是{type(l)}")
print(l)

# 准备字典，将字典变成json
d = {"吕泽舰":"29","addr":"沈阳","王京媛":"27","addr":"白山"}
l = json.dumps(d,ensure_ascii = False) # 输入ensure_ascii = Flase之后，name后的内容就会变为中文，不会再是\u5415\u6cfd\u8230
print(f"l的数据类型是{type(l)}")
print(l)

# 将json字符串变成python数据类型[{}]
str1 = '[{"name" : "吕泽舰","age" : "29"},{"name" : "单嘉琦","age" : "29"}]' # 一般来说字符串双引号单引号都可以，但是json里为了区分得用单引号
print(f"数据类型是{type(json.loads(str1))}")
print(json.loads(str1))

# 将json字符串变成python数据类型{}
str2 = '{"吕泽舰":"29","addr":"沈阳","王京媛":"27","addr":"白山"}'
print(f"数据类型是{type(json.loads(str2))}")
print(json.loads(str2))