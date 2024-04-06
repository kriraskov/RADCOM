import pyvisa


class PyVisaBase:
    """Base class for PyVisa operation.
    
    Wrapps the PyVisa functionality to provide an abstraction of
    the interface. The class represents a PyVisa resource and the
    properties needed to communicate with it.
    """
    def __init__(self, resource: pyvisa.Resource = None,
                 echo: bool = False):
        """Base constructor.

        Args:
            resource (pyvisa.Resource): A PyVisa resource object. If no
                object is provided at instatiation, open a new resource
                with `open_resource()`.
            echo (bool): Echo commands when written to the instrument.
        """
        self.resource = resource
        self.echo = echo

    @property
    def read_termination(self):
        return self.resource.read_termination

    @read_termination.setter
    def read_termination(self, value: str):
        self.resource.read_termination = value

    @property
    def write_termination(self):
        return self.resource.write_termination

    @write_termination.setter
    def write_termination(self, value: str):
        self.resource.write_termination = value

    @property
    def query_delay(self):
        return self.resource.query_delay

    @query_delay.setter
    def query_delay(self, value: float):
        self.resource.query_delay = value

    @property
    def timeout(self):
        return self.resource.timeout

    @timeout.setter
    def timeout(self, value: int):
        self.resource.timeout = value
        
    def open_resource(self, resource_name: str, query_delay: float,
                      timeout: int, read_termination: str,
                      write_termination: str):
        self._rm = pyvisa.ResourceManager()
        self.resource = self._rm.open_resource(resource_name)
        self.read_termination = read_termination
        self.write_termination = write_termination
        self.query_delay = query_delay
        self.timeout = timeout

    def write(self, cmd: str):
        """Write command to instrument.

        Args:
            cmd (str): Command to write.
        """
        if self.echo:
            print(f'{self.__class__.__name__}: {cmd}')
        self.resource.write(cmd)

    def read(self):
        """Read the output buffer of and instrument.

        Returns:
            str: The value in the output buffer.
        """
        return self.resource.read()

    def query(self, cmd: str):
        """Consecutive write and read of an instrument query.

        Args:
            cmd (str): Command to write

        Returns:
            str: The value in the output buffer.
        """
        if self.echo:
            print(f'{self.__class__.__name__}: {cmd}')
        return self.resource.query(cmd)

    def close(self):
        """Close PyVisa resource."""
        self.resource.close()

