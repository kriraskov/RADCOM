import pyvisa
from .base import network_analyzer as vna
from typing import Literal


SweepType = Literal['lin', 'log', 'power']

FrequencyUnit = Literal['Hz', 'kHz', 'MHz', 'GHz']

ParameterFormat = Literal['lin_phase', 'log_phase', 'real_imag']


class MS464xB(vna.NetworkAnalyzer):
    """Anritsu VectorStar MS464xB network analyzer.

    From the datasheet: "Each VNA channel is like a separate VNA."
    Hence, each `MS464xB` object represents a single VNA channel.

    Parameters:
        P1, P2: Ports 1 and 2 of the instrument.
    """
    PARAM_FORMATS = {'lin_phase': 'LINPH', 'log_phase': 'LOGHP',
                     'real_imag': 'REIM'}

    def __init__(self, resource_name: str, channel: int = 1,
                 query_delay: float = 0., timeout: int = 0,
                 write_termination: str = '\n', read_termination: str = '\r\n',
                 echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self.channel = channel
        self.__dict__['P1'] = MS464xBPort(1, self.channel, self.resource)
        self.__dict__['P2'] = MS464xBPort(2, self.channel, self.resource)
        self.write('LANG NATIVE')

    @property
    def sweep_type(self) -> str:
        return self.query(f':SENS{self.channel}:SWE:TYP?')

    @sweep_type.setter
    def sweep_type(self, value: SweepType) -> None:
        self.write(f':SENS{self.channel}:SWE:TYP ' + value)

    @property
    def center_frequency(self) -> float:
        return float(self.query(f':SENS{self.channel}:FREQ:CENT?'))

    @center_frequency.setter
    def center_frequency(self, value: float) -> None:
        self.write(f':SENS{self.channel}:FREQ:CENT {value}')

    @property
    def frequency_span(self) -> float:
        return float(self.query(f':SENS{self.channel}:FREQ:SPAN?'))

    @frequency_span.setter
    def frequency_span(self, value: float) -> None:
        self.write(f':SENS{self.channel}:FREQ:SPAN {value}')

    @property
    def start_frequency(self) -> float:
        return float(self.query(f':SENS{self.channel}:FREQ:STAR?'))

    @start_frequency.setter
    def start_frequency(self, value: float) -> None:
        self.write(f':SENS{self.channel}:FREQ:START {value}')

    @property
    def stop_frequency(self) -> float:
        return float(self.query(f':SENS{self.channel}:FREQ:STOP?'))

    @stop_frequency.setter
    def stop_frequency(self, value: float) -> None:
        self.write(f':SENS{self.channel}:FREQ:STOP {value}')

    @property
    def cw_frequency(self) -> float:
        return float(self.query(f':SENS{self.channel}:FREQ:CW?'))

    @cw_frequency.setter
    def cw_frequency(self, value: float) -> None:
        self.write(f':SENS{self.channel}:FREQ:CW {value}')

    @property
    def frequency_sweep_length(self) -> int:
        return int(self.query(f':SENS{self.channel}:SWE:POIN?'))

    @frequency_sweep_length.setter
    def frequency_sweep_length(self, value: int) -> None:
        self.write(f':SENS{self.channel}:SWE:POIN {value}')

    @property
    def snp_frequency_units(self) -> str:
        return self.query(':FORM:SNP:FREQ?')

    @snp_frequency_units.setter
    def snp_frequency_units(self, value: FrequencyUnit) -> None:
        self.write(f':FORM:SNP:FREQ {value}')

    @property
    def snp_parameter_format(self) -> str:
        return self.query(':FORM:SNP:PAR?')

    @snp_parameter_format.setter
    def snp_parameter_format(self, value: ParameterFormat) -> None:
        self.write(f':FORM:SNP:PAR {self.PARAM_FORMATS[value]}')

    @property
    def marker_format(self) -> str:
        return self.query(f':CALC{self.channel}:FORM?')

    @marker_format.setter
    def marker_format(self, fmt: ParameterFormat) -> None:
        self.write(f':CALC{self.channel}:FORM {fmt}')

    def get_marker(self, number: int = 1, trace: int = 1) -> float:
        return float(self.query(
            f':CALC{self.channel}:PAR{trace}:MARK{number}:X?'))

    def set_marker(self, x: float, number: int = 1, trace: int = 1) -> None:
        self.write(f':CALC{self.channel}:PAR{trace}:MARK{number}:ACT')
        self.write(f':CALC{self.channel}:PAR{trace}:MARK{number}:X {x}')

    def read_marker(self, number: int = 1, trace: int = 1) -> float:
        return float(self.query(
            f':CALC{self.channel}:PAR{trace}:MARK{number}:Y?'))

    def remote(self) -> None:
        # MS464xB switches to remote when any command is written.
        self.query('*IDN?')

    def return_to_local(self) -> None:
        print('RTL')
        self.resource.write('RTL')

    def measure(self, x: float, marker_number: int = 1, trace: int = 1,
                fmt: ParameterFormat = 'lin_phase') -> float:
        self.marker_format = fmt
        self.set_marker(x, marker_number, trace)
        self.write('TRS;WFS')
        return self.read_marker(marker_number, trace)

    def save_sweep(self, filename: str):
        self.write(f'TRS;WFS;SAVE "{filename}"')


class MS464xBPort(vna.Port):
    def __init__(self, number: int, channel: int, resource: pyvisa.Resource)\
            -> None:
        super().__init__(number, resource)
        self.channel = channel

    @property
    def power(self) -> float:
        return float(self.query(f':SOUR{self.channel}:POW:PORT{self.number}?'))

    @power.setter
    def power(self, value: float) -> None:
        self.write(f':SOUR{self.channel}:POW:PORT{self.number} {value}')

    @property
    def power_sweep_start(self) -> float:
        return float(self.query(
            f':SOUR{self.channel}:POW:PORT{self.number}:LIN:POW:STAR?'))

    @power_sweep_start.setter
    def power_sweep_start(self, value: float) -> None:
        self.write(
            f':SOUR{self.channel}:POW:PORT{self.number}:LIN:POW:STAR {value}')

    @property
    def power_sweep_stop(self) -> float:
        return float(self.query(
            f':SOUR{self.channel}:POW:PORT{self.number}:LIN:POW:STOP?'))

    @power_sweep_stop.setter
    def power_sweep_stop(self, value: float) -> None:
        self.write(
            f':SOUR{self.channel}:POW:PORT{self.number}:LIN:POW:STOP {value}')

    @property
    def power_sweep_length(self) -> int:
        return int(self.query(
            f':SOUR{self.channel}:POW:PORT{self.number}:LIN:POW:POIN?'))

    @power_sweep_length.setter
    def power_sweep_length(self, value: int) -> None:
        self.write(
            f':SOUR{self.channel}:POW:PORT{self.number}:LIN:POW:POIN {value}')
