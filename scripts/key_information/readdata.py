import sys

f = open("data.txt", "r")
lines = f.readlines()
f.close()

l = []

for line in lines:
    l.append(eval(line))

word = sys.argv[-1]
print (word)

count = 0
for data in l:
    if int(data[-3]) == int(sys.argv[-2]):
        count += 1
        if word in data[-1]:
            print (data[2])
            print ("-----------")

print (count)
