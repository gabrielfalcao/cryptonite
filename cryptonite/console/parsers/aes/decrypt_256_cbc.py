import argparse

parser = argparse.ArgumentParser(
    prog='cryptonite-aes decrypt-256-cbc',
    description='decrypts data in AES-CBC-256')

parser.add_argument(
    'plaintext',
    metavar='<plaintext>',
    help='a file or string to be decrypted'
)
parser.add_argument(
    'ciphertext',
    metavar='<ciphertext>',
    help='a file or string to be decrypted'
)
parser.add_argument(
    'passphrase',
    metavar='<passphrase>',
    help='the passphrase in which to use for deriving a private key'
)
