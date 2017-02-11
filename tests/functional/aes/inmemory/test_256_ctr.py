# -*- coding: utf-8 -*-

"\033[0;32min-memory AES CTR 256\033[0m"

from cryptonite.aes.ctr import encrypt256
from cryptonite.aes.ctr import decrypt256

from tests.functional.scenarios import generate_passphrase
from tests.functional.scenarios import generate_humanized_bytes


# def test_ctr_1kib():
#     "can encrypt/decrypt up to 1 KiB of plain-text"

#     # Given a random password
#     password = generate_passphrase()

#     # And a plaintext
#     plaintext = generate_humanized_bytes(1024)

#     # When I encrypt with AES-256-CTR
#     ciphertext = encrypt256(plaintext, password)

#     # Then it should not return a plaintext
#     ciphertext.should_not.equal(plaintext)

#     # And it can be decrypted to the exact plaintext
#     pt = decrypt256(ciphertext, password)
#     pt.should.equal(plaintext)


# def test_ctr_1mib():
#     "can encrypt/decrypt up to 1 MiB of plain-text"

#     # Given a random password
#     password = generate_passphrase()

#     # And a plaintext
#     plaintext = generate_humanized_bytes(1024 ** 2)

#     # When I encrypt with AES-256-CTR
#     ciphertext = encrypt256(plaintext, password)

#     # Then it should not return a plaintext
#     ciphertext.should_not.equal(plaintext)

#     # And it can be decrypted to the exact plaintext
#     pt = decrypt256(ciphertext, password)
#     pt.should.equal(plaintext)
