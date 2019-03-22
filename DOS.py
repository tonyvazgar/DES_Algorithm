import random
import math
import re

# Tuples with the permutation information
IP = (2, 6, 3, 1, 4, 8, 5, 7)
IPi = (4, 1, 3, 5, 7, 2, 8, 6)
EP = (4, 1, 2, 3, 2, 3, 4, 1)
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)

# Two S-Boxes
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

N = [2, 3, 1]

KEY = '0010010111'

hex2bin_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def permutation(perm, key):
    permutated_key = ""
    for i in perm:
        permutated_key += key[i-1]
    return permutated_key


def cutInHalf(bits):
    return left_half(bits), right_half(bits)


def left_half(bits):
    return bits[:len(bits)//2]


def right_half(bits):
    return bits[len(bits)//2:]


def shift1(bits):
    return bits[1:len(bits)] + bits[0]


def shift2(bits):
    return bits[2:len(bits)] + bits[0] + bits[1]


# Generar las llaves de acuerdo a la llave.
def generateKey(key, nShifts):
    left, right = cutInHalf(key)
    if nShifts == 1:
        shift_left = shift1(left)
        shift_right = shift1(right)
    elif nShifts == 2:
        shift_left = shift2(left)
        shift_right = shift2(right)
    shifted_key = shift_left + shift_right
    return shifted_key


def xor(bits, key):
    new = ""
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new


def look_on_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])


# RETURN DE FK
def fk(bits, key):
    left, right = cutInHalf(bits)
    bits = permutation(EP, right)
    bits = xor(bits, key)
    bits = look_on_sbox(left_half(bits), S0) + \
        look_on_sbox(right_half(bits), S1)

    bits = permutation(P4, bits)
    second_xor = xor(bits, left)
    return second_xor


def S_DES_Encrypt(text):
    bits_permutados = permutation(IP, text)
    permuted_key = permutation(P10, KEY)

    # Generacion de llaves, el numero es para saber cuantos shifts se hacen hacia la izquierda
    k1 = generateKey(permuted_key, 1)
    k2 = generateKey(k1, 2)

    # Permutacion a P8
    key_one = permutation(P8, k1)
    key_two = permutation(P8, k2)

    # Funcion Fk
    f = fk(bits_permutados, key_one)
    bits = right_half(bits_permutados) + f
    bits = fk(bits, key_two)
    final_en = permutation(IPi, bits + f)

    return final_en


def DES_Decrypt(cipher_text, LLAVE):
    bits = permutation(IP, cipher_text)
    permuted_key = permutation(P10, LLAVE)
    k1 = generateKey(permuted_key, 1)
    k2 = generateKey(k1, 2)

    # Permutacion a P8
    key_one = permutation(P8, k1)
    key_two = permutation(P8, k2)

    temp = fk(bits, key_two)
    bits = right_half(bits) + temp
    bits = fk(bits, key_one)
    final_des = permutation(IPi, bits + temp)
    # print("TEXTO DESENCRIPTADO: ", final_des)
    return final_des


""" Funcion que recibe un texto plano y regresa su valor en binario. """


def getBinary(text):
    binaryText = ' '.join('0' + format(ord(x), 'b') for x in text)
    return binaryText


""" Funcion que recibe un texto en binario y regresa su valor en hexadecimal. """


def binaryToHex(binaryText):
    if left_half(binaryText) == '0000':
        s = int(binaryText, 2)
        y = hex(s)
        d = str(y[2:]).upper()
        return '0' + d
    else:
        s = int(binaryText, 2)
        y = hex(s)
        d = str(y[2:]).upper()
    return d


def hexToBinary(hexLetter):
    s = int(hexLetter, 16)
    y = bin(s)
    d = str(y[2:])
    return d


def getText(binario):
    caracter = chr(int(binario, 2))
    return caracter


def mezclar(palabra):
    print("Palabra es: " + palabra)
    size = len(palabra)
    columns = len(N)
    print(columns)
    rows = int((size/columns)+1 if size % 2 == 0 else size/columns)
    print(rows)
    print(columns, rows)
    Matrix = [["" for x in range(columns)] for y in range(rows)]
    count = 0
    for i in range(columns):
        for j in range(rows):
            if count <= size:
                # print(palabra[count])
                Matrix[i][j] = palabra[count]
                count += 1
    # print(Matrix)

    newMatrix = [["" for x in range(columns)] for y in range(rows)]
    valores = []
    for i in range(columns):
        for n in N:
            # print(Matrix[i][n-1])
            valores.append(Matrix[i][n-1])
    valores.reverse()
    for i in range(columns):
        for j in range(rows):
            newMatrix[i][j] = valores.pop()

    string = ""
    pos = [i for i in range(columns)]
    # print(pos)
    for i in pos:
        for j in range(columns):
            string += newMatrix[j][i]
    transpose(newMatrix, columns)
    print("Transpuesta ", newMatrix)
    for i in range(1, columns):
        c = newMatrix[i]
        shifts = range(1, len(c))
        for s in shifts:
            newMatrix[i] = shift(c, s)
            shifts.pop()
    print("shifteada", newMatrix)
    print("Palabra transpuesta: "+string)
    return string


def shift(l, n):
    return l[n:] + l[:n]


def transpose(X, columns):
    for i in range(columns):
        print(X[i])
    # iterate through columns
        for j in range(len(X[0])):
            X[j][i] = X[i][j]


def encriptar(plain_text2):
    plain_text = plain_text2.replace(' ', '_')
    binary_list = [getBinary(character) for character in plain_text]
    encrypted_elements = [S_DES_Encrypt(binary) for binary in binary_list]
    encrypted_text = ""
    for element in encrypted_elements:
        encrypted_text += binaryToHex(element)
    return encrypted_text


def desencriptar(cipher_text, llave):
    binaries = "".join(hex2bin_map[character] for character in cipher_text)
    liston_separado = [binaries[i:i+8] for i in range(0, len(binaries), 8)]

    decrypted_elements = [DES_Decrypt(binary, llave) for binary in liston_separado]
    almost_plain = ""
    for binary in decrypted_elements:
        almost_plain += getText(binary)
    text = almost_plain.replace('_', ' ')
    return text


def leerLlaves(docLlaves):
    with open(docLlaves, "r") as file:
        lines = file.readlines()
    finalLines = [key.replace("\n", "") for key in lines]
    finalLines.sort()
    return finalLines

def bruteForce(keyList, cipher_text):
    for key in keyList:
        plainText = desencriptar(cipher_text, key)
        print("CON LLAVE: " + key + " TEXTO :" + plainText)

def main():

    palabra_chunga = mezclar('DIDYOUSEE')
    print("Palabra aturdida: ", palabra_chunga)

    cipher_text = encriptar(palabra_chunga)
    # texto_raw = input("Escribe la palabra a encriptar: ")
    # cipher_text = encriptar(texto_raw)
    # keys = leerLlaves("bits.txt")
    print("TEXTO ENCRIPTADO: \t", cipher_text)

    # bruteForce(keys, cipher_text)
    plain_text = desencriptar(cipher_text, KEY)
    print("TEXTO DESENCRIPTADO: \t", plain_text)


main()
