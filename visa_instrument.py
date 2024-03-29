import pyvisa


class Instrument:
    """Generic VISA instrument.

    Params:
        echo (bool): Print write and query commands to terminal.
    """

    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False):
        """Instrument constructor.

        Initialize the resources need to remotely control an instrument
        with VISA. To list available devices, use `list_resources()`
        from `pyvisa.highlevel.ResourceManager`.

        Example:
            >>> import pyvisa
            >>> rm = pyvisa.ResourceManager()
            >>> rm.list_resources()
            ('ASRL5::INSTR', 'ASRL7::INSTR')
            >>> inst = Instrument('ASRL7::INSTR')

        Args:
            resource_name (str): Address of resource to initialize.
            query_delay (float): Delay between write and read in query
                commands.
            timeout (float): Time before read commands abort.
            write_termination (str): Input terminator for write
                commands.
            read_termination (str): Output terminator for read commands.
        """
        self._rm = pyvisa.ResourceManager()
        self._resource = self._rm.open_resource(resource_name)
        self._resource.read_termination = read_termination
        self._resource.write_termination = write_termination
        self._resource.query_delay = query_delay
        self._resource.timeout = timeout
        self.echo = echo
        print(self._resource.query('*IDN?'))

    def write(self, cmd: str):
        """Write command to instrument.

        Writes the specified command and waits for the instrument to
        complete the execution by reading the OPC status register. Don't
        write query commands with this method.

        Args:
            cmd (str): Command to write
        """
        # The instrument executes every command completely before
        # continuing to the next.
        self.query(cmd + ';*OPC?')

    def read(self):
        """Read output from instrument.

        Reads the output buffer and returns the value. Wrapper
        method for `pyvisa.resources.Resource.read()`.

        Returns:
            str: The value in the output buffer.
        """
        return self._resource.read()

    def query(self, cmd: str):
        """Query command.

        Writes the specified command to the instrument, reads
        the output buffer, and returns the value. Wrapper
        method for `pyvisa.resources.Resource.query()`.

        Args:
            cmd (str): Command to write

        Returns:
            str: The value in the output buffer.
        """
        if self.echo:
            print(cmd)
        return self._resource.query(cmd)

    def close(self):
        """Close resource.

        Closes the PyVISA resource. Wrapper method for
        `pyvisa.resources.Resource.close()`
        """
        self._resource.close()
        