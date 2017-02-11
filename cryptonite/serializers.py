import re
import json

uid_regex = re.compile(
    r'(?P<name>.*?)\s*([(](?P<metadata>[^)]+)[)])?\s*[<]\s*(?P<email>[^>]+)\s*[>]\s*')


class GPGSerializer(object):

    def __init__(self, parent):
        self.parent = parent

    def extract_uid(self, uids):
        found = [x.groupdict()
                 for x in filter(bool, map(uid_regex.search, uids))]
        if not found:
            return None

        first = found[0]
        return self.get_decrypted_metadata(first)

    def get_private_key(self, item):
        keyid = item['keyid']
        return self.parent.gpg.export_keys([keyid], True)

    def get_public_key(self, item):
        keyid = item['keyid']
        return self.parent.gpg.export_keys([keyid], False)

    def get_decrypted_metadata(self, item):
        meta = item['metadata']
        if not meta:
            return item

        plain = self.parent.symmetric.decrypt(meta)
        try:
            return json.loads(plain)
        except ValueError:
            return item

    def key(self, key):
        uid = self.extract_uid(key['uids'])
        if uid:
            key.pop('uids', None)
            key.update(uid)

        if 'email' not in key:
            key['email'] = b'<none> '

        key['public'] = self.get_public_key(key)
        key['private'] = self.get_private_key(key)
        return key
