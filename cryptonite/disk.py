import os
import re
import yaml
from plant import Node
from cryptonite import conf
from cryptography.fernet import Fernet
from cryptonite.default import logger
from cryptonite.exceptions import InvalidBackupOperation


def get_all_keyring_nodes():
    nodes = [
        Node(conf.path)
    ]
    nodes.extend(map(Node, Node(conf.key_home).walk(lazy=False)))
    return nodes


def initialize_key_home(conf_path, key_home_path='./keys', force=False):
    raw = yaml.dump({
        'fernet_key': Fernet.generate_key(),
        'key_home': key_home_path,
    }, default_flow_style=False)

    conf_path = os.path.abspath(conf_path)
    if os.path.exists(conf_path):
        msg = 'replacing config file: {0}'.format(conf_path)
        if force:
            logger.warning(msg)
        else:
            raise InvalidBackupOperation(msg)

    with open(conf_path, 'wb') as fd:
        fd.write(raw)

    return raw, conf_path


def temp_filename():
    return '/tmp/cryptonite.{0}.tmptz2'.format(os.urandom(32).encode('hex'))


def clean_temp_files():
    regex = re.compile(r'cryptonite[.][a-z0-9]{64}.tmptz2')
    for path in os.listdir('/tmp'):
        if regex.search(path):
            os.unlink(path)
