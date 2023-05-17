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

def arithmetic_encode(txt,n):
    src = {'\x1b':1}
    total = 0
    k = 32
    a = 0
    b = 2**k-1
    print("Interval inicial", a, b)
    print()
    c = ''
    alpha = ['\x1b']
    count = 0

    for i in range(0, len(txt), n):
        total+=n
        lletra = txt[i:i+n]
        if lletra not in src:
            src.update({lletra:1}) 
            alpha.append(lletra)          
            print("La lletra " + lletra + " no estava en el diccionari, s'ha afegit")
            lletra = '\x1b'
        else:
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
    return c

def arithmetic_decode(code, k, src, l):
    x = ''
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

print(arithmetic_encode("abracadabra", 1))