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
    abc = ord("Z") - ord("A") + 1
    keyword = keyword.upper()
    length = len(keyword)
    for i, char in enumerate(plaintext):
        j = i % length
        shift = ord(keyword[j]) - ord("A")
        if not char.isalpha():
            ciphertext += char
        elif ord("A") <= ord(char) <= ord("Z"):
            ciphertext += chr((ord(char) - ord("A") + shift) % abc + ord("A"))
        elif ord("a") <= ord(char) <= ord("z"):
            ciphertext += chr((ord(char) - ord("a") + shift) % abc + ord("a"))
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
    abc = ord("Z") - ord("A") + 1
    keyword = keyword.upper()
    length = len(keyword)
    for i, char in enumerate(ciphertext):
        j = i % length
        shift = ord(keyword[j]) - ord("A")
        if not char.isalpha():
            plaintext += char
        elif ord("A") <= ord(char) <= ord("Z"):
            plaintext += chr((ord(char) - ord("A") - shift + abc) % abc + ord("A"))
        elif ord("a") <= ord(char) <= ord("z"):
            plaintext += chr((ord(char) - ord("a") - shift + abc) % abc + ord("a"))
    return plaintext
