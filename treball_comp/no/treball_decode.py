import math

def dec2binary(a, k):
    binary = bin(a)[2:]
    padded_binary = '0'*(k-len(binary)) + binary  
    return padded_binary

def arithmetic_decode(code):
    l = int(code[0:32], 2)
    l_alf = code[32:48]
    x = ''
    k = 32
    a = 0
    b = 2**k-1
    count = k-1
    end = False
    y = int(code[0:k], 2)
    total = 0
    for clave, valor in src.items():
        total += valor

    print("Alpha, gamma i beta inicials:", a, y, b)
    while l != len(x):
        p = 0
        aux_p = 0
        d = b-a+1
        for clave in src.keys():
            aux_p = p
            p += src[clave]/total
            if a+math.floor(d * p) > y:
                print(clave)
                x += clave
                break
        print("Determinen nova lletra:", x)
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
    return x

code = "0000000000000000000000000000101100000000000001100011011110000111000101110010110001111001000000101110000111"
#print(arithmetic_decode(code))
print(int(code[0:32], 2))
print(int(code[32:48], 2))
print(code[48:48+int(code[32:48], 2)*7])