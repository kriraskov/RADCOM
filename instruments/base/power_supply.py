from .instrument import Instrument, Channel
from abc import ABC, abstractmethod


class PowerSupply(ABC, Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        #self.reset()
        #self.clear()
        #self.remote()
        
    
    @abstractmethod
    def remote(self):
        ...


class OutputChannel(ABC, Channel):
    @property
    @abstractmethod
    def enable(self):
        ...
        
    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...
        
    @property
    @abstractmethod
    def voltage(self):
        ...
        
    @voltage.setter
    @abstractmethod
    def voltage(self, value: float):
        ...
    
    @property
    @abstractmethod
    def current(self):
        ...
        
    @current.setter
    @abstractmethod
    def current(self, value: float):
        ...
        