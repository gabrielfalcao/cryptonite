from abc import ABCMeta
from abc import abstractmethod

from cryptonite.meta.checks import is_subclass


class BaseCodec(object):
    __metaclass__ = ABCMeta

    def __init__(self, **params):
        self.setup(**params)

    @abstractmethod
    def initialize(self, **params):
        raise NotImplementedError

    @abstractmethod
    def encode(self, data):
        raise NotImplementedError

    @abstractmethod
    def decode(self, data):
        raise NotImplementedError


class CodecPipeline(BaseCodec):

    def setup(self, phases=None):
        if not phases:
            raise ValueError('CodecPipeline requires')

        self.steps = []
        for item in self.phases:
            if is_subclass(Phase, BaseCodec):
                PhaseClass = item
                phase = PhaseClass()
            elif is_instance(Phase, BaseCodec):
                phase = item
            else:
                msg = (
                    'CodecPipeline only accepts classes or instances of '
                    'codecs as a list members but got: {0} ({1})'
                )
                raise TypeError(msg.format(item, type(item)))

            self.steps.append(phase)

    def encode(self, data):
        # blablabla

    def decode(self, data):
        # blablabla
