import sys

fileName = sys.argv[1]

with open(fileName + ".txt", 'r', encoding='utf-8') as f:
    txt1 = f.read()

with open(fileName + "-desc.txt", 'r', encoding='utf-8') as f:
    txt2 = f.read()

print(txt1 == txt2)