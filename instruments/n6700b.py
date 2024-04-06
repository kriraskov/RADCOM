from .base.power_supply import PowerSupply, OutputChannel
from typing import Literal


PriorityMode = Literal['VOLT', 'CURR']


class N6700B(PowerSupply):
    """Agilent N6700B power supply.

    Parameters:
        C1...C4 (N6700BChannel): Output channels 1-4.
    """
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        for i in range(1, 4):
            self.__dict__[f'C{i}'] = N6700BChannel(i, self.resource, echo)
            
    def remote(self) -> None:
        pass

    def return_to_local(self) -> None:
        pass


class N6700BChannel(OutputChannel):
    """An N6700B output channel."""
    @property
    def enable(self) -> bool:
        return self.query(f'OUTP? (@{self.number})') == 'ON'
        
    @enable.setter
    def enable(self, value: bool) -> None:
        self.write(f'OUTP {"ON" if value else "OFF"},(@{self.number})')
        
    @property
    def voltage(self) -> float:
        return float(self.query(f'VOLT? (@{self.number})'))
        
    @voltage.setter
    def voltage(self, value: float) -> None:
        self.write(f'VOLT {value},(@{self.number})')
    
    @property
    def current(self) -> float:
        return float(self.query(f'CURR? (@{self.number})'))
        
    @current.setter
    def current(self, value: float) -> None:
        self.write(f'CURR {value},(@{self.number})')
        
    @property
    def positive_voltage_limit(self) -> float:
        """Maximum allowed positive voltage."""
        return float(self.query(f'VOLT:LIM? (@{self.number})'))
        
    @positive_voltage_limit.setter
    def positive_voltage_limit(self, value: float) -> None:
        self.write(f'VOLT:LIM {value},(@{self.number})')
        
    @property
    def negative_voltage_limit(self) -> float:
        """Maximum allowed negative voltage."""
        return float(self.query(f'VOLT:LIM:NEG? (@{self.number})'))
        
    @negative_voltage_limit.setter
    def negative_voltage_limit(self, value: float) -> None:
        self.write(f'VOLT:LIM:NEG {value},(@{self.number})')
        
    @property
    def positive_current_limit(self) -> float:
        """Maximum allowed positive current."""
        return float(self.query(f'CURR:LIM? (@{self.number})'))
        
    @positive_current_limit.setter
    def positive_current_limit(self, value: float) -> None:
        self.write(f'CURR:LIM {value},(@{self.number})')
        
    @property
    def negative_current_limit(self) -> float:
        """Maximum allowed negative current."""
        return float(self.query(f'CURR:LIM:NEG? (@{self.number})'))
        
    @negative_current_limit.setter
    def negative_current_limit(self, value: float) -> None:
        self.write(f'CURR:LIM:NEG {value},(@{self.number})')
        
    @property
    def priority_mode(self) -> float:
        """Voltage priority or current priority."""
        return float(self.query(f'FUNC? (@{self.number})'))
        
    @priority_mode.setter
    def priority_mode(self, value: PriorityMode) -> None:
        self.write(f'FUNC value,(@{self.number})')

    @property
    def voltage_reading(self) -> float:
        """Voltage reading of the channel."""
        return float(self.query(f'MEAS:VOLT? (@{self.number})'))
    
    @property
    def current_reading(self) -> float:
        """Current reading of the channel."""
        return float(self.query(f'MEAS:CURR? (@{self.number})'))
