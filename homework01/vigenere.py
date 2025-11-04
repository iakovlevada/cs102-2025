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
    lowercase_z = ord("z")
    uppercase_z = ord("Z")
    lowercase_a = ord("a")
    uppercase_a = ord("A")
    keyword = keyword.upper()
    length = len(keyword)
    for i, char in enumerate(plaintext):
        j = i % length
        shift = ord(keyword[j]) - uppercase_a
        if not char.isalpha():
            ciphertext += char
        elif uppercase_a <= ord(char) <= uppercase_z:
            ciphertext += chr((ord(char) - uppercase_a + shift) % abc + uppercase_a)
        elif lowercase_a <= ord(char) <= lowercase_z:
            ciphertext += chr((ord(char) - lowercase_a + shift) % abc + lowercase_a)
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
    lowercase_z = ord("z")
    uppercase_z = ord("Z")
    lowercase_a = ord("a")
    uppercase_a = ord("A")
    keyword = keyword.upper()
    length = len(keyword)
    for i, char in enumerate(ciphertext):
        j = i % length
        shift = ord(keyword[j]) - uppercase_a
        if not char.isalpha():
            plaintext += char
        elif uppercase_a <= ord(char) <= uppercase_z:
            plaintext += chr((ord(char) - uppercase_a - shift + abc) % abc + uppercase_a)
        elif lowercase_a <= ord(char) <= lowercase_z:
            plaintext += chr((ord(char) - lowercase_a - shift + abc) % abc + lowercase_a)
    return plaintext
