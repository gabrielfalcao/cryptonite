import re
import logging

logger = logging.getLogger('cryptonite')
uid_regex = re.compile(
    r'(?P<name>.*?)\s*([(](?P<metadata>[^)]+)[)])?\s*[<]\s*(?P<email>[^>]+)\s*[>]\s*')


def unique(iterable):
    result = []

    for x in iterable:
        if x in result:
            continue

        result.append(x)

    return result
