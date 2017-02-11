from itertools import chain
from cryptonite.util import unique
from cryptonite.meta.meta import Locator

DEFAULT_FORBIDDEN_CLASSES = (
    # meta-classes
    'ExceptionMeta',
    'CodecMeta',
    'CipherMeta',

    # base-classes
    'CryptoniteException',
    'BaseCipher',
    'BaseCodec',
)

# # TODO:
# from cryptonite.meta.locators import CipherLocator
# from cryptonite.meta.locators import CodecLocator
# from cryptonite.meta.locators import ExceptionLocator
#
# DEFAULT_FORBIDDEN_LOCATORS = (
#     CipherLocator,
#     CodecLocator,
#     ExceptionLocator,
#
# )


DEFAULT_FORBIDDEN_MODULES = (
    'cryptonite.meta',
)


class TypeGuard(object):
    """a gate-keeper for types and their metaclasses"""

    def __init__(self, forbidden_modules, forbidden_classes):
        self.forbidden_classes = unique(
            chain(DEFAULT_FORBIDDEN_CLASSES, forbidden_classes))
        self.forbidden_modules = unique(
            chain(DEFAULT_FORBIDDEN_MODULES, forbidden_modules))

    def check_module_name(self, name):
        return validates_module(name, self.forbidden_module_names)

    def check_class_name(self, name):
        return validates_subclass(name, self.forbidden_class_names)

    def check_object(self, TypeObject):
        locator = Locator.from_object(TypeObject)
        return self.check_locator(locator)

    def check_locator(self, locator):
        if not isinstance(locator, Locator):
            msg = (
                'TypeGuard.check_locator() needs a '
                'Locator instance as argument but got: {0} - {1}'
            )
            raise TypeError(msg.format(locator, type(locator)))

        checks = [
            self.check_module_name(locator.module_name),
            self.check_class_name(locator.class_name),
        ]

        return all(checks)


def validates_module(name, *forbidden_modules):
    forbidden_modules = (__name__, ) + forbidden_modules
    checks = []
    for forbidden in forbidden_modules:
        checks.append(not forbidden.startswith(name))
        checks.append(not name.startswith(forbidden))

    return all(checks)


def validates_subclass(module, name, *forbidden_names):
    checks = [validates_module(module)]
    for forbidden in forbidden_names:
        checks.append(name.strip() != forbidden.strip())

    return all(checks)


def is_subclass(Class, other):
    return isinstance(other, type) and issubclass(other, Class)


def is_instance(Class, other):
    return isinstance(other, Class)


def is_child_object(Class, other):
    return is_subclass(Class, other) or is_instance(Class, other)
