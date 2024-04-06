from .instrument import Instrument, Channel
from abc import ABC, abstractmethod


class Oscilloscope(ABC, Instrument):
    """Base class for oscilloscopes."""
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self.reset()
        self.clear()
        self.remote()

    @property
    @abstractmethod
    def horizontal_scale(self):
        ...

    @horizontal_scale.setter
    @abstractmethod
    def horizontal_scale(self, value: float):
        ...

    @property
    @abstractmethod
    def horizontal_range(self):
        ...

    @horizontal_range.setter
    @abstractmethod
    def horizontal_range(self, value: float):
        ...

    @property
    @abstractmethod
    def horizontal_position(self):
        ...

    @horizontal_position.setter
    @abstractmethod
    def horizontal_position(self, value: float):
        ...

    @property
    @abstractmethod
    def horizontal_reference(self):
        ...

    @horizontal_reference.setter
    @abstractmethod
    def horizontal_reference(self, value: float):
        ...

    @property
    @abstractmethod
    def sample_rate(self):
        ...

    @sample_rate.setter
    @abstractmethod
    def sample_rate(self, value: float):
        ...

    @property
    @abstractmethod
    def resolution(self):
        ...

    @resolution.setter
    @abstractmethod
    def resolution(self, value: float):
        ...

    @property
    @abstractmethod
    def record_length(self):
        ...

    @record_length.setter
    @abstractmethod
    def record_length(self, value: float):
        ...

    @property
    @abstractmethod
    def trigger_source(self):
        ...

    @trigger_source.setter
    @abstractmethod
    def trigger_source(self, value: str):
        ...

    @property
    @abstractmethod
    def trigger_level(self):
        ...

    @trigger_level.setter
    @abstractmethod
    def trigger_level(self, value: float):
        ...
        
    @property
    @abstractmethod
    def trigger_coupling(self):
        ...
        
    @trigger_coupling.setter
    @abstractmethod
    def trigger_coupling(self, value: str):
        ...

    @abstractmethod
    def remote(self):
        ...

    @abstractmethod
    def return_to_local(self):
        ...

    def timebase(self, sample_rate: float = None, resolution: float = None,
                 record_length: float = None, h_scale: float = None,
                 h_range: float = None, h_ref: float = None,
                 h_pos: float = None):
        if h_scale is not None and h_range is None:
            self.horizontal_scale = h_scale
        elif h_range is not None and h_scale is None:
            self.horizontal_range = h_range
        elif h_scale is not None and h_range is not None:
            raise ValueError('Incorrect scale/range specification.')
        
        if sample_rate is not None and resolution is None:
            self.sample_rate = sample_rate
        elif resolution is not None and sample_rate is None:
            self.resolution = resolution
        elif sample_rate is not None and resolution is not None:
            raise ValueError('Incorrect rate/resolution specification.')

        if record_length is not None:
            self.record_length = record_length

        if h_ref is not None:
            self.horizontal_reference = h_ref

        if h_pos is not None:
            self.horizontal_position = h_pos

    def trigger_config(self, source: str, level: float, coupling: str):
        self.trigger_source = source
        self.trigger_level = level
        self.trigger_coupling = coupling


class InputChannel(ABC, Channel):
    @property
    @abstractmethod
    def enable(self):
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...

    @property
    @abstractmethod
    def vertical_scale(self):
        ...

    @vertical_scale.setter
    @abstractmethod
    def vertical_scale(self, value: float):
        ...

    @property
    @abstractmethod
    def vertical_range(self):
        ...

    @vertical_range.setter
    @abstractmethod
    def vertical_range(self, value: float):
        ...

    @property
    @abstractmethod
    def vertical_position(self):
        ...

    @vertical_position.setter
    @abstractmethod
    def vertical_position(self, value: float):
        ...
    
    @property
    @abstractmethod
    def coupling(self):
        ...
    
    @coupling.setter
    @abstractmethod
    def coupling(self, value: str):
        ...

    def setup(self, v_scale: float = None, v_range: float = None,
              v_pos: float = None, coupling: str = None):
        self.enable = True

        if v_scale is not None and v_range is None:
            self.vertical_scale = v_scale
        elif v_range is not None and v_scale is None:
            self.vertical_range = v_range
        elif v_scale is not None and v_range is not None:
            raise ValueError('Incorrect scale/range specification.')

        if v_pos is not None:
            self.vertical_position = v_pos
            
        if coupling is not None:
            self.coupling = coupling


class Math(ABC, Channel):
    @property
    @abstractmethod
    def enable(self):
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...

    @property
    @abstractmethod
    def expression(self):
        ...

    @expression.setter
    @abstractmethod
    def expression(self, value: str):
        ...

    @property
    @abstractmethod
    def vertical_scale(self):
        ...

    @vertical_scale.setter
    @abstractmethod
    def vertical_scale(self, value: float):
        ...

    @property
    @abstractmethod
    def vertical_range(self):
        ...

    @vertical_range.setter
    @abstractmethod
    def vertical_range(self, value: float):
        ...

    def setup(self, expr: str, v_range: float = None, v_scale: float = None):
        self.enable = True
        self.expression = expr

        if v_scale is not None and v_range is None:
            self.vertical_scale = v_scale
        elif v_range is not None and v_scale is None:
            self.vertical_range = v_range
        elif v_scale is not None and v_range is not None:
            raise ValueError('Incorrect scale/range specification.')


class Measurement(ABC, Channel):
    @property
    @abstractmethod
    def enable(self):
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...

    @property
    @abstractmethod
    def source1(self):
        ...

    @source1.setter
    @abstractmethod
    def source1(self, value: str):
        ...

    @property
    @abstractmethod
    def source2(self):
        ...

    @source2.setter
    @abstractmethod
    def source2(self, value: str):
        ...
        
    @property
    @abstractmethod
    def category(self):
        ...
        
    @category.setter
    @abstractmethod
    def category(self, value: str):
        ...
        
    @property
    @abstractmethod
    def main(self):
        ...
    
    @main.setter
    @abstractmethod
    def main(self, value: str):
        ...
        
    @property
    @abstractmethod
    def statistics(self):
        """Enable statistics."""
        ...
    
    @statistics.setter
    @abstractmethod
    def statistics(self, value: bool):
        ...
 
    @abstractmethod
    def read_val(self, parameter: str = None, statistics: str = None):
        ...
        
    @abstractmethod
    def add_parameter(self, parameter: str = None):
        ...
        
    def setup(self, main: str, source1: str, source2: str = None,
              category: str = None, statistics: bool = False):
        self.enable = True
        
        if category:
            self.category = category

        self.main = main
        self.source1 = source1
        
        if source2:
            self.source2 = source2
            
        if statistics:
            self.statistics = True