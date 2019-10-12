def encrypt_caesar(plaintext: str) -> str:
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
    ciphertext = ''
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if chr((ord(plaintext[i]) + 3)).isalpha():
                ciphertext += chr(ord(plaintext[i]) + 3)
            else:
                ciphertext += chr(ord(plaintext[i]) - 23)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
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
    plaintext = ''
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if chr((ord(ciphertext[i]) - 3)).isalpha():
                plaintext += chr(ord(ciphertext[i]) - 3)
            else:
                plaintext += chr(ord(ciphertext[i]) + 23)
        else:
            plaintext += ciphertext[i]
    return plaintext
