"""
Vigenere cipher
"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    alphabet = [chr(A) for A in range(ord("A"), ord("Z") + 1)]
    j = 0
    for char in plaintext:
        for k, letter in enumerate(alphabet):
            if keyword[j] == letter or keyword[j] == letter.lower():
                if ord(char) in range(ord("Z") - k + 1, ord("Z") + 1):
                    ciphertext += chr(ord(char) - (ord("Z") - ord("A") + 1) + k)
                elif ord(char) in range(ord("z") - k + 1, ord("z") + 1):
                    ciphertext += chr(ord(char) - (ord("z") - ord("a") + 1) + k)
                elif not char.isalpha():
                    ciphertext += char
                else:
                    ciphertext += chr(ord(char) + k)
        j += 1
        if j == len(keyword):
            j = 0
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    alphabet = [chr(A) for A in range(ord("A"), ord("Z") + 1)]
    j = 0
    for char in ciphertext:
        for k, letter in enumerate(alphabet):
            if keyword[j] == letter or keyword[j] == letter.lower():
                if ord(char) in range(ord("A"), ord("A") + k):
                    plaintext += chr(ord(char) + (ord("Z") - ord("A") + 1) - k)
                elif ord(char) in range(ord("a"), ord("a") + k):
                    plaintext += chr(ord(char) + (ord("z") - ord("a") + 1) - k)
                elif not char.isalpha():
                    plaintext += char
                else:
                    plaintext += chr(ord(char) - k)
        j += 1
        if j == len(keyword):
            j = 0
    return plaintext
