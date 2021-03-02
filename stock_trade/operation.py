from abc import ABCMeta, abstractmethod


class IOperation:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def do_operation(self, asset, cur_data, history_data_15min, history_data_day): raise NotImplementedError