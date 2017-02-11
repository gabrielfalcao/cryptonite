# -*- coding: utf-8 -*-
from cryptonite.ciphers import BaseCipher

from .modes import CTRMode
from .armor import cuirass
from .armor import uncuirass



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
