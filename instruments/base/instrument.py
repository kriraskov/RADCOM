import pyvisa
from .pyvisa_base import PyVisaBase


class Instrument(PyVisaBase):
    """Base class for instruments."""
    def __init__(self, resource_name: str = None, query_delay: float = 0.,
                 timeout: int = 2000, write_termination: str = None,
                 read_termination: str = None, echo: bool = False):
        """Instrument constructor.

        Initialize the resources needed to remotely control an
        instrument over VISA. To list available devices, use `list_resources()`
        from `pyvisa.highlevel.ResourceManager`.

        Example:
            >>> import pyvisa
            >>> rm = pyvisa.ResourceManager()
            >>> rm.list_resources()
            ('ASRL5::INSTR', 'ASRL7::INSTR')
            >>> inst = Instrument('ASRL7::INSTR')

        Args:
            resource_name (str): Address of resource to initialize.
        """
        super().__init__(None, echo)
        self.open_resource(resource_name, query_delay, timeout,
                           write_termination, read_termination)
        print(self.identity)

    @property
    def complete(self):
        return self.query('*OPC?')

    @property
    def status(self):
        return self.query('*STB?')

    @property
    def options(self):
        return self.query('*OPT?')

    @property
    def identity(self):
        return self.query('*IDN?')

    @property
    def event_status_enable(self):
        return self.query('*ESE?')

    @event_status_enable.setter
    def event_status_enable(self, value: int):
        self.write(f'*ESE {value}')

    @property
    def service_request_enable(self):
        return self.query('*SRE?')

    @service_request_enable.setter
    def service_request_enable(self, value: int):
        self.write(f'*SRE {value}')
        
    def write(self, cmd: str):
        """Write command to instrument and await complete execution.

        Args:
            cmd (str): Command to write.
        """
        super().write(cmd)
        while not self.complete:
            pass

    def trigger(self):
        self.write('*TRG')

    def clear(self):
        self.write('*CLS')

    def reset(self):
        self.write('*RST')

    def event_status_enable_select(
            self, operation_complete: bool = False, query_error: bool = False,
            device_specific_error: bool = False, execution_error: bool = False,
            command_error: bool = False, power_on: bool = False):
        self.event_status_enable = (power_on << 7) | (command_error << 5) \
            | (execution_error << 4) | (device_specific_error << 3) \
            | (query_error << 2) | operation_complete

    def service_request_enable_select(
            self, error_queue: bool = False,
            questionable_data_summary: bool = False,
            message_available: bool = False,
            standard_event_summary: bool = False, master_summary: bool = False,
            standard_operation_summary: bool = False):
        self.service_request_enable = (standard_operation_summary << 7) \
            | (master_summary << 6) | (standard_event_summary << 5) \
            | (message_available << 4) | (questionable_data_summary << 3) \
            | (error_queue << 2)
            

class Channel(PyVisaBase):
    def __init__(self, number: int, resource: pyvisa.Resource,
                 echo: bool = False):
        super().__init__(resource, echo)
        self.number = number
        
    def write(self, cmd: str):
        super().write(cmd)
        while not self.complete:
            pass

    @property
    def complete(self):
        return self.query('*OPC?')
        