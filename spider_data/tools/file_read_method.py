filename = "somefile.txt"
with open(filename) as f:
    while True:
        line = f.readline()
        if not line:
            print("读取文件结束")
            break
        print(type(line))
        print(line)


with open(filename) as f:
    for line in f:
        print(line)
