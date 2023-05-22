import math
import os
import sys
from bitarray import bitarray

def dec2binary(a, k):
    binary = bin(a)[2:]
    padded_binary = '0'*(k-len(binary)) + binary  
    return padded_binary

def decode(code, n):
    len_txt = int(code[0:32], 2)
    len_alpha = int(code[32:48], 2)
    alpha_bin = code[48:48+len_alpha*7]
    C = code[48+len_alpha*7:]
    alpha = []
    for i in range (0, len_alpha*7, 7):
        bin = alpha_bin[i:i+7]
        lletra = chr(int(bin, 2))
        alpha.append(lletra)
    
    it_alpha = 1
    src = {'\x1b':1}
    total = 1

    txt = ''
    lletra = ''
    k = 32
    a = 0
    b = 2**k-1
    count = k-1
    end = False
    y = int(C[0:k], 2)

    #print("Alpha, gamma i beta inicials:", a, y, b)

    while len(txt) != len_txt:
        p = 0
        aux_p = 0
        d = b-a+1
        for clave in src.keys():
            aux_p = p
            p += src[clave]
            if a+math.floor(d * p/total) > y:
                lletra = clave
                break
        #print("Determinen nova lletra:", lletra)
        if lletra == '\x1b':
            lletra = alpha[it_alpha]
            it_alpha += 1
            #print("Determinen la verdadera nova lletra:", lletra)
            src.update({lletra:0})
        txt += lletra
        src[lletra] = src[lletra]+1
        b = a + math.floor(d * p/total)-1
        a = a + math.floor(d * aux_p/total) 
        total += 1
        #print("Nous alpha, gamma i beta:", a, y, b)
        a_bin = dec2binary(a, k)
        y_bin = dec2binary(y, k)
        b_bin = dec2binary(b, k)
        #print("En binari:", a_bin, y_bin, b_bin)

        while (a_bin[0] == b_bin[0]):
            if count < len(C)-1:
                count += 1
            else:
                end = True
            char = a_bin[0]
            a = a*2
            b = b*2 +1
            if C[count] == '0' or end:
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
            #print ("Reescalat:", a_bin, y_bin, b_bin)
            
        if a_bin[1] == '1' and b_bin[1] == '0':
            while(not(a_bin[0:2] == '00' or b_bin[0:2] == '11')):
                if count < len(C)-1:
                    count += 1
                else:
                    end = True
                a = a*2-2**(k-1)
                b = b*2-2**(k-1)+1
                if C[count] == '0' or end:
                    y = y*2-2**(k-1)
                else:
                    y = y*2-2**(k-1)+1
                a_bin = dec2binary(a, k)
                y_bin = dec2binary(y, k)
                b_bin = dec2binary(b, k)
                #print ("Underflow:", a_bin, y_bin, b_bin)
        
        #print("Queden alpha, gamma i beta:", a, y, b)
        #print()
    return txt


fileName = sys.argv[1]

with open(fileName + ".cdi", 'rb') as f:
    bits = bitarray()
    bits.fromfile(f)

txt = bits.to01()
decoded = decode(txt, 1)

with open(os.path.splitext(fileName)[0] + "-desc.txt", 'w', encoding='utf-8') as f:
    f.write(decoded)