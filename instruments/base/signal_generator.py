from .instrument import Instrument, Channel
from abc import ABC, abstractmethod


class SignalGenerator(ABC, Instrument):
    """Base class for signals generators."""
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self.reset()
        self.clear()
        self.remote()
        

class OutputChannel(ABC, Channel):
    """An output channel of the signal generator."""
    @property
    @abstractmethod
    def enable(self):
        """Enable the channel."""
        ...
    
    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...
    
    @property
    @abstractmethod
    def frequency(self):
        """Output frequency of the signal."""
        ...
    
    @frequency.setter
    @abstractmethod
    def frequency(self, value: float):
        ...
    
    @property
    @abstractmethod
    def power(self):
        """Output power in dBm of the signal."""
        ...
    
    @power.setter
    @abstractmethod
    def power(self, value: float):
        ...
        