import pyvisa
from .base import oscilloscope as osc
from typing import Literal


Sources = Literal['C1', 'C2', 'C3', 'C4', 'EXT']

HorizontalScaleMode = Literal['RES', 'RECL']

Coupling = Literal['DC', 'DCL', 'AC']


class RTO6(osc.Oscilloscope):
    """Rohde & Schwarz RTO6 oscilloscope.

    Parameters:
        C1...C4 (RTO6Channel): Channels 1-4 of the oscilloscope.
        M1...M8 (RTO6Math): Math channels 1-8 of the oscilloscope.
        MG1...MG10 (RTO6MeasurementGroup): Measurement groups 1-10 of
            the oscilloscope.
    """
    SOURCES = {'C1': 'CHAN1', 'C2': 'CHAN2', 'C3': 'CHAN3', 'C4': 'CHAN4',
               'EXT': 'EXT'}

    NUM_SOURCES = {'CHAN1': 1, 'CHAN2': 2, 'CHAN3': 3, 'CHAN4': 4, 'EXT': 5}

    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 0, write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False) -> None:
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        for i in range(1, 5):
            self.__dict__[f'C{i}'] = RTO6Channel(i, self.resource, echo)

        for i in range(1, 9):
            self.__dict__[f'M{i}'] = RTO6Math(i, self.resource, echo)
            
        for i in range(1, 11):
            self.__dict__[f'MG{i}'] = RTO6Measurement(i, self.resource, echo)

    @property
    def horizontal_scale(self) -> float:
        return float(self.query('TIM:SCAL?'))

    @horizontal_scale.setter
    def horizontal_scale(self, value: float) -> None:
        self.write(f'TIM:SCAL {value}')

    @property
    def horizontal_range(self) -> float:
        return float(self.query('TIM:RANG?'))

    @horizontal_range.setter
    def horizontal_range(self, value: float) -> None:
        self.write(f'TIM:RANG {value}')

    @property
    def horizontal_position(self) -> float:
        return float(self.query('TIM:HOR:POS?'))

    @horizontal_position.setter
    def horizontal_position(self, value: float) -> None:
        self.write(f'TIM:HOR:POS {value}')

    @property
    def horizontal_reference(self) -> float:
        return float(self.query('TIM:HOR:POS?'))

    @horizontal_reference.setter
    def horizontal_reference(self, value: float) -> None:
        self.write(f'TIM:REF {value}')

    @property
    def sample_rate(self) -> float:
        return float(self.query('ACQ:SRAT?'))

    @sample_rate.setter
    def sample_rate(self, value: float) -> None:
        self.write(f'ACQ:SRAT {value}')

    @property
    def resolution(self) -> float:
        return float(self.query('ACQ:RES?'))

    @resolution.setter
    def resolution(self, value: float) -> None:
        self.write(f'ACQ:RES {value}')

    @property
    def record_length(self) -> float:
        return float(self.query('ACQ:POIN?'))

    @record_length.setter
    def record_length(self, value: float) -> None:
        self.write(f'ACQ:POIN {value}')

    @property
    def trigger_source(self) -> str:
        return self.query('TRIG1:SOUR?')

    @trigger_source.setter
    def trigger_source(self, value: Sources) -> None:
        self.write(f'TRIG1:SOUR {self.SOURCES[value]}')

    @property
    def trigger_level(self) -> float:
        return float(self.query(
            f'TRIG1:LEV{self.NUM_SOURCES[self.trigger_source]}?'))

    @trigger_level.setter
    def trigger_level(self, value: float) -> None:
        self.write(f'TRIG1:LEV{self.NUM_SOURCES[self.trigger_source]} {value}')
        
    @property
    def trigger_coupling(self) -> str:
        return self.query('TRIG1:ANED:COUP?')
        
    @trigger_coupling.setter
    def trigger_coupling(self, value: Coupling) -> None:
        self.write(f'TRIG1:ANED:COUP {value}')
    
    @property
    def horizontal_scale_mode(self) -> str:
        return self.query('ACQ:POIN:AUTO?')

    @horizontal_scale_mode.setter
    def horizontal_scale_mode(self, value: HorizontalScaleMode) -> None:
        self.write(f'ACQ:POIN:AUTO {value}')

    def remote(self) -> None:
        pass

    def return_to_local(self) -> None:
        pass

    def zoom(self, x_start=None, x_stop=None, y_start=None, y_stop=None,
             diagram='Diagram1', name='Zoom1') -> None:
        """Add a zoom window."""
        self.write(f"LAY:ZOOM:ADD '{diagram}', VERT, OFF, {x_start}, "
                   f"{x_stop}, {y_start}, {y_stop}, '{name}'")


class RTO6Channel(osc.InputChannel):
    def __init__(self, number: int, resource: pyvisa.Resource,
                 echo: bool = False, sync: bool = False) -> None:
        super().__init__(number, resource, echo)
        if number == 1:
            self.enable = False  # Don't want Ch1 to be enabled at reset

    @property
    def enable(self) -> bool:
        return self.query(f'CHAN{self.number}:STAT?') == 'ON'

    @enable.setter
    def enable(self, value: bool) -> None:
        self.write(f'CHAN{self.number}:STAT {"ON" if value else "OFF"}')

    @property
    def vertical_scale(self) -> float:
        return float(self.query(f'CHAN{self.number}:SCAL?'))

    @vertical_scale.setter
    def vertical_scale(self, value: float) -> None:
        self.write(f'CHAN{self.number}:SCAL {value}')

    @property
    def vertical_range(self) -> float:
        return float(self.query(f'CHAN{self.number}:RANG?'))

    @vertical_range.setter
    def vertical_range(self, value: float) -> None:
        self.write(f'CHAN{self.number}:RANG {value}')

    @property
    def vertical_position(self) -> float:
        return float(self.query(f'CHAN{self.number}:POS?'))

    @vertical_position.setter
    def vertical_position(self, value: float) -> None:
        self.write(f'CHAN{self.number}:POS {value}')
        
    @property
    def coupling(self) -> str:
        return self.query(f'CHAN{self.number}:COUP?')
    
    @coupling.setter
    def coupling(self, value: Coupling) -> None:
        self.write(f'CHAN{self.number}:COUP {value}')


class RTO6Math(osc.Math):
    @property
    def enable(self) -> bool:
        return self.query(f'CALC:MATH{self.number}:STAT?') == 'ON'

    @enable.setter
    def enable(self, value: bool) -> None:
        self.write(f'CALC:MATH{self.number}:STAT {"ON" if value else "OFF"}')

    @property
    def expression(self) -> str:
        return self.query(f'CALC:MATH{self.number}?')

    @expression.setter
    def expression(self, value: str) -> None:
        self.write(f"CALC:MATH{self.number} '{value}'")

    @property
    def vertical_scale(self) -> float:
        return float(self.query(f'CALC:MATH{self.number}:VERT:SCAL?'))

    @vertical_scale.setter
    def vertical_scale(self, value: float) -> None:
        self.write(f'CALC:MATH{self.number}:VERT:SCAL {value}')

    @property
    def vertical_range(self) -> float:
        return float(self.query(f'CALC:MATH{self.number}:VERT:RANG?'))

    @vertical_range.setter
    def vertical_range(self, value: float) -> None:
        self.write(f'CALC:MATH{self.number}:VERT:RANG {value}')


class RTO6Measurement(osc.Measurement):
    SOURCES = {'C1': 'C1W1', 'C2': 'C2W1', 'C3': 'C3W1', 'C4': 'C4W1',
               'M1': 'M1', 'M2': 'M2', 'M3': 'M3', 'M4': 'M4', 'M5': 'M5',
               'M6': 'M6', 'M7': 'M7', 'M8': 'M8'}

    @property
    def enable(self) -> bool:
        return self.query(f'MEAS{self.number}?') == 'ON'

    @enable.setter
    def enable(self, value: bool) -> None:
        self.write(f'MEAS{self.number} {"ON" if value else "OFF"}')

    @property
    def source1(self) -> str:
        return self.query(f'MEAS{self.number}:FSRC?')

    @source1.setter
    def source1(self, value: Sources) -> None:
        self.write(f'MEAS{self.number}:FSRC {self.SOURCES[value]}')

    @property
    def source2(self) -> str:
        return self.query(f'MEAS{self.number}:SSRC?')

    @source2.setter
    def source2(self, value: Sources) -> None:
        self.write(f'MEAS{self.number}:SSRC {self.SOURCES[value]}')
        
    @property
    def category(self) -> str:
        return self.query(f'MEAS{self.number}:CAT?')
        
    @category.setter
    def category(self, value: str) -> None:
        self.write(f'MEAS:CAT {value}')
        
    @property
    def main(self) -> str:
        return self.query(f'MEAS{self.number}:MAIN?')
    
    @main.setter
    def main(self, value: str) -> None:
        self.write(f'MEAS:MAIN {value}')
    
    @property
    def statistics(self) -> bool:
        return self.query(f'MEAS{self.number}:STAT?') == 'ON'
    
    @statistics.setter
    def statistics(self, value: bool) -> None:
        self.write(f'MEAS{self.number}:STAT {"ON" if value else "OFF"}')
        
    def add_parameter(self, parameter: str = None) -> None:
        self.write(f'MEAS{self.number}:ADD {parameter}, ON')

    def read_val(self, parameter: str = None, stats: str = None) -> float:
        stats = stats if stats is not None else 'ACT'
        return float(self.query(f'MEAS{self.number}:RES:{stats}? {parameter}'))

    def reset_statistics(self) -> None:
        """Reset the statistics of the measurement group."""
        self.write(f'MEAS{self.number}:STAT:RES')
