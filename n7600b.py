from visa_instrument import Instrument

class N6700B(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        print(self._resource.query('*IDN?'))

    def set_volt(self, volt: float, channel: int):
        self.write(f'VOLT {volt},(@{channel})')

    def set_current(self, current: float, channel: int):
        self.write(f'CURR {current},(@{channel})')

    def enable_output(self, channel: int):
        self.write(f'OUTP ON,(@{channel})')

    def disable_output(self, channel: int):
        self.write(f'OUTP OFF,(@{channel})')

