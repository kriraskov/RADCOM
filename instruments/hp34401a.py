from .base import multimeter as dmm


class HP34401AD(dmm.Multimeter):
    """HP/Agilent 34401A Multimeter."""
    RANGES = {'100mV': 0.1, '1V': 1, '10V': 10, '100V': 100, '750V': 750,
              '1kV': 1000, '100Ohm': 100, '1kOhm': 1000, '10kOhm': 1e4,
              '100kOhm': 1e5, '1MOhm': 1e6, '10MOhm': 1e7, '100MOhm': 1e8,
              '10mA': 0.01, '100mA': 0.1, '1A': 1, '3A': 3}

    RATES = {'min': 0.02, 'slow': 0.2, 'medium': 1, 'fast': 10, 'max': 100}

    TRIGGER_TYPES = {'internal': 'IMM', 'external': 'EXT', 'bus': 'BUS'}

    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self._function = None
        self._trigger_source = None

    @property
    def function(self) -> str:
        return self.query('FUNC?')

    @function.setter
    def function(self, value: dmm.Function) -> None:
        self.write(f'FUNC "{value}"')
        self._function = value

    @property
    def range(self) -> str:
        return self.query(f'{self._function}:RANG?')

    @range.setter
    def range(self, value: dmm.Range) -> None:
        self.write(f'{self._function}:RANG {self.RANGES[value]}')

    @property
    def rate(self) -> str:
        return self.query(f'{self._function}:NPLC?')

    @rate.setter
    def rate(self, value: dmm.Rate) -> None:
        self.write(f'{self._function}:NPLC {self.RATES[value]}')

    @property
    def trigger_source(self) -> str:
        return self.query('TRIG:SOUR?')

    @trigger_source.setter
    def trigger_source(self, value: dmm.TriggerSource) -> None:
        self.write(f'TRIG:SOUR "{value}"')
        self._trigger_source = value

    @property
    def trigger_measurement(self) -> bool:
        return self._trigger_source == 'BUS'

    def remote(self) -> None:
        self.write('SYST:REM')

    def return_to_local(self) -> None:
        self.write('SYST:LOC')

    def read_val(self) -> float:
        return float(self.query('READ?'))

    def trigger(self) -> None:
        self.write('*TRG')
