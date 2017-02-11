import io
import logging

from cryptonite.aes.ctr import AES128CTR
from cryptonite.aes.ctr import AES256CTR
from cryptonite.console.base import get_sub_parser_argv

logger = logging.getLogger('cryptonite')


def execute_command_aes_128_ctr_encrypt():
    from cryptonite.console.parsers.aes.encrypt_128_ctr import parser

    args = parser.parse_args(get_sub_parser_argv())
    aes = AES128CTR()

    read_fp = io.open(args.input_file, 'rb')
    write_fp = io.open(args.output_file, 'wb')

    for current, total in aes.encrypt_fp(args.passphrase, read_fp, write_fp):
        print "encrypted {current} of {totak} bytes".format(**locals())


def execute_command_aes_128_ctr_decrypt():
    from cryptonite.console.parsers.aes.decrypt_128_ctr import parser

    args = parser.parse_args(get_sub_parser_argv())
    aes = AES128CTR()

    read_fp = io.open(args.input_file, 'rb')
    write_fp = io.open(args.output_file, 'wb')

    for current, total in aes.decrypt_fp(args.passphrase, read_fp, write_fp):
        print "decrypted {current} of {totak} bytes".format(**locals())


def execute_command_aes_256_ctr_encrypt():
    from cryptonite.console.parsers.aes.encrypt_256_ctr import parser

    args = parser.parse_args(get_sub_parser_argv())
    aes = AES256CTR()

    read_fp = io.open(args.input_file, 'rb')
    write_fp = io.open(args.output_file, 'wb')

    for current, total in aes.encrypt_fp(args.passphrase, read_fp, write_fp):
        print "encrypted {current} of {totak} bytes".format(**locals())


def execute_command_aes_256_ctr_decrypt():
    from cryptonite.console.parsers.aes.decrypt_256_ctr import parser

    args = parser.parse_args(get_sub_parser_argv())
    aes = AES256CTR()

    read_fp = io.open(args.input_file, 'rb')
    write_fp = io.open(args.output_file, 'wb')

    for current, total in aes.decrypt_fp(args.passphrase, read_fp, write_fp):
        print "decrypted {current} of {totak} bytes".format(**locals())
