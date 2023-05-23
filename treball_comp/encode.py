import math
import sys
import os
from bitarray import bitarray
from time import process_time

def dec2binary(a, k):
    binary = bin(a)[2:]
    padded_binary = '0'*(k-len(binary)) + binary  
    return padded_binary

def list2code(a):
    c = ""
    for i in a:
        dec = i.encode('utf-8')
        bits = [bin(byte)[2:].zfill(8) for byte in dec]
        print(bits, i)
        for j in bits:
            c += j
        #print(c)
    print(len(c))
    c = dec2binary(int(len(c)/8), 16) + c
    return c

def encode(txt,n):
    src = {'\x1b':1}
    total = 1
    k = 32
    a = 0
    b = 2**k-1
    #print("Interval inicial", a, b)
    #print()
    c = ''
    alpha = ['\x1b']
    count = 0
    aux = ''

    for i in range(0, len(txt), n):
        lletra = txt[i:i+n]
        aux = lletra

        if lletra not in src:
            #print("La lletra " + lletra + " no estava en el diccionari, s'ha afegit")
            lletra = '\x1b'     
        d = b-a+1
        it = alpha.index(lletra)
        p = 0
        while(it > 0):
            p += src[alpha[it-1]]
            it -= 1
        b = a + math.floor(d * (p + src[lletra])/total)-1
        a = a + math.floor(d * p/total)    
        #print(src)
        #print("Es codifica la lletra:", lletra, " i queda el subinterval", a, b)
        a_bin = dec2binary(a, k)
        b_bin = dec2binary(b, k)
        #print("En binari:", a_bin, b_bin)

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
            #print ("Reescalat:", a_bin, b_bin)
            #print("codi:", c)
            if count > 0:
                #print("Afegits", count, "bits d'underflow")
                if char == '0':
                    char = '1'
                else:
                    char = '0'
                while(count > 0):
                    c += char
                    count -= 1
               # print("codi:", c)

        if a_bin[1] == '1' and b_bin[1] == '0':
            while(not(a_bin[0:2] == '00' or b_bin[0:2] == '11')):
                count += 1
                a = a*2-2**(k-1)
                b = b*2-2**(k-1)+1
                a_bin = dec2binary(a, k)
                b_bin = dec2binary(b, k)
                #print("Underflow num.", count)
                #print ("Reescalat:", a_bin, b_bin)
        #print("Interval ha quedat", a, b)
        #print()
        if aux not in src:
            src.update({aux:1})
            alpha.append(aux)          
        else:
            src[aux]+=1
        total+=n

    c += '1'
    #print("afegim un 1 al final i queda el codi", c)
    code = dec2binary(len(txt), 32)
    #print("El text te una mida de ", len(txt) ,  " i el code és " + code)
    #code += dec2binary(len(alpha), 16)
    #print("Alpha te una mida de ", len(alpha), " i és ", alpha , " i codificat és ", list2code(alpha))
    print (alpha)
    alpha_bin = list2code(alpha)
    code += alpha_bin
    print(alpha_bin[16:])
    code += c
    #print("El codi final és " + code)
    return code
    



fileName = sys.argv[1]

with open(fileName + ".txt", 'r', encoding='utf-8') as f:
    txt = f.read()

t = process_time()
encoded = encode(txt, 1)
print("temps codificació =",process_time()-t);
bits = bitarray(encoded)

with open(os.path.splitext(fileName)[0] + ".cdi", 'wb') as f:
    bits.tofile(f)

print ("El fitxer s'ha comprimit a " + fileName + ".cdi.")
rendiment = 8 * os.path.getsize(fileName+".cdi") / len(txt)
print ("El rendiment en la compressió és ", rendiment )