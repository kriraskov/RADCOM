from .instrument import Instrument
from abc import ABC, abstractmethod
from typing import Literal


Function = Literal['CURR:AC', 'CURR:DC', 'CONT', 'DIOD', 'FREQ', 'RES',
                   'VOLT:AC', 'VOLT:DC']

Range = Literal['300mV', '3V', '30V', '300V', '750V', '1kV', '300Ohm', '3kOhm',
                '30kOhm', '300kOhm', '3MOhm', '30MOhm', '300MOhm', '10mA',
                '30mA', '100mA', '1A', '3A', '10A', '1000Hz', '10kHz',
                '100kHz', '1000kHz', '1MHz', '100mV', '1V', '10V', '100V',
                '100Ohm', '1kOhm', '10kOhm', '100kOhm', '1MOhm', '10MOhm',
                '100MOhm']

Rate = Literal['min', 'slow', 'medium', 'fast', 'max']

TriggerSource = Literal['internal', 'external', 'bus']


class Multimeter(ABC, Instrument):
    """Multimeter base class."""
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self._trigger_measurement = False
        self.reset()
        self.clear()
        self.remote()

    @property
    @abstractmethod
    def function(self) -> str:
        """Operation mode of the multimeter."""
        ...

    @function.setter
    @abstractmethod
    def function(self, value: Function) -> None:
        ...

    @property
    @abstractmethod
    def range(self) -> str:
        """Measurement range."""
        ...

    @range.setter
    @abstractmethod
    def range(self, value: Range) -> None:
        ...

    @property
    @abstractmethod
    def rate(self) -> str:
        """Measurement rate."""
        ...

    @rate.setter
    @abstractmethod
    def rate(self, value: Rate) -> None:
        ...

    @property
    @abstractmethod
    def trigger_source(self) -> str:
        """Trigger source."""
        ...

    @trigger_source.setter
    @abstractmethod
    def trigger_source(self, value: TriggerSource) -> None:
        ...

    @property
    @abstractmethod
    def trigger_measurement(self) -> bool:
        """The trigger mode requires an external trigger."""
        ...

    @abstractmethod
    def remote(self) -> str:
        """Configure the multimeter for remote operation."""
        ...

    @abstractmethod
    def return_to_local(self) -> None:
        """Configure the multimeter for local operation."""
        ...

    @abstractmethod
    def read_val(self) -> float:
        """Read the measured value."""
        ...

    def measure(self) -> float:
        """Trigger a measurement and read the results."""
        if self.trigger_measurement:
            self.trigger()
        return self.read_val()

    def close(self) -> None:
        """Return to local and close the resource."""
        self.return_to_local()
        super().close()

    def setup(self, func: Function, rate: Rate, range_: Range,
              trigger_type: TriggerSource, echo: bool = False) -> None:
        """Set up the multimeter.

        Args:
            func (Function): Operation mode of the multimeter.
            rate (Rate): Measurement rate.
            range_ (Range): Measurement range.
            trigger_type (TriggerSource): Trigger source.
            echo (bool): Echo commands.
        """
        self.echo = echo
        self.function = func
        self.rate = rate
        self.range = range_
        self.trigger_source = trigger_type
