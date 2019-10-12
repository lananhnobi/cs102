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
    keyword1 = []
    for i in range(len(keyword)):
        if keyword[i].isupper():
            keyword1.append(ord(keyword[i]) - 65)
        if keyword[i].islower():
            keyword1.append(ord(keyword[i]) - 97)
    if len(plaintext) > len(keyword1):
        keyword1 *= len(plaintext) // len(keyword1) + 1
    for i in range(len(plaintext)):
        if plaintext[i].islower():
            if (ord(plaintext[i]) + keyword1[i]) > 122:
                ciphertext += chr(ord(plaintext[i]) + keyword1[i] - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + keyword1[i])
        elif plaintext[i].isupper():
            if (ord(plaintext[i]) + keyword1[i]) > 90:
                ciphertext += chr(ord(plaintext[i]) + keyword1[i] - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + keyword1[i])
        else:
            ciphertext += plaintext[i]
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
    keyword1 = []
    for i in range(len(keyword)):
        if keyword[i].isupper():
            keyword1.append(ord(keyword[i]) - 65)
        if keyword[i].islower():
            keyword1.append(ord(keyword[i]) - 97)
    if len(ciphertext) > len(keyword1):
        keyword1 *= len(ciphertext) // len(keyword1) + 1
    for i in range(len(ciphertext)):
        if ciphertext[i].islower():
            if (ord(ciphertext[i]) - keyword1[i]) < 97:
                plaintext += chr(ord(ciphertext[i]) - keyword1[i] + 26)
            else:
                plaintext += chr(ord(ciphertext[i]) - keyword1[i])
        elif ciphertext[i].isupper():
            if (ord(ciphertext[i]) - keyword1[i]) < 65:
                plaintext += chr(ord(ciphertext[i]) - keyword1[i] + 26)
            else:
                plaintext += chr(ord(ciphertext[i]) - keyword1[i])
        else:
            plaintext += ciphertext[i]
    return plaintext
