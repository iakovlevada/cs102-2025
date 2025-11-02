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
    abc = ord("Z") - ord("A") + 1
    for char in plaintext:
        if ord("Z") + 1 - shift <= ord(char) <= ord("Z"):
            ciphertext += chr(ord(char) - abc + shift)
        elif ord("z") + 1 - shift <= ord(char) <= ord("z"):
            ciphertext += chr(ord(char) - abc + shift)
        elif not char.isalpha():
            ciphertext += char
        elif ord("A") <= ord(char) <= ord("Z") or ord("a") <= ord(char) <= ord("z"):
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
    abc = ord("Z") - ord("A") + 1
    for char in ciphertext:
        if ord("A") <= ord(char) <= ord("A") + shift - 1:
            plaintext += chr(ord(char) + abc - shift)
        elif ord("a") <= ord(char) <= ord("a") + shift - 1:
            plaintext += chr(ord(char) + abc - shift)
        elif not char.isalpha():
            plaintext += char
        elif ord("A") <= ord(char) <= ord("Z") or ord("a") <= ord(char) <= ord("z"):
            plaintext += chr(ord(char) - shift)
    return plaintext
