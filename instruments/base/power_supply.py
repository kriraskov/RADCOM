from .instrument import Instrument, Channel
from abc import ABC, abstractmethod


class PowerSupply(ABC, Instrument):
    """Base class for power supplies."""
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        #self.reset()
        #self.clear()
        #self.remote()

    @abstractmethod
    def remote(self) -> None:
        """Configure the power supply for remote operation."""
        ...

    @abstractmethod
    def return_to_local(self) -> None:
        """Configure the power supply for local operation."""
        ...


class OutputChannel(ABC, Channel):
    @property
    @abstractmethod
    def enable(self) -> bool:
        """Enable the channel."""
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool) -> None:
        ...

    @property
    @abstractmethod
    def voltage(self) -> float:
        """Set the voltage of the channel."""
        ...

    @voltage.setter
    @abstractmethod
    def voltage(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def current(self) -> float:
        """Set the current of the channel."""
        ...

    @current.setter
    @abstractmethod
    def current(self, value: float) -> None:
        ...
