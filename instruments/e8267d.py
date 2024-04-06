from .base.power_supply import PowerSupply, OutputChannel

class E8267D(PowerSupply):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self.__dict__['OUT'] = E8267DOutput(1, self.resource, echo)
        

class E8267DOutput(OutputChannel):
    @property
    def enable(self):
        return self.query('OUTPUT:STAT?')
    
    @enable.setter
    def enable(self, value: bool):
        self.write(f'OUTPUT:STAT {"ON" if value else "OFF"}')
    
    @property
    def frequency(self):
        return self.query('SOUR:FREQ:CW?')
    
    @frequency.setter
    def frequency(self, value: float):
        self.write(f'SOUR:FREQ:CW {value}')
    
    @property
    def power(self):
        return self.query('SOUR:POW:LEV:IMM:AMPL?')
    
    @power.setter
    def power(self, value: float):
        self.write(f'SOUR:POW:LEV:IMM:AMPL {value}')
        