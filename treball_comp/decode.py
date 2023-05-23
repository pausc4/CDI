import math
import os
import sys
from bitarray import bitarray
from time import process_time

def dec2binary(a, k):
    binary = bin(a)[2:]
    padded_binary = '0'*(k-len(binary)) + binary  
    return padded_binary
    
def decode(code, n):
    len_txt = int(code[0:32], 2)
    #print(len_txt)
    len_alpha = int(code[32:48], 2)*8
    alpha = []
    alpha_bin = code[48:48+len_alpha]

    i = 0
    while i < len(alpha_bin):
        if (alpha_bin[i] == '0'):
            bin = alpha_bin[i:i+8]
            lletra = chr(int(bin, 2))
            alpha.append(lletra)
            i += 8
        elif (alpha_bin[i:i+3] == '110'):
            bin = alpha_bin[i:i+16]

            bytes_utf8 = [int(bin[i:i+8], 2) for i in range(0, len(bin), 8)]
            utf8_bytes = bytes(bytes_utf8)
            lletra = utf8_bytes.decode('utf-8')

            alpha.append(lletra)
            i += 16
        elif (alpha_bin[i:i+4] == '1110'):
            bin = alpha_bin[i:i+24]

            bytes_utf8 = [int(bin[i:i+8], 2) for i in range(0, len(bin), 8)]
            utf8_bytes = bytes(bytes_utf8)
            lletra = utf8_bytes.decode('utf-8')

            alpha.append(lletra)
            i += 24
        elif (alpha_bin[i:i+5] == '11110'):
            bin = alpha_bin[i:i+32]

            bytes_utf8 = [int(bin[i:i+8], 2) for i in range(0, len(bin), 8)]
            utf8_bytes = bytes(bytes_utf8)
            lletra = utf8_bytes.decode('utf-8')

            alpha.append(lletra)
            i += 32
    #print(alpha)


    C = code[48+len_alpha:]

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
        #print(src)
        #print("Determinen nova lletra:", lletra)
        if lletra == '\x1b':
            lletra = alpha[it_alpha]
            it_alpha += 1
            #print("Determinen la verdadera nova lletra:", lletra)
            src.update({lletra:0})
        if (lletra != '/ufeff'):
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
    #print(alpha)
    return txt


fileName = sys.argv[1]

with open(fileName + ".cdi", 'rb') as f:
    bits = bitarray()
    bits.fromfile(f)
#print(bits)

txt = bits.to01()

t = process_time()
decoded = decode(txt, 1)
print("temps descodificació =",process_time()-t)

with open(os.path.splitext(fileName)[0] + "-desc.txt", 'w', encoding='utf-8') as f:
    f.write(decoded)