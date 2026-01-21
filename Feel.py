f = open("sample.txt", "w+")
f.write("PythonFileHandling")
f.seek(0)

print("Initial Position:", f.tell())

data1 = f.read(6)
print("Read Data:", data1)
print("Position after read:", f.tell())

f.seek(0)
data2 = f.read(6)
print("After seek, Read Data:", data2)
print("Final Position:", f.tell())

f.close()
