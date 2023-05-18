import math
import sys
import os

def decoder(encoded, n):
    txt_len = int(encoded[:32],2)
    alpha_len = int(encoded[32:48], 2) * 7
    print("El txt_len és ", txt_len, " i el alpha_len és ", alpha_len)
    alpha = []
    src = {}
    total = 0
    for i in range(48, 48+alpha_len, 7):
        lletra = int(encoded[i:i+7], 2)
        print(lletra)
        lletra = chr(lletra)
        print(lletra)
        alpha.append(lletra)
        src.update({lletra:1})
        total += 1
    code = encoded[48+alpha_len:]

    print("El source és:", src, " i l'alpha és:", alpha, " i el total és ", total)

    

fileName = sys.argv[1]
with open(fileName, 'r') as f:
    txt = f.read()

decoded = decoder(txt, 1)

#with open(os.path.splitext(fileName)[0] + ".og", 'w') as f:
#    f.write(decoded)