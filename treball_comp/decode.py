import math
import sys
import os

def dec2binary(a, k):
    binary = bin(a)[2:]
    padded_binary = '0'*(k-len(binary)) + binary  
    return padded_binary

def decoder(encoded, n):
    txt_len = int(encoded[:32],2)
    alpha_len = int(encoded[32:48], 2) * 7
    print("El txt_len és ", txt_len, " i el alpha_len és ", alpha_len)
    alpha = []
    src = {}
    total = 0
    for i in range(48, 48+alpha_len, 7):
        lletra = int(encoded[i:i+7], 2)
        lletra = chr(lletra)
        alpha.append(lletra)
        src.update({lletra:1})
        total += 1
    code = encoded[48+alpha_len:]
    print("El codi és:", code)
    print("El source és:", src, " i l'alpha és:", alpha, " i el total és ", total)

    k = 8
    txt = ''
    a = 0
    b = 2**k-1
    count = k-1
    end = False
    y = int(code[0:k], 2)

    print("Alpha, gamma i beta inicials:", a, y, b)
    while 9 != len(txt):
        p = 0
        aux_p = 0
        d = b-a+1
        for clave in src.keys():
            aux_p = p
            p += src[clave]/total
            if a+math.floor(d * p) > y:
                print(clave)
                src[clave] += 1
                txt += clave
                total += 1
                print(src, total)
                break
        print("Determinen nova lletra:", txt[len(txt)-1])
        b = a + math.floor(d * p)-1
        a = a + math.floor(d * aux_p) 
        print("Nous alpha, gamma i beta:", a, y, b)
        a_bin = dec2binary(a, k)
        y_bin = dec2binary(y, k)
        b_bin = dec2binary(b, k)
        print("En binari:", a_bin, y_bin, b_bin)

        while (a_bin[0] == b_bin[0]):
            if count < len(code)-1:
                count += 1
            else:
                end = True
            char = a_bin[0]
            a = a*2
            b = b*2 +1
            if code[count] == '0' or end:
                y = y*2
            else:
                y = y*2+1
            if (char == '1'):
                a = a - 2**k
                b = b - 2**k
                y = y - 2**k
            a_bin = dec2binary(a, k)
            y_bin = dec2binary(y, k)
            b_bin = dec2binary(b, k)
            print ("Reescalat:", a_bin, y_bin, b_bin)
            
        if a_bin[1] == '1' and b_bin[1] == '0':
            while(not(a_bin[0:2] == '00' or b_bin[0:2] == '11')):
                if count < len(code)-1:
                    count += 1
                else:
                    end = True
                a = a*2-2**(k-1)
                b = b*2-2**(k-1)+1
                if code[count] == '0' or end:
                    y = y*2-2**(k-1)
                else:
                    y = y*2-2**(k-1)+1
                a_bin = dec2binary(a, k)
                y_bin = dec2binary(y, k)
                b_bin = dec2binary(b, k)
                print ("Underflow:", a_bin, y_bin, b_bin)
        
        print("Queden alpha, gamma i beta:", a, y, b)
        print()
    print(txt)
    return txt

fileName = sys.argv[1]
with open(fileName, 'r') as f:
    txt = f.read()

decoded = decoder(txt, 1)

with open(os.path.splitext(fileName)[0] + ".og", 'w') as f:
    f.write(decoded)