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

KEY = '1011011010'


def permutation(perm, key):
    permutated_key = ""
    for i in perm:
        permutated_key += key[i-1]
    return permutated_key


def left_half(bits):
    return bits[:5]


def right_half(bits):
    return bits[5:len(bits)]


def right_half_two(bits):
    return bits[4:len(bits)]


def shift1(bits):
    return bits[1:len(bits)] + bits[0]


def shift2(bits):
    return bits[2:len(bits)] + bits[0] + bits[1]


# Generar las llaves de acuerdo a la llave.
def generateKey(key, nShifts):
    left = left_half(key)
    right = right_half(key)
    # print("LEFT PART: ", left)
    # print("RIGHT PART: ", right)
    if nShifts == 1:
        shift_left = shift1(left)
        shift_right = shift1(right)
    elif nShifts == 2:
        shift_left = shift2(left)
        shift_right = shift2(right)
    shifted_key = shift_left + shift_right
    # print("PERMUTED ", nShifts, "SHIFT LEFT: ", shift_left, "\t", shift_right)
    # print("SHIFTED KEY: ", shifted_key)
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
    left = left_half(bits)
    right = right_half_two(bits)
    bits = permutation(EP, right)
    # print("EP: ", bits)
    bits = xor(bits, key)
    # print("XOR CON LA LLAVE 1: ", bits)
    bits = look_on_sbox(left_half(bits), S0) + \
        look_on_sbox(right_half_two(bits), S1)
    # print("BITS DEPUES DE SBOX: ", bits)
    bits = permutation(P4, bits)
    # print("BITS PERMUTADOS CON P4: ", bits)
    second_xor = xor(bits, left)
    # print("XOR ANTES DEL SW: ", second_xor)
    # print("-"*40)
    return second_xor


def encriptar(text):
    # Texto original a encriptar
    # print("Texto Original: ", text)

    # Permutacion de los bits originales
    bits_permutados = permutation(IP, text)
    # print("Texto Permutado: ", bits_permutados)

    # Permutacion de la llave
    print("KEY: ", KEY)
    permuted_key = permutation(P10, KEY)
    # print("PERMUTED KEY: ", permuted_key)

    # Generacion de llaves, el numero es para saber cuantos shifts se hacen hacia la izquierda
    k1 = generateKey(permuted_key, 1)
    k2 = generateKey(k1, 2)

    # Permutacion a P8
    key_one = permutation(P8, k1)
    key_two = permutation(P8, k2)
    # print("KEY ONE: ", key_one)
    # print("KEY TWO: ", key_two)
    f = fk(bits_permutados, key_one)
    bits = right_half_two(bits_permutados) + f
    # print("BITS DESPUES DE HACER LA 1RA VUELTA: ", bits)
    bits = fk(bits, key_two)
    # print("BITS DESPUES DE HACER LA 2DA VUELTA: ", bits)
    antes_p = bits + f
    # print("BITS ANTES DE LA IP-1: ", antes_p)
    final_en = permutation(IPi, bits + f)
    print("TEXTO ENCRIPTADO: ", final_en)


def desencriptar(cipher_text):
    bits = permutation(IP, cipher_text)
    permuted_key = permutation(P10, KEY)
    k1 = generateKey(permuted_key, 1)
    k2 = generateKey(k1, 2)

    # Permutacion a P8
    key_one = permutation(P8, k1)
    key_two = permutation(P8, k2)

    temp = fk(bits, key_two)
    bits = right_half_two(bits) + temp
    bits = fk(bits, key_one)
    final_des = permutation(IPi, bits + temp)
    print("TEXTO DESENCRIPTADO: ", final_des)


def main():
    encriptar('10110110')
    desencriptar('01000000')


main()
