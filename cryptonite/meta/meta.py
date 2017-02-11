# -*- coding: utf-8 -*-

import sys
import copy
from collections import OrderedDict


class Locator(object):

    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name

    def to_string(self):
        return '.'.join((self.module_name, self.class_name))

    def __cmp__(self, other):
        return isinstance(other, Locator) and other.to_string() == self.to_string()

    def __hash__(self):
        return int(self.module_name.encode('hex'), 16) ^ int(self.class_name.encode('hex'), 16)

    @property
    def module(self):
        return sys.modules[self.module_name]

    def locate(self):
        return getattr(self.module, self.class_name, None)

    def matches_class(self, Class):
        return self.locate() == Class

    @classmethod
    def from_location(cls, module_name, class_name):
        return cls(module_name, class_name)

    @classmethod
    def from_object(cls, obj):
        location = cls.extract_location(obj)
        return cls.from_location(*location)

    @classmethod
    def extract_location(cls, obj):
        if not isinstance(obj, type):
            return cls.extract_location(obj.__class__)

        return (obj.__module__, obj.__name__)

    @classmethod
    def extract_path(cls, obj):
        parts = cls.extract_location(obj)
        return '.'.join(parts)


class TypeStore(object):

    def __init__(self):
        self.type_key_mapping = OrderedDict()
        self.key_mapping = OrderedDict()
        self.class_mapping = OrderedDict()
        self.locator_mapping = OrderedDict()
        self.__meta = None
        self.__base = None

    def set_base(self, BaseClass):
        self.__base = BaseClass

    def set_meta(self, MetaClass):
        self.__meta = MetaClass

    def set(self, Class, key, value):
        if key in self.key_mapping:
            msg = '{} already mapped by {}'
            raise ValueError(msg.format(key, self.__base))

        self.key_mapping[key] = value
        self.class_mapping[Class] = key
        self.locator_mapping[Locator.from_object(Class)] = key

    def get_by_key(self, key):
        return self.key_mapping[key]

    def get_by_class(self, Class):
        return self.class_mapping[Class]


def get_member(members, cls, key):
    return copy.deepcopy(members.get(key) or getattr(cls, key, None))


def set_member(members, cls, key, value):
    members[key] = value
    setattr(cls, key, value)
