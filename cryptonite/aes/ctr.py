# -*- coding: utf-8 -*-
from cryptonite.aes.bases import BaseAESCTR

from cryptonite.aes.blocks import Block128
from cryptonite.aes.blocks import Block256


class AES128CTR(BaseAESCTR):
    blocks = Block128
    label = 'aes-128-ctr'


class AES256CTR(BaseAESCTR):
    blocks = Block256
    label = 'aes-256-ctr'


def encrypt128(plaintext, passphrase):
    cipher = AES128CTR()
    return cipher.encrypt(plaintext, passphrase)


def decrypt128(ciphertext, passphrase):
    cipher = AES128CTR()
    return cipher.decrypt(ciphertext, passphrase)


def encrypt256(plaintext, passphrase):
    cipher = AES256CTR()
    return cipher.encrypt(plaintext, passphrase)


def decrypt256(ciphertext, passphrase):
    cipher = AES256CTR()
    return cipher.decrypt(ciphertext, passphrase)
