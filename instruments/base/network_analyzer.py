from .instrument import Instrument, Channel
from abc import ABC, abstractmethod


class NetworkAnalyzer(ABC, Instrument):
    """Network analyzer base class."""
    @property
    @abstractmethod
    def sweep_type(self) -> str:
        ...

    @sweep_type.setter
    @abstractmethod
    def sweep_type(self, value: str) -> None:
        ...

    @property
    @abstractmethod
    def center_frequency(self) -> float:
        ...

    @center_frequency.setter
    @abstractmethod
    def center_frequency(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def frequency_span(self) -> float:
        ...

    @frequency_span.setter
    @abstractmethod
    def frequency_span(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def start_frequency(self) -> float:
        ...

    @start_frequency.setter
    @abstractmethod
    def start_frequency(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def stop_frequency(self) -> float:
        ...

    @stop_frequency.setter
    @abstractmethod
    def stop_frequency(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def cw_frequency(self) -> float:
        ...

    @cw_frequency.setter
    @abstractmethod
    def cw_frequency(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def frequency_sweep_length(self) -> int:
        ...

    @frequency_sweep_length.setter
    @abstractmethod
    def frequency_sweep_length(self, value: int) -> None:
        ...

    @property
    @abstractmethod
    def snp_frequency_units(self) -> str:
        ...

    @snp_frequency_units.setter
    @abstractmethod
    def snp_frequency_units(self, value: str) -> None:
        ...

    @property
    @abstractmethod
    def snp_parameter_format(self) -> str:
        ...

    @snp_parameter_format.setter
    @abstractmethod
    def snp_parameter_format(self, value: str) -> None:
        ...

    @abstractmethod
    def get_marker(self, number: int = 1, trace: int = 1) -> float:
        ...

    @abstractmethod
    def set_marker(self, x: float, number: int = 1, trace: int = 1) -> None:
        ...

    @abstractmethod
    def read_marker(self, number: int = 1, trace: int = 1) -> float:
        ...

    @abstractmethod
    def remote(self) -> None:
        ...

    @abstractmethod
    def return_to_local(self) -> None:
        ...

    def close(self) -> None:
        self.return_to_local()
        super().close()

    def setup_freq_sweep(self, sweep_length: int, start: float = None,
                         stop: float = None, center: float = None,
                         span: float = None, sweep_type: str = None) -> None:
        self.sweep_type = sweep_type
        self.frequency_sweep_length = sweep_length
        if (start and stop) and not (center or span):
            self.start_frequency = start
            self.stop_frequency = stop
        elif (center and span) and not (start or stop):
            self.center_frequency = center
            self.frequency_span = span
        else:
            raise ValueError('Incorrect sweep specification.')


class Port(ABC, Channel):
    @property
    @abstractmethod
    def power(self) -> float:
        ...

    @power.setter
    @abstractmethod
    def power(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def power_sweep_start(self) -> float:
        ...

    @power_sweep_start.setter
    @abstractmethod
    def power_sweep_start(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def power_sweep_stop(self) -> float:
        ...

    @power_sweep_stop.setter
    @abstractmethod
    def power_sweep_stop(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def power_sweep_length(self) -> int:
        ...

    @power_sweep_length.setter
    @abstractmethod
    def power_sweep_length(self, value: int) -> None:
        ...
