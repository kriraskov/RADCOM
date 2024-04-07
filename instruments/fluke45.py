from .base import multimeter as dmm


class Fluke45(dmm.Multimeter):
    """Fluke45 Multimeter."""
    FUNCS = {'CURR:AC': 'AAC', 'CURR:DC': 'ADC', 'CONT': 'CONT',
             'DIOD': 'DIODE', 'FREQ': 'FREQ', 'RES': 'OHMS',
             'VOLT:AC': 'VAC', 'VOLT:DC': 'VDC'}

    RANGES = {'300mV': 1, '3V': 2, '30V': 3, '300V': 4, '1000V': 5,
              '300Ohm': 1, '3kOhm': 2, '30kOhm': 3, '300kOhm': 4, '3MOhm': 5,
              '30MOhm': 6, '300MOhm': 7, '30mA': 1, '10mA': 1, '100mA': 2,
              '10A': 3, '1000Hz': 1, '10kHz': 2, '100kHz': 3, '1000kHz': 4,
              '1MHz': 5, '100mV': 1, '1V': 2, '10V': 3, '100V': 4, '750V': 4,
              '100Ohm': 1, '1kOhm': 2, '10kOhm': 3, '100kOhm': 4, '1MOhm': 5,
              '10MOhm': 6, '100MOhm': 7}

    RATES = {'min': 'S', 'slow': 'S', 'medium': 'M', 'fast': 'F',
             'max': 'F'}

    TRIGGER_TYPES = {'internal': 1, 'external': 5, 'bus': 3}

    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self._trigger_source = 0

    @property
    def function(self) -> str:
        return self.query('FUNC1?')

    @function.setter
    def function(self, value: dmm.Function) -> None:
        self.write(self.FUNCS[value])

    @property
    def function2(self) -> str:
        return self.query('FUNC2?')

    @function2.setter
    def function2(self, value: dmm.Function) -> None:
        if self.FUNCS[value] == 'CONT':
            raise ValueError('Continuity test (CONT) is not available for'
                             'secondary display.')
        self.write(f'{self.FUNCS[value]}2')

    @property
    def range(self) -> str:
        return self.query('RANGE1?')

    @range.setter
    def range(self, value: dmm.Range) -> None:
        self.write(f'RANGE {self.RANGES[value]}')

    @property
    def rate(self) -> str:
        return self.query('RATE?')

    @rate.setter
    def rate(self, value: dmm.Rate) -> None:
        self.write(f'RATE {self.RATES[value]}')

    @property
    def val1(self) -> float:
        return float(self.query('VAL1?'))

    @property
    def trigger_source(self) -> str:
        return self.query('TRIGGER?')

    @trigger_source.setter
    def trigger_source(self, value: dmm.TriggerSource) -> None:
        self.write(f'TRIGGER {self.TRIGGER_TYPES[value]}')
        self._trigger_source = value

    @property
    def trigger_measurement(self) -> bool:
        return self._trigger_source == 2 or self._trigger_source == 3

    def remote(self) -> None:
        pass

    def return_to_local(self) -> None:
        pass

    def read_val(self) -> float:
        return float(self.query('VAL?'))

    def write(self, cmd: str) -> None:
        super().write(cmd)
        self.read()     # Returns '=>' if successful

    def query(self, cmd: str) -> str:
        val = super().query(cmd)
        self.read()     # Returns '=>' if successful
        return val


if __name__ == '__main__':
    fluke45 = Fluke45('ASRL11::INSTR', timeout=5000)
    fluke45.setup('VOLT:AC', 'slow', '100mA', 'bus')
    print(f'Measurement: {fluke45.measure()}')
