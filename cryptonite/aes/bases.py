# -*- coding: utf-8 -*-
from cryptonite.ciphers import BaseCipher
from cryptonite.exceptions import AESCTRIntegrityViolation

from .modes import CBCMode
from .modes import CTRMode
from .armor import cuirass
from .armor import uncuirass
from .armor import b64encode
from .armor import b64decode


#  _____ _____    ____  _____
# |_   _|     |  |    \|     |
#   | | |  |  |  |  |  |  |  |
#   |_| |_____|  |____/|_____|
#  ............................
#
# fuck this, build a string encoder pipeline

class BaseAES(BaseCipher):
    def transmogrify_passphrase(self, passphrase, iv=None):
        if not iv:
            iv = self.blocks.generate_iv()

        # TODO: consider bcrypt hashing the password
        key, iv = self.blocks.pbkdf2hmac(
            iterations=5000,
            secret=passphrase,
            salt=iv
        )
        return key, iv


class BaseAESCBC(BaseAES):
    mode = CBCMode

    def encrypt(self, plaintext, passphrase):
        key, iv = self.transmogrify_passphrase(passphrase)
        engine = self.mode.engine(key, iv)

        # 1. b64encode
        spaceless = b64encode(plaintext)  # decrypt step 5
        # 2. add padding
        padded = self.blocks.pad(spaceless)  # decrypt step 4
        # 3. encrypt the padded data with aes-256-cbc
        aes_ciphertext = engine.encrypt(padded)  # decrypt step 3
        # 4. pack the iv in front of the ciphertext
        bundle = self.blocks.pack_iv_and_ciphertext(iv, aes_ciphertext)  # decrypt step 2
        # 5. armor the ciphertext for ascii-safety
        ciphertext = cuirass(bundle)  # decrypt step 1
        return ciphertext

    def decrypt(self, ciphertext, passphrase):
        # 1. unarmor the ciphertext
        bundle = uncuirass(ciphertext)
        # 2. unpack the iv and the actual ciphertext
        iv, aes_ciphertext = self.blocks.unpack_iv_and_ciphertext(bundle)
        # 3. decrypt the ciphertext with aes-256-cbc
        key, iv = self.transmogrify_passphrase(passphrase, iv)
        engine = self.mode.engine(key, iv)
        padded = engine.decrypt(aes_ciphertext)
        # 4. remove padding from data
        spaceless = self.blocks.unpad(padded)
        # 5. b64decode the original
        plaintext = b64decode(spaceless)
        return plaintext


class BaseAESCTR(BaseAES):
    mode = CTRMode

    def encrypt(self, plaintext, passphrase):
        # 1. generate a signature salt
        signature_salt = self.blocks.generate_iv()
        # 2. generate keys
        key, signature_key = self.transmogrify_passphrase(passphrase, signature_salt)
        # 3. generate iv
        iv = self.blocks.generate_iv()
        engine = self.mode.engine(key, iv)
        ciphertext = engine.encrypt(plaintext)
        bundle = signature_salt + iv + ciphertext
        signature = self.blocks.sign_ciphertext(bundle, signature_key)
        signed = self.blocks.pack_signature_with_ciphertext(signature, ciphertext)
        return b64encode(signed)

    def decrypt(self, ciphertext, passphrase):
        # 1. unarmor the ciphertext
        bundle = b64decode(ciphertext)
        signature_salt, signature, signed = (
            self.blocks.unpack_signature_and_ciphertext(bundle))

        key, signature_key = self.transmogrify_passphrase(passphrase, signature_salt)
        computed_signature = self.blocks.sign_ciphertext(signed, signature_key)

        (
            computed_signature,
            signature
        ) = map(lambda s: s.encode('hex'), [
            computed_signature,
            signature
        ])

        if computed_signature != signature:
            raise AESCTRIntegrityViolation.from_locals(locals())

        ciphertext, iv = self.blocks.unpack_ciphertext_and_iv(signed)

        engine = self.mode.engine(key, iv)
        plaintext = engine.decrypt(ciphertext)
        return plaintext
