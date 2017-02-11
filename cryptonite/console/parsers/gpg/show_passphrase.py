import argparse

parser = argparse.ArgumentParser(
    prog='cryptonite passphrase',
    description='prints the passphrase for the given recipient')

parser.add_argument('recipient', metavar='<recipient>',
                    help='any identification for the key: fingerprint, id or email')
