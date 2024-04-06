from .base.power_supply import PowerSupply, OutputChannel
from typing import Literal


PriorityMode = Literal['VOLT', 'CURR']


class N6700B(PowerSupply):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        for i in range(1, 4):
            self.__dict__[f'C{i}'] = N6700BChannel(i, self.resource, echo)
            
    def remote(self):
        pass


class N6700BChannel(OutputChannel):
    @property
    def enable(self):
        return self.query(f'OUTP? (@{self.number})') == 'ON'
        
    @enable.setter
    def enable(self, value: bool):
        self.write(f'OUTP {"ON" if value else "OFF"},(@{self.number})')
        
    @property
    def voltage(self):
        return float(self.query(f'VOLT? (@{self.number})'))
        
    @voltage.setter
    def voltage(self, value: float):
        self.write(f'VOLT {value},(@{self.number})')
    
    @property
    def current(self):
        return float(self.query(f'CURR? (@{self.number})'))
        
    @current.setter
    def current(self, value: float):
        self.write(f'CURR {value},(@{self.number})')
        
    @property
    def positive_voltage_limit(self):
        return float(self.query(f'VOLT:LIM? (@{self.number})'))
        
    @positive_voltage_limit.setter
    def positive_voltage_limit(self, value: float):
        self.write(f'VOLT:LIM {value},(@{self.number})')
        
    @property
    def negative_voltage_limit(self):
        return float(self.query(f'VOLT:LIM:NEG? (@{self.number})'))
        
    @negative_voltage_limit.setter
    def negative_voltage_limit(self, value: float):
        self.write(f'VOLT:LIM:NEG {value},(@{self.number})')
        
    @property
    def positive_current_limit(self):
        return float(self.query(f'CURR:LIM? (@{self.number})'))
        
    @positive_current_limit.setter
    def positive_current_limit(self, value: float):
        self.write(f'CURR:LIM {value},(@{self.number})')
        
    @property
    def negative_current_limit(self):
        return float(self.query(f'CURR:LIM:NEG? (@{self.number})'))
        
    @negative_current_limit.setter
    def negative_current_limit(self, value: float):
        self.write(f'CURR:LIM:NEG {value},(@{self.number})')
        
    @property
    def priority_mode(self):
        return float(self.query(f'FUNC? (@{self.number})'))
        
    @priority_mode.setter
    def priority_mode(self, value: PriorityMode):
        self.write(f'FUNC value,(@{self.number})')

    @property
    def voltage_reading(self):
        return float(self.query(f'MEAS:VOLT? (@{self.number})'))
    
    @property
    def current_reading(self):
        return float(self.query(f'MEAS:CURR? (@{self.number})'))