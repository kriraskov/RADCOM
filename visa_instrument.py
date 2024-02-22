import pyvisa


class Instrument:
    """Generic VISA instrument."""
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\n'):
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
        print(self._resource.query("*RST;*CLS;*IDN?"))

    def write(self, cmd: str):
        """Write command to instrument.

        Writes the specified command and waits for the
        instrument to complete the execution by reading the
        OPC status register.

        Args:
            cmd (str): Command to write
        """
        self.query(cmd + ";*OPC?")

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
        return self._resource.query(cmd)

    def close(self):
        """Close resource.

        Closes the PyVISA resource. Wrapper method for
        `pyvisa.resources.Resource.close()`
        """
        self._resource.close()
        

class Fluke45(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.):
        """FLUKE 45 constructor.

        Args:
            resource_name (str): Address of resource to initialize.
            query_delay (float): Delay between write and read in query
                commands.
        """
        super().__init__(resource_name, query_delay, write_termination='\r\n',
                         read_termination='\r\n')
        self.write("TRIG 3")

    def query(self, cmd: str):
        """Query command.

        Writes the specified command to the instrument, reads
        the output buffer, and returns the value. Overrides
        `Instrument.query()` to read the output buffer two
        times before returning the value.

        Args:
            cmd (str): Command to write

        Returns:
            str: The value in the output buffer.
        """
        val = self._resource.query(cmd)
        self.read()
        return val

    def setup(self, units: str, rate: str, meas_range: int):
        """Setup the instrument.

        Args:
            units (str):
            rate (str):
            meas_range (int):
        """
        self.write(units)
        print("=== FLUKE 45: " + units + " MEASUREMENT ===")
        self.write("RANGE " + str(meas_range))
        print("RANGE:  " + self.query("RANGE1?"))
        self.write("RATE " + rate)
        print("RATE:   " + self.query("RATE?"))

    def measure(self):
        """Trigger and read a measurement.

        Triggers the instrument for a measurement and queries the
        measured value.

        Returns:
            str: The value on the primary display.
        """
        return self.query("*TRG;VAL1?")


class HP34401A(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0.):
        super().__init__(resource_name, query_delay, timeout)
        self._resource.write("SYST:REM")

    def setup(self, units: str, meas_range: int, resolution: str = "DEF"):
        self.write("CONF:" + units + " " + str(meas_range) + "," + resolution)
        print("=== HP34401A: " + units + " MEASUREMENT ===")
        print(self.query("CONF?"))

    def measure(self):
        return


if __name__ == "__main__":
    hp = HP34401A('ASRL7::INSTR', query_delay=2, timeout=10000)
