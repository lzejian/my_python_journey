import textwrap

def wrap(string, max_width):
    result_list = []
    for i in range(0,len(string),max_width):
        result_list.append(string[i:i + max_width])
    return "\n".join(result_list)
        
    return str
if __name__ == '__main__':
    string, max_width = input(), int(input())
    result = wrap(string, max_width)
    print(result)