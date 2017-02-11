from Crypto import Random
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256 as CSHA256
from Crypto.Hash import SHA as CSHA1

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.hashes import SHA256

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptonite.meta.checks import is_child_object
from cryptonite.exceptions import AESUnpaddingError
from cryptonite.exceptions import AESIVPackingError


def bits(count):
    return count / 8


class BaseBlock(object):
    backend = default_backend()

    @staticmethod
    def is_child_object(other):
        return is_child_object(BaseBlock, other)

    @classmethod
    def generate_iv(cls):
        return Random.new().read(cls.IVSIZE)

    @classmethod
    def pad(cls, ciphertext):
        string = bytes(ciphertext)
        blocksize = cls.BLKSIZE
        length = len(string)
        padmax = blocksize - length
        padsize = padmax % blocksize
        padbyte = chr(padsize)
        return string + (padsize * padbyte)

    @classmethod
    def unpad(cls, ciphertext):
        string = bytes(ciphertext)
        length = len(ciphertext)
        remaining = length % cls.BLKSIZE
        offset = cls.BLKSIZE - remaining
        if remaining:
            raise AESUnpaddingError.from_locals(locals())

        return string[:-ord(string[length - 1:])]

    @classmethod
    def pack_iv_and_ciphertext(cls, iv, ciphertext):
        method = 'pack_iv_and_ciphertext'
        expected_length = cls.IVSIZE
        iv_length = len(iv)
        if iv_length != expected_length:
            raise AESIVPackingError.from_locals(locals())

        packed = b''.join([iv, ciphertext])
        return packed

    @classmethod
    def unpack_iv_and_ciphertext(cls, packed):
        iv = packed[:cls.IVSIZE]
        ciphertext = packed[cls.IVSIZE:]
        return (iv, ciphertext)

    @classmethod
    def pbkdf2hmac(cls, iterations, secret, salt=None):
        salt = salt or Random.new().read(cls.IVSIZE)
        kdf = PBKDF2HMAC(
            algorithm=cls.HASHALGO(),
            length=cls.BLKSIZE,
            salt=salt,
            iterations=iterations,
            backend=cls.backend)

        key = kdf.derive(secret)

        return key, salt

    @classmethod
    def sign_ciphertext(cls, ciphertext, signature_key):
        hmac = HMAC.new(signature_key, ciphertext, cls.HMACALGO)
        signature = hmac.digest()
        return signature

    @classmethod
    def pack_signature_with_ciphertext(cls, signature, ciphertext):
        return ciphertext + signature

    @classmethod
    def unpack_signature_and_ciphertext(cls, bundle):
        # TODO: signature_salt ~> signature_salt
        signature_salt = bundle[:cls.IVSIZE]
        signature = bundle[-cls.BLKSIZE:]
        ciphertext = bundle[:-cls.BLKSIZE]
        return signature_salt, signature, ciphertext

    @classmethod
    def unpack_ciphertext_and_iv(cls, ciphertext):
        ciphertext = ciphertext[cls.IVSIZE:]
        ctr_iv = ciphertext[:cls.IVSIZE]
        return ciphertext, ctr_iv


class Block128(BaseBlock):
    HASHALGO = SHA1
    HMACALGO = CSHA1
    BLKSIZE = bits(128)
    IVSIZE = bits(128)


class Block256(BaseBlock):
    HASHALGO = SHA256
    HMACALGO = CSHA256
    BLKSIZE = bits(256)
    IVSIZE = bits(128)
