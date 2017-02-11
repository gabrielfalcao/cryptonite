# -*- coding: utf-8 -*-
from cryptonite.aes.bases import BaseAESCBC

from cryptonite.aes.blocks import Block128
from cryptonite.aes.blocks import Block256


class AES128CBC(BaseAESCBC):
    blocks = Block128
    label = 'aes-128-cbc'


class AES256CBC(BaseAESCBC):
    blocks = Block256
    label = 'aes-256-cbc'


def encrypt128(plaintext, passphrase):
    cipher = AES128CBC()
    return cipher.encrypt(plaintext, passphrase)


def decrypt128(ciphertext, passphrase):
    cipher = AES128CBC()
    return cipher.decrypt(ciphertext, passphrase)


def encrypt256(plaintext, passphrase):
    cipher = AES256CBC()
    return cipher.encrypt(plaintext, passphrase)


def decrypt256(ciphertext, passphrase):
    cipher = AES256CBC()
    return cipher.decrypt(ciphertext, passphrase)
