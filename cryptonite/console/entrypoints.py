
from __future__ import unicode_literals

import logging
import argparse
import warnings

from cryptonite.util import clean_temp_files

from cryptonite.console.gpg.base import get_main_parser_argv
from cryptonite.console.gpg.base import execute_command_gpg_version
from cryptonite.console.gpg.keys import execute_command_gpg_list
from cryptonite.console.gpg.keys import execute_command_gpg_create
from cryptonite.console.gpg.keys import execute_command_gpg_import
from cryptonite.console.gpg.keys import execute_command_gpg_show_keyid
from cryptonite.console.gpg.keys import execute_command_gpg_show_public
from cryptonite.console.gpg.keys import execute_command_gpg_show_private
from cryptonite.console.gpg.keys import execute_command_gpg_show_passphrase
from cryptonite.console.gpg.keys import execute_command_gpg_show
from cryptonite.console.gpg.keys import execute_command_gpg_delete
from cryptonite.console.gpg.crypto import execute_command_gpg_encrypt
from cryptonite.console.gpg.crypto import execute_command_gpg_decrypt
from cryptonite.console.gpg.crypto import execute_command_gpg_sign
from cryptonite.console.gpg.crypto import execute_command_gpg_verify
from cryptonite.console.gpg.operations import execute_command_gpg_quickstart
from cryptonite.console.gpg.operations import execute_command_gpg_wipe
from cryptonite.console.gpg.operations import execute_command_gpg_generate_backup
from cryptonite.console.gpg.operations import execute_command_gpg_recover_from_backup

from cryptonite.console.aes.cbc import execute_command_aes_128_cbc_encrypt
from cryptonite.console.aes.cbc import execute_command_aes_128_cbc_decrypt
from cryptonite.console.aes.cbc import execute_command_aes_256_cbc_encrypt
from cryptonite.console.aes.cbc import execute_command_aes_256_cbc_decrypt

from cryptonite.console.aes.ctr import execute_command_aes_128_ctr_encrypt
from cryptonite.console.aes.ctr import execute_command_aes_128_ctr_decrypt
from cryptonite.console.aes.ctr import execute_command_aes_256_ctr_encrypt
from cryptonite.console.aes.ctr import execute_command_aes_256_ctr_decrypt


warnings.catch_warnings()
warnings.simplefilter("ignore")


def gnupg():
    handlers = {
        'quickstart': execute_command_gpg_quickstart,
        'delete': execute_command_gpg_delete,
        'list': execute_command_gpg_list,
        'sign': execute_command_gpg_sign,
        'show': execute_command_gpg_show,
        'create': execute_command_gpg_create,
        'import': execute_command_gpg_import,
        'decrypt': execute_command_gpg_decrypt,
        'verify': execute_command_gpg_verify,
        'public': execute_command_gpg_show_public,
        'keyid': execute_command_gpg_show_keyid,
        'encrypt': execute_command_gpg_encrypt,
        'private': execute_command_gpg_show_private,
        'version': execute_command_gpg_version,
        'passphrase': execute_command_gpg_show_passphrase,
        'backup': execute_command_gpg_generate_backup,
        'recover': execute_command_gpg_recover_from_backup,
        'wipe': execute_command_gpg_wipe,
    }
    parser = argparse.ArgumentParser(prog='cryptonite')
    options = ", ".join(handlers.keys())
    help_msg = 'Available commands:\n\n{0}\n'.format(options)

    parser.add_argument('command', help=help_msg, choices=handlers.keys())

    argv = get_main_parser_argv()

    args = parser.parse_args(argv)

    if args.command not in handlers:
        parser.print_help()
        raise SystemExit(1)

    try:
        clean_temp_files()
    except:
        pass

    try:
        handlers[args.command]()
    except KeyboardInterrupt:
        print "\033[A\r                        "
        print "\033[A\r\rYou hit Control-C. Bye"
        raise SystemExit(1)

    except Exception:
        logging.exception("Failed to execute %s", args.command)
        raise SystemExit(1)


def aes():
    handlers = {
        'encrypt-128-cbc': execute_command_aes_128_cbc_encrypt,
        'decrypt-128-cbc': execute_command_aes_128_cbc_decrypt,
        'encrypt-128-ctr': execute_command_aes_128_ctr_encrypt,
        'decrypt-128-ctr': execute_command_aes_128_ctr_decrypt,
        'encrypt-256-cbc': execute_command_aes_256_cbc_encrypt,
        'decrypt-256-cbc': execute_command_aes_256_cbc_decrypt,
        'encrypt-256-ctr': execute_command_aes_256_ctr_encrypt,
        'decrypt-256-ctr': execute_command_aes_256_ctr_decrypt,
    }
    parser = argparse.ArgumentParser(prog='cryptonite')
    options = ", ".join(handlers.keys())
    help_msg = 'Available commands:\n\n{0}\n'.format(options)

    parser.add_argument('command', help=help_msg, choices=handlers.keys())

    argv = get_main_parser_argv()

    args = parser.parse_args(argv)

    if args.command not in handlers:
        parser.print_help()
        raise SystemExit(1)

    try:
        clean_temp_files()
    except:
        pass

    try:
        handlers[args.command]()
    except KeyboardInterrupt:
        print "\033[A\r                        "
        print "\033[A\r\rYou hit Control-C. Bye"
        raise SystemExit(1)

    except Exception:
        logging.exception("Failed to execute %s", args.command)
        raise SystemExit(1)
