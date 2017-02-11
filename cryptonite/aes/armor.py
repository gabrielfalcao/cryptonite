import bz2
from base64 import b64encode
from base64 import b64decode


def cuirass(data):
    """armor a cipher-text after encrypting:
    - compress bz2
    - encode base64
    """
    return b64encode(bz2.compress(data, compresslevel=9))


def uncuirass(data):
    """unarmor a cipher-text before decrypting, reverse order of :py:function:`plackart`:
    - decode base64
    - decompress bz2
    """
    return bz2.decompress(b64decode(data))
