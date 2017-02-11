from cryptonite.meta.meta import Locator
from cryptonite.meta.meta import get_member
from cryptonite.meta.meta import set_member
from cryptonite.meta.meta import TypeStore

from cryptonite.meta.checks import validates_subclass


BASE_CODECS = [
    'CodecMeta',
    'BaseCodec',
]


BASE_CIPHERS = [
    'CipherMeta',
    'BaseCipher',
    'BaseAES',
    'BaseAESCBC',
    'BaseAESCTR',
]


BASE_EXCEPTIONS = [
    'ExceptionMeta',
    'CryptoniteException',
]


class ExceptionMeta(type):
    store = TypeStore()

    def __init__(cls, name, bases, members):
        module = get_member(members, cls, '__module__')
        template = get_member(members, cls, '__template__')

        if validates_subclass(module, name, *BASE_EXCEPTIONS):
            if not template:
                raise TypeError(
                    '{} is a TemplateException subclasses that did not define a __template__')

        super(ExceptionMeta, cls).__init__(name, bases, members)


class CodecMeta(type):
    store = TypeStore()

    def __init__(cls, name, bases, members):
        module = get_member(members, cls, '__module__')
        label = get_member(members, cls, 'label')

        if validates_subclass(module, name, *BASE_CODECS):
            if not label:
                message = ' '.join((
                    '{}.label must be defined at class',
                    'level as a non-empty string'
                ))
                raise RuntimeError(message.format(name))

            locator = Locator.from_object(cls)
            set_member(members, cls, 'name', locator.to_string())
            CodecMeta.store.set(cls, label, cls)

        super(CodecMeta, cls).__init__(name, bases, members)


class CipherMeta(type):
    store = TypeStore()

    def __init__(cls, name, bases, members):
        module = get_member(members, cls, '__module__')
        label = get_member(members, cls, 'label')
        mode = get_member(members, cls, 'mode')
        blocks = get_member(members, cls, 'blocks')

        if validates_subclass(module, name, *BASE_CIPHERS):
            if not label:
                message = ' '.join((
                    '{}.label must be defined at class',
                    'level as a non-empty string'
                ))
                raise RuntimeError(message.format(name))

            if not mode:
                message = ' '.join((
                    '{}.mode must be defined at class',
                    'level as a reference to a BlockCipherModeBase'
                ))
                raise RuntimeError(message.format(name))

            if not blocks:
                message = ' '.join((
                    '{}.blocks must be defined at class',
                    'level as a reference to a BaseBlock'
                ))
                raise RuntimeError(message.format(name))

            CipherMeta.store.set(cls, label, {
                'mode': mode,
                'blocks': blocks,
            })

        super(CipherMeta, cls).__init__(name, bases, members)
