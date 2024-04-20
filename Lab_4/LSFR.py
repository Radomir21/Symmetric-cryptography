from itertools import product
from scipy.stats import norm
from multiprocessing import Pool



def lsfr_generate_bit(state, recurenta):
    result = state[0]
    generated = sum(state[i] for i in recurenta) % 2
    state = state[1:] + bytearray([generated])
    return result, state

def geffe_generate_bit(lrz_1, lrz_2, lrz_3):
    x, state_lrz_1 = lsfr_generate_bit(lrz_1[0], lrz_1[1])
    y, state_lrz_2 = lsfr_generate_bit(lrz_2[0], lrz_2[1])
    s, state_lrz_3 = lsfr_generate_bit(lrz_3[0], lrz_3[1])
    return (s & x) ^ ((1 ^ s) & y), (state_lrz_1, state_lrz_2, state_lrz_3)

# Приклад використання:
z_i = bytearray([1, 0, 1, 1, 0])
recurrent_list = [0, 2, 3, 4]
lrz_1_state = (z_i.copy(), recurrent_list.copy())
lrz_2_state = (z_i.copy(), recurrent_list.copy())
lrz_3_state = (z_i.copy(), recurrent_list.copy())

# Генерація біта
result_bit, new_lrz_states = geffe_generate_bit(lrz_1_state, lrz_2_state, lrz_3_state)
print(result_bit)


z_default = '00010101000010100010101001111111111011001101010001101110101010000001010111101001110001100111000001000011100010111101010100000101011110101010111100001100000110111011000000000111011101011011000000011110001000110011100001000110001000000000011011000101111011000001110011100011011011111110111110101100000100110101100001001101001100011000011110101010011000101000010011101001000110011011000010100000101100100000100110100011111001100100001110110001001001001011110111010011110111010101010101000111100000000001111010001000010001000100010100100101001000111010001000100100001011010010000111111001001100100001111010001001100000011101001001000110111000010110111111011010011101010010100100001111111111101110010000110000010011111100001011111001010001011011100011100010110011100101101101111100011110101101001011010110111001101010000010100110001111111100110010100110110001011011001100101100101000101010001101101100111001100101110000011000111101111111001100110110111101100101010101011100011001000010111010100010101100010111110111110001000110001110100101110111010000111110011000110010010011011111111011111111011011101101001000000000001011111010101011101010010010001010110011100101010011100101010001111000010001100111100111110111101101101111001000010101001101100001010100011100100001111000110100111000011101011101011001100001110011111010000010010111111010001110001011010100011110000011100100111001100001001111111111001001000110001000111110010011101111001010000010000111011101101011101001000110011000010011010100111100011101000100101011101001011000110010110000111100110011010011110011100101100101101100100101110101010010001010101101011101011100100100110000011010110111100001111101101110011100010101011110111010110101011101110100110011101110000010101000110110111101100010111100001011101101111010111001100110010100000110011101111111000101111110010001011011010001001011000110000000100100101011010110110010001110110011100010101111001101110010010100010001110001110000110010000101111110110011111111001100101000000001110110011010100111001100010101011111000010111000010101101111'
z_sequence = bytearray([int(el) for el in z_default])
print(z_default)


def lsfr_generate_bit(state, polynom):
    result = state[0]
    generated = sum(state[i] for i in polynom) % 2
    state = state[1:] + bytearray([generated])
    return result, state


L1_polynom = [3, 0]


def L_1(n):
    state = (n.copy(), L1_polynom)
    array_bits = bytearray()

    for _ in range(222):
        bit, state = lsfr_generate_bit(state[0], state[1])
        array_bits.append(bit)

    R = sum(array_bits[i] ^ z_default[i] for i in range(222))
    
    if R <= 71:
        return (list(n), R)


if __name__ == '__main__':
    generat_bit = (bytearray(vector) for vector in product([0, 1], repeat=25))
    pool = Pool()
    result = pool.map(L_1, generat_bit)
    result = sorted(filter(None, result), key=lambda x: x[1])
    print(result)







