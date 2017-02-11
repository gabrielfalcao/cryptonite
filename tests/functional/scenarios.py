import re
import os


def generate_passphrase(length=27):
    return re.sub(r'\W+', 'a', os.urandom(27).encode('base64').strip('='))


def generate_humanized_bytes(count):
    if count & 1:
        raise RuntimeError(
            'can only generate an even amount of bytes'
        )

    return os.urandom(count / 2).encode('hex')
