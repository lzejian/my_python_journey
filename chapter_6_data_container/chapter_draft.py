record = []
n = int(input())
for x in range(n):
    name,score = [input(),float(input())]
    record.append([name,score])
print(record)

my_arr = set()
for x in record:
    my_arr.add(x[1])
new_my_arr = sorted(my_arr)
name = []
for x in record:
    if x[1] == new_my_arr[1]:
        name.append(x[0])
name = sorted(name)
for students in name:
    print(students) 
        
    
            