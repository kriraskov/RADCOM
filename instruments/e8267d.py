from .base.signal_generator import SignalGenerator, OutputChannel


class E8267D(SignalGenerator):
    """Agilent A8267D vector signal generator."""
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 0, write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self.__dict__['OUT'] = E8267DOutput(1, self.resource, echo)


class E8267DOutput(OutputChannel):
    """Agilent A8267D output channel."""
    @property
    def enable(self) -> bool:
        return self.query('OUTPUT:STAT?') == 'ON'

    @enable.setter
    def enable(self, value: bool) -> None:
        self.write(f'OUTPUT:STAT {"ON" if value else "OFF"}')

    @property
    def frequency(self) -> float:
        return float(self.query('SOUR:FREQ:CW?'))

    @frequency.setter
    def frequency(self, value: float) -> None:
        self.write(f'SOUR:FREQ:CW {value}')

    @property
    def power(self) -> float:
        return float(self.query('SOUR:POW:LEV:IMM:AMPL?'))

    @power.setter
    def power(self, value: float) -> None:
        self.write(f'SOUR:POW:LEV:IMM:AMPL {value}')
