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
    lowercase_z = ord("z")
    uppercase_z = ord("Z")
    lowercase_a = ord("a")
    uppercase_a = ord("A")
    for char in plaintext:
        if uppercase_z + 1 - shift <= ord(char) <= uppercase_z:
            ciphertext += chr(ord(char) - abc + shift)
        elif lowercase_z + 1 - shift <= ord(char) <= lowercase_z:
            ciphertext += chr(ord(char) - abc + shift)
        elif not char.isalpha():
            ciphertext += char
        elif uppercase_a <= ord(char) <= uppercase_z or lowercase_a <= ord(char) <= lowercase_z:
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
    lowercase_z = ord("z")
    uppercase_z = ord("Z")
    lowercase_a = ord("a")
    uppercase_a = ord("A")
    for char in ciphertext:
        if uppercase_a <= ord(char) <= uppercase_a + shift - 1:
            plaintext += chr(ord(char) + abc - shift)
        elif lowercase_a <= ord(char) <= lowercase_a + shift - 1:
            plaintext += chr(ord(char) + abc - shift)
        elif not char.isalpha():
            plaintext += char
        elif uppercase_a <= ord(char) <= uppercase_z or lowercase_a <= ord(char) <= lowercase_z:
            plaintext += chr(ord(char) - shift)
    return plaintext
