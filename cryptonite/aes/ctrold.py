# -*- coding: utf-8 -*-

from Crypto import Random
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import PBKDF2

from cryptonite.aes.armor import cuirass, uncuirass


ITERATIONS = 1345

BLOCK_SIZE = 32
IV_SIZE = 16


class IntegrityViolation(Exception):
    pass


def generate_keys(seed_text, salt):
    # Use the PBKDF2 algorithm to obtain the encryption and hmac key
    full_key = PBKDF2(seed_text, salt, dkLen=64, count=ITERATIONS)

    # Take the first half of this hash and use it as the key
    # to encrypt the plain text log file. encrypt_key is 256 bits
    encrypt_key = full_key[:len(full_key) / 2]

    # Use the last half as the HMAC key
    signature_key = full_key[len(full_key) / 2:]

    return encrypt_key, signature_key


def encrypt256(plaintext, passphrase):
    # Generate the encryption and hmac keys from the token,
    # using a random salt
    signature_salt = Random.new().read(IV_SIZE)
    encrypt_key, signature_key = generate_keys(passphrase, signature_salt)

    # Set-up the counter for AES CTR-mode cipher
    ctr_iv = Random.new().read(IV_SIZE)
    ctr = Counter.new(128, initial_value=long(ctr_iv.encode('hex'), 16))
    ciphertext = signature_salt + ctr_iv

    # create the cipher object
    cipher = AES.new(encrypt_key, AES.MODE_CTR, counter=ctr)

    # encrypt the plain text log and add it to the logfile cipher text
    # which currently contains the iv for aes ctr mode
    ciphertext = ciphertext + cipher.encrypt(plaintext)

    # use the 2nd half of the hashed token to sign the cipher text
    # version of the log file using a mac (message authentication code)
    hmac = HMAC.new(signature_key, ciphertext, SHA256)
    signature = hmac.digest()

    # Add the mac to the ciphertext
    ciphertext = ciphertext + signature

    return cuirass(ciphertext)


def decrypt256(ciphertext, passphrase):
    ciphertext = uncuirass(ciphertext)
    # Extract the hmac salt from the file
    signature_salt = ciphertext[:16]

    # Generate the encryption and hmac keys from the token
    encrypt_key, signature_key = generate_keys(passphrase, signature_salt)

    # Extract the MAC from the end of the file
    signature = ciphertext[-32:]

    # Cut the MAC off of the end of the ciphertext
    ciphertext = ciphertext[:-32]

    # Check the MAC
    hmac = HMAC.new(signature_key, ciphertext, SHA256)
    computed_signature = hmac.digest()

    if computed_signature != signature:
        # The macs don't match. Raise an exception for the caller to handle.
        raise IntegrityViolation()

    # Cut the HMAC salt from the start of the file
    ciphertext = ciphertext[16:]

    # Decrypt the data

    # Recover the IV from the ciphertext
    ctr_iv = ciphertext[:16]  # AES counter block is 128 bits (16 bytes)

    # Cut the IV off of the ciphertext
    ciphertext = ciphertext[16:]

    # Create and initialise the counter
    ctr = Counter.new(128, initial_value=long(ctr_iv.encode('hex'), 16))

    # Create the AES cipher object and decrypt the ciphertext
    cipher = AES.new(encrypt_key, AES.MODE_CTR, counter=ctr)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext
