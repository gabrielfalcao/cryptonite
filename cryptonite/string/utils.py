from cryptonite.version import version

"""
NOTES:
- consider using Base58 for armoring the different types of ciphers and modes:
  - GPG
  - AES-256-CBC
  - AES-256-CTR
"""


def ensure_unicode(data):
    return data.encode('utf-8')


def binary_to_plaintext(data, header):
    return "\n".join([
        '-----BEGIN {}-----'.format(header),
        'Version: Cryptonite v{}'.format(version),
        '',
        data.encode('base64').encode('rot13'),
        '-----END {}-----'.format(header),
    ])


def plaintext_to_binary(data):
    return "\n".join(data.strip().splitlines()[3:-1]).strip().decode('base64')


def wrap_lines(string, limit=80):
    return b"\n".join([string[i:i + limit] for i in range(0, len(string), limit)])


def unwrap_lines(string):
    return b"".join(string.splitlines())
