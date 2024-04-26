import pyvisa
from .pyvisa_base import PyVisaBase


class Instrument(PyVisaBase):
    """Base class for instruments."""
    def __init__(self, resource_name: str = None, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False,
                 name: str = None) -> None:
        """Instrument constructor.

        Initialize the resources needed to remotely control an
        instrument over VISA and print the instruments identity string.

        Args:
            resource_name (str): Name of resource to initialize.
            query_delay (float): Time in seconds between write and read.
            timeout (float): Time in milliseconds before interrupt of
                unanswered reads.
            write_termination (str): Termination character of written
                commands.
            read_termination (str): Termination character of read
                strings.
            echo (bool): Echo commands.
            name (str): Name to show when printing commands.
        """
        super().__init__(None, echo, name)
        self.open_resource(resource_name, query_delay, timeout,
                           write_termination, read_termination)
        print(self.identity)

    @property
    def status(self) -> str:
        """Value of the status-byte register."""
        return self.query('*STB?')

    @property
    def options(self) -> str:
        """Available options."""
        return self.query('*OPT?')

    @property
    def identity(self) -> str:
        """The instruments identity string."""
        return self.query('*IDN?')

    @property
    def event_status_enable(self) -> str:
        """Value of the event-status-enable register."""
        return self.query('*ESE?')

    @event_status_enable.setter
    def event_status_enable(self, value: int) -> None:
        self.write(f'*ESE {value}')

    @property
    def service_request_enable(self) -> str:
        """Value of the service-request-enable register."""
        return self.query('*SRE?')

    @service_request_enable.setter
    def service_request_enable(self, value: int) -> None:
        self.write(f'*SRE {value}')
        
    def write(self, cmd: str) -> None:
        """Write command to instrument and await execution."""
        super().write(cmd)
        super().write('*WAI')

    def trigger(self) -> None:
        """Trigger the instrument for a measurement."""
        self.write('*TRG')

    def clear(self) -> None:
        """Clear the status register and error queue."""
        self.write('*CLS')

    def reset(self) -> None:
        """Reset the instrument."""
        self.write('*RST')

    def event_status_enable_select(
            self, operation_complete: bool = False, query_error: bool = False,
            device_specific_error: bool = False, execution_error: bool = False,
            command_error: bool = False, power_on: bool = False) -> None:
        """Select bits of the event-status-enable register."""
        self.event_status_enable = (power_on << 7) | (command_error << 5) \
            | (execution_error << 4) | (device_specific_error << 3) \
            | (query_error << 2) | operation_complete

    def service_request_enable_select(
            self, error_queue: bool = False,
            questionable_data_summary: bool = False,
            message_available: bool = False,
            standard_event_summary: bool = False, master_summary: bool = False,
            standard_operation_summary: bool = False) -> None:
        """Select bits of the service-request-enable register."""
        self.service_request_enable = (standard_operation_summary << 7) \
            | (master_summary << 6) | (standard_event_summary << 5) \
            | (message_available << 4) | (questionable_data_summary << 3) \
            | (error_queue << 2)
            

class Channel(PyVisaBase):
    """A unit within an instrument.

    Use this class to define subsystems within an instrument, such as
    channels, ports, math channels, etc. Add such objects to the
    instruments `__dict__`.

    Args:
        number (int): Channel number.
        resource (pyvisa.resources.Resource): Reference to the
            instruments Resource object.
        echo (bool): Echo commands.
    """
    def __init__(self, number: int, resource: pyvisa.resources.Resource,
                 echo: bool = False, name: str = None):
        super().__init__(resource, echo, name)
        self.number = number
        
    def write(self, cmd: str) -> None:
        """Write command to instrument and await execution."""
        super().write(cmd)
        super().write('*WAI')
