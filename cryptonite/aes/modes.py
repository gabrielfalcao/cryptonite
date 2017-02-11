from Crypto.Cipher import AES
from Crypto.Util import Counter

from cryptonite.meta.checks import is_child_object


class BlockCipherModeBase(object):
    @classmethod
    def create_engine(cls, key, **kw):
        return AES.new(key, cls.MODE, **kw)

    @classmethod
    def valid(cls, other):
        return

    @staticmethod
    def is_child_object(other):
        return is_child_object(BlockCipherModeBase, other)


class CBCMode(BlockCipherModeBase):
    MODE = AES.MODE_CBC

    @classmethod
    def engine(cls, key, iv):
        return cls.create_engine(key, IV=iv)


class CTRMode(BlockCipherModeBase):
    MODE = AES.MODE_CTR

    @classmethod
    def engine(cls, key, iv):
        ctr = Counter.new(128, initial_value=int(iv.encode('hex'), 16))
        return cls.create_engine(key, counter=ctr)
