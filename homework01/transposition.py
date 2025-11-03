def encrypt_transposition(plaintext, block_size, id1, id2):
    if id1 >= block_size or id2 >= block_size:
        raise ValueError
    ciphertext = ""
    i = 0
    while i + block_size <= len(plaintext):
        ciphertext0 = list(plaintext[i : (i + block_size)])
        ciphertext0[id1], ciphertext0[id2] = ciphertext0[id2], ciphertext0[id1]
        ciphertext01 = "".join(map(str, ciphertext0))
        ciphertext += ciphertext01
        i += block_size
    ciphertext0 = list(plaintext[(len(plaintext) // block_size) * block_size :])
    if len(ciphertext0) > id1 and len(ciphertext0) > id2:
        ciphertext0[id1], ciphertext0[id2] = ciphertext0[id2], ciphertext0[id1]
        ciphertext01 = "".join(map(str, ciphertext0))
        ciphertext += ciphertext01
    else:
        ciphertext01 = "".join(map(str, ciphertext0))
        ciphertext += ciphertext01
    return ciphertext


print(encrypt_transposition("He", 4, 0, 1))
