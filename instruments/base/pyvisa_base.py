import pyvisa


class PyVisaBase:
    """Base class for PyVisa operation.
    
    Wraps the PyVisa API to provide an abstraction of its interface.
    This class represents a PyVisa resource and the properties needed to
    communicate with it. If no resource is provided at instantiation,
    open a new resource with `open_resource()`. List available
    resources with `list_resources()`.

    Attributes:
        resource (pyvisa.Resource): Reference to the PyVisa resource
            object that handles a specific resource.
        echo (bool): Echo commands when written to the instrument.
    """
    def __init__(self, resource: pyvisa.resources.Resource = None,
                 echo: bool = False):
        self.resource = resource
        self.echo = echo

    @property
    def read_termination(self) -> str:
        """Termination character of read strings."""
        return self.resource.read_termination

    @read_termination.setter
    def read_termination(self, value: str) -> None:
        self.resource.read_termination = value

    @property
    def write_termination(self) -> str:
        """Termination character of written commands."""
        return self.resource.write_termination

    @write_termination.setter
    def write_termination(self, value: str) -> None:
        self.resource.write_termination = value

    @property
    def query_delay(self) -> float:
        """Delay in seconds between write and read."""
        return self.resource.query_delay

    @query_delay.setter
    def query_delay(self, value: float) -> None:
        self.resource.query_delay = value

    @property
    def timeout(self) -> int:
        """Time in milliseconds before interrupt of unanswered reads."""
        return self.resource.timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        self.resource.timeout = value
        
    def open_resource(self, resource_name: str, query_delay: float,
                      timeout: int, read_termination: str,
                      write_termination: str) -> None:
        """Open a resource by name and set its attributes.

        Args:
            resource_name (str): Name of the resource to open.
            query_delay (float): Delay in seconds between write and
                read.
            timeout (float): Time in milliseconds before interrupt of
                unanswered reads.
            read_termination (str): Termination character of read
                strings.
            write_termination (str): Termination character of written
                commands.
        """
        rm = pyvisa.ResourceManager()
        self.resource = rm.open_resource(resource_name)
        self.read_termination = read_termination
        self.write_termination = write_termination
        self.query_delay = query_delay
        self.timeout = timeout

    def write(self, cmd: str) -> None:
        """Write a command to the instrument."""
        if self.echo:
            print(f'{self.__class__.__name__}: {cmd}')
        self.resource.write(cmd)

    def read(self) -> str:
        """Read the output buffer of and instrument."""
        return self.resource.read()

    def query(self, cmd: str) -> str:
        """Consecutive write and read of a query command."""
        if self.echo:
            print(f'{self.__class__.__name__}: {cmd}')
        return self.resource.query(cmd)

    def close(self) -> None:
        """Close the PyVisa resource."""
        self.resource.close()

    @staticmethod
    def list_resources(self) -> None:
        """List available resources."""
        rm = pyvisa.ResourceManager()
        rm.list_resources()

