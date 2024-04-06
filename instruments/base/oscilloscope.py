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
        """Scale of the horizontal axis in seconds per div."""
        ...

    @horizontal_scale.setter
    @abstractmethod
    def horizontal_scale(self, value: float):
        ...

    @property
    @abstractmethod
    def horizontal_range(self):
        """Range of the horizontal axis in seconds."""
        ...

    @horizontal_range.setter
    @abstractmethod
    def horizontal_range(self, value: float):
        ...

    @property
    @abstractmethod
    def horizontal_position(self):
        """Offset in seconds of the trigger point."""
        ...

    @horizontal_position.setter
    @abstractmethod
    def horizontal_position(self, value: float):
        ...

    @property
    @abstractmethod
    def horizontal_reference(self):
        """Relative position of the horizontal rescaling point."""
        ...

    @horizontal_reference.setter
    @abstractmethod
    def horizontal_reference(self, value: float):
        ...

    @property
    @abstractmethod
    def sample_rate(self):
        """Sampling rate of the oscilloscope."""
        ...

    @sample_rate.setter
    @abstractmethod
    def sample_rate(self, value: float):
        ...

    @property
    @abstractmethod
    def resolution(self):
        """Resolution of the oscilloscope."""
        ...

    @resolution.setter
    @abstractmethod
    def resolution(self, value: float):
        ...

    @property
    @abstractmethod
    def record_length(self):
        """Number of samples recorded in each acquisition."""
        ...

    @record_length.setter
    @abstractmethod
    def record_length(self, value: float):
        ...

    @property
    @abstractmethod
    def trigger_source(self):
        """Trigger source of the oscilloscope."""
        ...

    @trigger_source.setter
    @abstractmethod
    def trigger_source(self, value: str):
        ...

    @property
    @abstractmethod
    def trigger_level(self):
        """Trigger level of the selected source."""
        ...

    @trigger_level.setter
    @abstractmethod
    def trigger_level(self, value: float):
        ...
        
    @property
    @abstractmethod
    def trigger_coupling(self):
        """Coupling of the external trigger."""
        ...
        
    @trigger_coupling.setter
    @abstractmethod
    def trigger_coupling(self, value: str):
        ...

    @abstractmethod
    def remote(self):
        """Configure the oscilloscope for remote operation."""
        ...

    @abstractmethod
    def return_to_local(self):
        """Configure the oscilloscope for local operation."""
        ...

    def timebase(self, sample_rate: float = None, resolution: float = None,
                 record_length: float = None, h_scale: float = None,
                 h_range: float = None, h_ref: float = None,
                 h_pos: float = None):
        """Configure the timebase options of acquistions."""
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
        """Configure the trigger source."""
        self.trigger_source = source
        self.trigger_level = level
        self.trigger_coupling = coupling


class InputChannel(ABC, Channel):
    """An individual oscilloscope channel."""
    @property
    @abstractmethod
    def enable(self) -> bool:
        """Enable the channel."""
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool) -> None:
        ...

    @property
    @abstractmethod
    def vertical_scale(self):
        """Scale of the vertical axis in volt per div."""
        ...

    @vertical_scale.setter
    @abstractmethod
    def vertical_scale(self, value: float):
        ...

    @property
    @abstractmethod
    def vertical_range(self):
        """Range of the vertical axis in volt."""
        ...

    @vertical_range.setter
    @abstractmethod
    def vertical_range(self, value: float):
        ...

    @property
    @abstractmethod
    def vertical_position(self):
        """Vertical position of the waveform on the screen in divs."""
        ...

    @vertical_position.setter
    @abstractmethod
    def vertical_position(self, value: float):
        ...
    
    @property
    @abstractmethod
    def coupling(self):
        """Coupling of the channel"""
        ...
    
    @coupling.setter
    @abstractmethod
    def coupling(self, value: str):
        ...

    def setup(self, v_scale: float = None, v_range: float = None,
              v_pos: float = None, coupling: str = None):
        """Set up the oscilloscope channel."""
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
    """An oscilloscope math channel."""
    @property
    @abstractmethod
    def enable(self):
        """Enable the channel."""
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...

    @property
    @abstractmethod
    def expression(self):
        """Mathematical expression to calculate."""
        ...

    @expression.setter
    @abstractmethod
    def expression(self, value: str):
        ...

    @property
    @abstractmethod
    def vertical_scale(self):
        """Scale of the vertical axis in volt per div."""
        ...

    @vertical_scale.setter
    @abstractmethod
    def vertical_scale(self, value: float):
        ...

    @property
    @abstractmethod
    def vertical_range(self):
        """Range of the vertical axis in volt."""
        ...

    @vertical_range.setter
    @abstractmethod
    def vertical_range(self, value: float):
        ...

    def setup(self, expr: str, v_range: float = None, v_scale: float = None):
        """Set up the math channel"""
        self.enable = True
        self.expression = expr

        if v_scale is not None and v_range is None:
            self.vertical_scale = v_scale
        elif v_range is not None and v_scale is None:
            self.vertical_range = v_range
        elif v_scale is not None and v_range is not None:
            raise ValueError('Incorrect scale/range specification.')


class Measurement(ABC, Channel):
    """An oscilloscope measurement group."""
    @property
    @abstractmethod
    def enable(self):
        """Enable the measurement group."""
        ...

    @enable.setter
    @abstractmethod
    def enable(self, value: bool):
        ...

    @property
    @abstractmethod
    def source1(self):
        """Primary source of measurements."""
        ...

    @source1.setter
    @abstractmethod
    def source1(self, value: str):
        ...

    @property
    @abstractmethod
    def source2(self):
        """Secondary source for two-channel measurements."""
        ...

    @source2.setter
    @abstractmethod
    def source2(self, value: str):
        ...
        
    @property
    @abstractmethod
    def category(self):
        """Measurement category."""
        ...
        
    @category.setter
    @abstractmethod
    def category(self, value: str):
        ...
        
    @property
    @abstractmethod
    def main(self):
        """Primary measurement parameter."""
        ...
    
    @main.setter
    @abstractmethod
    def main(self, value: str):
        ...
        
    @property
    @abstractmethod
    def statistics(self):
        """Enable statistics for the measurement group."""
        ...
    
    @statistics.setter
    @abstractmethod
    def statistics(self, value: bool):
        ...
 
    @abstractmethod
    def read_val(self, parameter: str = None, statistics: str = None):
        """Read the value of the primary measurement parameter."""
        ...
        
    @abstractmethod
    def add_parameter(self, parameter: str = None):
        """Add a parameter to the measurement group."""
        ...
        
    def setup(self, main: str, source1: str, source2: str = None,
              category: str = None, statistics: bool = False):
        """Set up the measurement group."""
        self.enable = True
        
        if category:
            self.category = category

        self.main = main
        self.source1 = source1
        
        if source2:
            self.source2 = source2
            
        if statistics:
            self.statistics = True
