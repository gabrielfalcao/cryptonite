import os
import io
import logging

from cryptonite import conf
from cryptonite.util import get_all_keyring_nodes
from cryptonite.util import initialize_key_home
from cryptonite.console.ui import get_bool
from cryptonite.console.base import get_sub_parser_argv

from cryptonite.operations.backup import BackupManager

logger = logging.getLogger('cryptonite')


def execute_command_generate_backup():
    from cryptonite.console.parsers.backup import parser

    args = parser.parse_args(get_sub_parser_argv())
    manager = BackupManager(conf.key_home, conf.path)

    print manager.generate_backup(args.path)


def execute_command_recover_from_backup():
    from cryptonite.console.parsers.recover import parser

    args = parser.parse_args(get_sub_parser_argv())
    manager = BackupManager(conf.key_home, conf.path)

    with io.open(args.path, 'rb') as fd:
        data = fd.read()

    manager.recover_backup(data, conf.path, args.force)


def execute_command_quickstart():
    from cryptonite.console.parsers.quickstart import parser

    args = parser.parse_args(get_sub_parser_argv())

    data, path = initialize_key_home(args.conf_path, args.home, args.force)
    width = max(map(len, data.splitlines()))

    print "\033[1;30m{0}".format('-' * width)
    print data.strip()
    print '-' * width
    print "\033[0m\033[1;33myou might want do add the following line to your ~/.bashrc", "\033[0m"
    print "export CRYPTONITE_CONFIG_PATH='{0}'".format(path)
    print


def execute_command_wipe():
    from cryptonite.console.parsers.wipe import parser

    args = parser.parse_args(get_sub_parser_argv())
    should_backup = not args.no_backup

    if should_backup:
        manager = BackupManager(conf.key_home, conf.path)
        manager.generate_backup(path=args.backup_path)

    deleted = False
    for node in get_all_keyring_nodes():
        if not os.path.exists(node.path):
            continue

        agreed = False
        if args.force:
            agreed = True
        else:
            agreed = get_bool('delete file: {0} ?'.format(node.path))

        if agreed:
            os.unlink(node.path)
            logger.warning('deleting: {0}'.format(node.path))
            deleted = True

    if not deleted:
        print "{0} already empty".format(conf.path)

    if should_backup:
        logger.info('a backup was generated at: {0}'.format(args.backup_path))
