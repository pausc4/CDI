import math

def dec2binary(a, k):
    binary = bin(a)[2:]
    padded_binary = '0'*(k-len(binary)) + binary  
    return padded_binary

def list2code(a):
    c = ""
    for i in a:
        dec = ord(i)
        c += dec2binary(dec, 7)
    return c

def encoder (txt, n):
    total = 0
    k = 8
    a = 0
    b = 2**k-1
    print("Interval inicial", a, b)
    print()
    c = ''
    alpha = sorted(list(set(txt)))
    count = 0
    src = {}
    
    for i in alpha:
        src.update({i:1})
        total+=1

    for i in range(0, len(txt), n):
        total+=n
        lletra = txt[i:i+n]
        
        src.update({lletra:src[lletra]+1})
        
        d = b-a+1
        it = alpha.index(lletra)
        p = 0
        while(it > 0):
            p += src[alpha[it-1]]
            it -= 1
        b = a + math.floor(d * (p + src[lletra])/total)-1
        a = a + math.floor(d * p/total)    

        print("Es codifica la lletra:", lletra, " i queda el subinterval", a, b)
        a_bin = dec2binary(a, k)
        b_bin = dec2binary(b, k)
        print("En binari:", a_bin, b_bin)

        while (a_bin[0] == b_bin[0]):
            char = a_bin[0]
            c += char
            a = a*2
            b = b*2 +1
            if (char == '1'):
                a = a - 2**k
                b = b - 2**k
            a_bin = dec2binary(a, k)
            b_bin = dec2binary(b, k)
            print ("Reescalat:", a_bin, b_bin)
            print("codi:", c)
            if count > 0:
                print("Afegits", count, "bits d'underflow")
                if char == '0':
                    char = '1'
                else:
                    char = '0'
                while(count > 0):
                    c += char
                    count -= 1
                print("codi:", c)

        if a_bin[1] == '1' and b_bin[1] == '0':
            while(not(a_bin[0:2] == '00' or b_bin[0:2] == '11')):
                count += 1
                a = a*2-2**(k-1)
                b = b*2-2**(k-1)+1
                a_bin = dec2binary(a, k)
                b_bin = dec2binary(b, k)
                print("Underflow num.", count)
                print ("Reescalat:", a_bin, b_bin)

        print("Interval ha quedat", a, b)
        print()
    
    c += '1'
    print("afegim un 1 al final i queda el codi", c)
    code = dec2binary(len(txt), 32)
    print("El text te una mida de ", len(txt) ,  " i el code és " + code)
    code += dec2binary(len(alpha), 16)
    print("Alpha te una mida de ", len(alpha), " i és ", alpha , " i codificat és ", list2code(alpha))
    code += list2code(alpha)
    code += c
    print("El codi final és " + code)
    print("EL source és ", src)
    return code


import sys
import os

fileName = sys.argv[1]
with open(fileName, 'r') as f:
    txt = f.read()

encoded = encoder(txt, 1)

with open(os.path.splitext(fileName)[0] + ".codi", 'w') as f:
    f.write(encoded)

