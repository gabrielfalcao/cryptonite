from cryptonite.meta.classes import ExceptionMeta


class CryptoniteException(Exception):
    """allows subclasses to define a __template__ that will be rendered
    with the _``**kwargs``_ provided to their constructor."""

    __metaclass__ = ExceptionMeta

    def __init__(self, **kw):
        context = {
            '__name__': self.__class__.__name__,
        }
        context.update(self.process_context(**kw))

        rendered = self.__template__.format(**context)
        super(CryptoniteException, self).__init__(rendered)

    def process_context(self, **context):
        return context

    @classmethod
    def from_locals(__cls__, context):
        context['__self__'] = context.pop('self', None)
        return __cls__(**context)


class AESUnpaddingError(CryptoniteException):
    __template__ = (
        '{cls.__name__}.unpad() got invalid string '
        'with length={length} and offset={offset}'
    )


class AESIVPackingError(CryptoniteException):
    __template__ = (
        '{cls.__name__}.{method}() '
        'failed because the provided iv has wrong length: '
        '{iv_length} != {expected_length}'
    )


class InvalidOperation(CryptoniteException):
    __template__ = (
        'could not perform {operation} because {reason}'
    )


class InvalidBackupOperation(InvalidOperation):

    def process_context(self, **context):
        context['action'] = 'backup'
        return context


class CodecError(CryptoniteException):
    __template__ = (
        'Error when using codec {Codec.name}: {message}'
    )


class AESCTRIntegrityViolation(CryptoniteException):
    __template__ = (
        'cannot decrypt due to hmac digest mismatch: {computed_signature} != {signature}'
    )
