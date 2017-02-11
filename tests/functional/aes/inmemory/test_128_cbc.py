# -*- coding: utf-8 -*-

"\033[0;32min-memory AES CBC 128\033[0m"

from cryptonite.aes.cbc import encrypt128
from cryptonite.aes.cbc import decrypt128

from tests.functional.scenarios import generate_passphrase
from tests.functional.scenarios import generate_humanized_bytes


def test_cbc_1kib():
    "can encrypt/decrypt up to 1 KiB of plain-text"

    # Given a random password
    password = generate_passphrase()

    # And a plaintext
    plaintext = generate_humanized_bytes(1024)

    # When I encrypt with AES-128-CBC
    ciphertext = encrypt128(plaintext, password)

    # Then it should not return a plaintext
    ciphertext.should_not.equal(plaintext)

    # And it can be decrypted to the exact plaintext
    pt = decrypt128(ciphertext, password)
    pt.should.equal(plaintext)


def test_cbc_1mib():
    "can encrypt/decrypt up to 1 MiB of plain-text"

    # Given a random password
    password = generate_passphrase()

    # And a plaintext
    plaintext = generate_humanized_bytes(1024 ** 2)

    # When I encrypt with AES-128-CBC
    ciphertext = encrypt128(plaintext, password)

    # Then it should not return a plaintext
    ciphertext.should_not.equal(plaintext)

    # And it can be decrypted to the exact plaintext
    pt = decrypt128(ciphertext, password)
    pt.should.equal(plaintext)
