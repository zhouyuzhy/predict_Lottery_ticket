from abc import ABCMeta, abstractmethod


class IStrategy:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def is_call_signal(self, cur_data, history_data): raise NotImplementedError

    @abstractmethod
    def is_put_signal(self, cur_data, history_data): raise NotImplementedError
