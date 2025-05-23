
from __future__ import unicode_literals

import io
import json
import sys
import logging
from prettytable import PrettyTable

from cryptonite.core import Cryptonite
from cryptonite.core import KeyAlreadyExists
from cryptonite.core import InvalidKeyError
from cryptonite.util import ensure_unicode

from cryptonite.console.ui import get_bool
from cryptonite.console.ui import get_passphrase
from cryptonite.console.base import get_sub_parser_argv
from cryptonite.console.util import is_file_and_exists


logger = logging.getLogger('cryptonite')


class color:
    red = staticmethod(lambda x: "\033[1;31m{0}\033[0m".format(x))
    green = staticmethod(lambda x: "\033[1;32m{0}\033[0m".format(x))
    yellow = staticmethod(lambda x: "\033[1;33m{0}\033[0m".format(x))
    blue = staticmethod(lambda x: "\033[1;34m{0}\033[0m".format(x))
    white = staticmethod(lambda x: "\033[1;37m{0}\033[0m".format(x))
    grey = staticmethod(lambda x: "\033[1;30m{0}\033[0m".format(x))


def execute_command_gpg_create():
    from cryptonite.console.parsers.generate_key import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = Cryptonite()
    if args.secret:
        passphrase = args.secret
    elif args.no_secret:
        passphrase = None
    else:
        passphrase = get_passphrase()

    name = args.name
    email = args.email
    password = passphrase
    try:
        key = gee.generate_key(name, email, password)
        logger.info("Generated: {0}".format(key))
    except KeyAlreadyExists as e:
        logger.error(
            'key already exists: email={email}, id={keyid}'.format(**e.key))
        raise SystemExit(1)


def execute_command_gpg_list():
    from cryptonite.console.parsers.list_keys import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = Cryptonite()
    table = PrettyTable([
        color.grey('keyid'),
        color.grey('fingerprint'),
        color.grey('email'),
        color.grey('private'),
        color.grey('public'),
    ])

    for key in gee.list_keys():
        if args.private and not key['private']:
            continue

        if args.public and key['private']:
            continue

        if args.email:
            print key['email']
        else:
            table.add_row([
                color.white(key['keyid']),
                color.white(key['fingerprint']),
                color.green(key['email']),
                bool(key.get('private')) and color.blue(
                    'yes') or color.yellow('no'),
                bool(key.get('public')) and color.blue(
                    'yes') or color.yellow('no'),
            ])

    if not args.email:
        print table.get_string()


def execute_command_gpg_import():
    from cryptonite.console.parsers.import_key import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = Cryptonite()
    key = args.key
    if not key:
        key = sys.stdin.read()

    elif is_file_and_exists(key):
        key = io.open(key, 'rb').read()

    key = "\n".join([x.strip() for x in key.splitlines()])
    try:
        result = gee.import_key(key)
    except InvalidKeyError as e:
        logger.error('failed to import key: {0}'.format(e))
        raise SystemExit(1)

    for x in result.fingerprints:
        logger.info('imported: %s', x)


def execute_command_gpg_show_public():
    from cryptonite.console.parsers.show_public import parser

    args = parser.parse_args(get_sub_parser_argv())
    args
    gee = Cryptonite()
    key = gee.get_key(args.recipient, public=True, private=False)
    if key['public']:
        print key['public']


def execute_command_gpg_show_keyid():
    from cryptonite.console.parsers.show_keyid import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = Cryptonite()

    key = gee.get_key(args.recipient, public=True, private=True)
    print key['keyid']


def execute_command_gpg_show_private():
    from cryptonite.console.parsers.show_private import parser

    args = parser.parse_args(get_sub_parser_argv())
    args
    gee = Cryptonite()
    key = gee.get_key(args.recipient, private=True, public=False)
    pkey = key.get('private')
    if not pkey:
        raise SystemExit(1)

    print key['private']


def execute_command_gpg_show_passphrase():
    from cryptonite.console.parsers.show_passphrase import parser

    args = parser.parse_args(get_sub_parser_argv())
    args
    gee = Cryptonite()
    key = gee.get_key(args.recipient, private=True, public=False)
    passphrase = key.get('passphrase')

    if passphrase:
        print passphrase


def execute_command_gpg_show():
    from cryptonite.console.parsers.show import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = Cryptonite()
    key = gee.get_key(args.recipient, private=True, public=True)
    if not key:
        raise SystemExit(1)

    print json.dumps(key, indent=2)


def execute_command_gpg_delete():
    from cryptonite.console.parsers.delete_key import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = Cryptonite()

    key = gee.get_key(args.recipient, private=True, public=True)
    if not key['fingerprint']:
        print "\033[1;31mno such key\033[0m"
        raise SystemExit(1)

    parts = map(ensure_unicode, filter(
        bool, [key[x] for x in ['email', 'keyid', 'fingerprint']]))
    msg = b" ".join(parts)

    agreed = False
    if args.force:
        agreed = True
    else:
        agreed = get_bool(u'Delete the key {0} ?'.format(msg))

    if agreed:
        print "deleting", msg
        print gee.delete_key(key['fingerprint'])
    else:
        print "\033[1;31mnot deleting", msg, "\033[0m"
