import os
import io
import tarfile
from cryptonite import conf
from cryptonite.util import temp_filename
from cryptonite.util import binary_to_plaintext
from cryptonite.util import plaintext_to_binary
from cryptonite.default import logger
from cryptonite.exceptions import InvalidBackupOperation


class BackupManager(object):

    def __init__(self, key_home, conf_path):
        self.key_home = os.path.abspath(key_home)
        self.conf_path = os.path.abspath(conf_path)

    def generate_backup(self, path):
        if not os.path.exists(self.key_home):
            raise InvalidBackupOperation(
                'the given key home does not exist: {0}'.format(self.key_home))

        if not os.path.isdir(self.key_home):
            raise InvalidBackupOperation(
                'the given key home is not a directory: {0}'.format(self.key_home))

        if not os.path.exists(self.conf_path):
            raise InvalidBackupOperation(
                'the given conf_path does not exist: {0}'.format(self.conf_path))

        if not os.path.isfile(self.conf_path):
            raise InvalidBackupOperation(
                'the given conf_path is not a valid file: {0}'.format(self.conf_path))

        tmp_path = temp_filename()
        tar = tarfile.open(tmp_path, format=tarfile.GNU_FORMAT, mode='w:bz2')

        def set_file_info(info):
            logger.info('Compressing {0}'.format(info.name))
            return info

        tar.add(self.key_home,
                arcname='keyring', filter=set_file_info)

        tar.add(self.conf_path,
                arcname='cryptonite.yml', filter=set_file_info)

        tar.close()

        data = io.open(tmp_path, 'rb').read()
        os.unlink(tmp_path)

        encoded = binary_to_plaintext(data)
        if path:
            with io.open(path, 'wb') as fd:
                fd.write(encoded)

        return encoded

    def recover_backup(self, encoded, conf_path, force=False):
        binary = plaintext_to_binary(encoded)
        tmp_path = temp_filename()
        with io.open(tmp_path, 'wb') as fd:
            fd.write(binary)

        tar = tarfile.open(tmp_path, format=tarfile.GNU_FORMAT, mode='r:bz2')
        members = dict([(m.name, m) for m in tar.getmembers()])

        conf_member = members.pop('cryptonite.yml')
        if not conf_member:
            raise InvalidBackupOperation(
                'the backup file is invalid because does not contain a cryptonite.yml file')

        expected_members = {
            'keyring',
            'keyring/pubring.gpg',
            'keyring/pubring.gpg~',
            'keyring/random_seed',
            'keyring/secring.gpg',
            'keyring/trustdb.gpg'
        }
        difference = set(members.keys()).difference(expected_members)
        if len(difference) > 0:
            raise InvalidBackupOperation(
                'the backup file is invalid because it contains invalid members: {0}'.format(", ".join(sorted(difference))))

        # we don't care about the keyring
        members.pop('keyring')

        if os.path.exists(conf_path):
            msg = 'replacing config file: {0}'.format(conf_path)
            if force:
                logger.warning(msg)
            else:
                raise InvalidBackupOperation(msg)

        rawconf = tar.extractfile(conf_member).read()
        with io.open(conf_path, 'wb') as fd:
            fd.write(rawconf)

        conf.setup_from_config_path(conf, conf_path)

        if os.path.exists(conf.key_home):
            msg = 'replacing existing key home: {0}'.format(conf.key_home)
            if force:
                logger.warning(msg)
            else:
                raise InvalidBackupOperation(msg)
        else:
            logger.info(
                'creating key home directory {0}'.format(conf.key_home))
            os.makedirs(conf.key_home)

        logger.info('setting mode 0700 on directory {0}'.format(conf.key_home))
        os.chmod(conf.key_home, 0700)

        for member in members.values():
            raw = tar.extractfile(member).read()
            dst = os.path.join(conf.key_home, os.path.basename(member.name))
            with io.open(dst, 'wb') as fd:
                logger.info('writing keyring file {0}'.format(dst))
                fd.write(raw)
                logger.info('setting mode 0600 on {0}'.format(dst))
                os.chmod(dst, 0600)
