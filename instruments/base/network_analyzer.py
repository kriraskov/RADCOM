from .instrument import Instrument, Channel
from abc import ABC, abstractmethod
from typing import Literal
import pyvisa


SweepType = Literal['lin', 'log', 'power']

FrequencyUnit = Literal['Hz', 'kHz', 'MHz', 'GHz']

ParameterFormat = Literal['lin_phase', 'log_phase', 'real_imag']


class NetworkAnalyzer(ABC, Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self.ports = list()

    @property
    @abstractmethod
    def sweep_type(self):
        ...

    @sweep_type.setter
    @abstractmethod
    def sweep_type(self, value: SweepType):
        ...

    @property
    @abstractmethod
    def center_frequency(self):
        ...

    @center_frequency.setter
    @abstractmethod
    def center_frequency(self, value: float):
        ...

    @property
    @abstractmethod
    def frequency_span(self):
        ...

    @frequency_span.setter
    @abstractmethod
    def frequency_span(self, value: float):
        ...

    @property
    @abstractmethod
    def start_frequency(self):
        ...

    @start_frequency.setter
    @abstractmethod
    def start_frequency(self, value: float):
        ...

    @property
    @abstractmethod
    def stop_frequency(self):
        ...

    @stop_frequency.setter
    @abstractmethod
    def stop_frequency(self, value: float):
        ...

    @property
    @abstractmethod
    def cw_frequency(self):
        ...

    @cw_frequency.setter
    @abstractmethod
    def cw_frequency(self, value: float):
        ...

    @property
    @abstractmethod
    def frequency_sweep_length(self):
        ...

    @frequency_sweep_length.setter
    @abstractmethod
    def frequency_sweep_length(self, value: int):
        ...

    @property
    @abstractmethod
    def snp_frequency_units(self):
        ...

    @snp_frequency_units.setter
    @abstractmethod
    def snp_frequency_units(self, value: FrequencyUnit):
        ...

    @property
    @abstractmethod
    def snp_parameter_format(self):
        ...

    @snp_parameter_format.setter
    @abstractmethod
    def snp_parameter_format(self, value: ParameterFormat):
        ...

    @abstractmethod
    def get_marker(self, number: int = 1, trace: int = 1):
        ...

    @abstractmethod
    def set_marker(self, x: float, number: int = 1, trace: int = 1):
        ...

    @abstractmethod
    def read_marker(self, number: int = 1, trace: int = 1):
        ...

    @abstractmethod
    def remote(self):
        ...

    @abstractmethod
    def return_to_local(self):
        ...

    def close(self):
        self.return_to_local()
        super().close()

    def config_freq_sweep(self, sweep_length: int, start: float = None,
                          stop: float = None, center: float = None,
                          span: float = None, sweep_type: SweepType = 'lin'):
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
    def __init__(self, number: int, resource: pyvisa.Resource,
                 echo: bool = False, sync: bool = False):
        super().__init__(number, resource, echo, sync)

    @property
    @abstractmethod
    def power(self):
        ...

    @power.setter
    @abstractmethod
    def power(self, value: int):
        ...

    @property
    @abstractmethod
    def power_sweep_start(self):
        ...

    @power_sweep_start.setter
    @abstractmethod
    def power_sweep_start(self, value: float):
        ...

    @property
    @abstractmethod
    def power_sweep_stop(self):
        ...

    @power_sweep_stop.setter
    @abstractmethod
    def power_sweep_stop(self, value: float):
        ...

    @property
    @abstractmethod
    def power_sweep_length(self,):
        ...

    @power_sweep_length.setter
    @abstractmethod
    def power_sweep_length(self, value: float):
        ...

    def config_power_sweep(self, sweep_length: int, cw_frequency: float,
                           start: float, stop: float):
        super().sweep_type = 'power'
        super().cw_frequency = cw_frequency
        self.power_sweep_start = start
        self.power_sweep_stop = stop
        self.power_sweep_length = sweep_length


