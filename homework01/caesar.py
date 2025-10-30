"""
Caesar cipher
"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if ord(char) in range(ord("Z") + 1 - shift, ord("Z") + 1):
            ciphertext += chr(ord(char) - (ord("Z") - ord("A") + 1) + shift)
        elif ord(char) in range(ord("z") + 1 - shift, ord("z") + 1):
            ciphertext += chr(ord(char) - (ord("z") - ord("a") + 1) + shift)
        elif not char.isalpha():
            ciphertext += char
        else:
            ciphertext += chr(ord(char) + shift)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if ord(char) in range(ord("A"), ord("A") + shift):
            plaintext += chr(ord(char) + (ord("Z") - ord("A") + 1) - shift)
        elif ord(char) in range(ord("a"), ord("a") + shift):
            plaintext += chr(ord(char) + (ord("z") - ord("a") + 1) - shift)
        elif not char.isalpha():
            plaintext += char
        else:
            plaintext += chr(ord(char) - shift)
    return plaintext


STR = str(input())
print(encrypt_caesar(STR))
print(decrypt_caesar(STR))
