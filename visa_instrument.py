import pyvisa

FUNCTIONS = {'AAC': 'CURR:AC', 'CURR:AC': 'CURR:AC', 'ADC': 'CURR:DC',
             'CURR:DC': 'CURR:DC', 'CONT': 'CONT', 'DIODE': 'DIOD',
             'DIOD': 'DIOD', 'FREQ': 'FREQ', 'OHMS': 'RES', 'RES': 'RES',
             'VAC': 'VOLT:AC', 'VOLT:AC': 'VOLT:AC', 'VDC': 'VOLT:DC',
             'VOLT:DC': 'VOLT:DC'}


class Instrument:
    """Generic VISA instrument."""

    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n'):
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
        # Reset; clear status register; enable OPC; enable std event
        print(self._resource.query('*RST;*CLS;*ESE 1;*SRE 32;*IDN?'))

    def write(self, cmd: str):
        """Write command to instrument.

        Writes the specified command and waits for the instrument to
        complete the execution by reading the OPC status register. Don't
        write query commands with this method.

        Args:
            cmd (str): Command to write
        """
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
        return self._resource.query(cmd)

    def close(self):
        """Close resource.

        Closes the PyVISA resource. Wrapper method for
        `pyvisa.resources.Resource.close()`
        """
        self._resource.close()


class FLUKE45(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n'):
        """FLUKE 45 constructor.

        Initialize the resources need to remotely control the instrument
        with VISA and setup the instrument for external trigger with
        settling delay. To list available devices, use
        `list_resources()` from `pyvisa.highlevel.ResourceManager`.

        Args:
            resource_name (str): Address of resource to initialize.
            query_delay (float): Delay between write and read in query
                commands.
            timeout (float): Time before read commands abort.
            write_termination (str): Input terminator for write
                commands.
            read_termination (str): Output terminator for read commands.
        """
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination)
        self.write('TRIG 3')    # External trigger with settling delay.

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

    def setup(self, func: str, meas_rate: str, meas_range: str):
        """Setup the instrument.

        Args:
            func (str): DMM function. See the FLUKE 45 manual for a list
                of available functions.
            meas_rate (str): Measurement rate (`'S'`, `'M'`, or `'F'`).
                Determines the integration time of the ADC.
            meas_range (str): Measurement range. Se the FLUKE 45 manual
                for a list of available ranges.
        """
        self.write(func)
        print('=== FLUKE 45: ' + func + ' MEASUREMENT ===')
        if func not in ('CONT', 'DIODE'):
            self.write('RANGE ' + meas_range)
            print('RANGE:  ' + self.query('RANGE1?'))
            self.write('RATE ' + meas_rate)
            print('RATE:   ' + self.query('RATE?'))

    def measure(self):
        """Trigger and read a measurement.

        Triggers the instrument for a measurement and queries the
        measured value.

        Returns:
            str: The value on the primary display.
        """
        return self.query('*TRG;VAL1?')


class HP34401A(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n'):
        """HP/Agilent 34401A constructor.

        Initialize the resources need to remotely control the instrument
        with VISA and setup the instrument for remote operation with
        internal trigger. To list available devices, use
        `list_resources()` from `pyvisa.highlevel.ResourceManager`.

        Args:
            resource_name (str): Address of resource to initialize.
            query_delay (float): Delay between write and read in query
                commands.
            timeout (float): Time before read commands abort.
            write_termination (str): Input terminator for write
                commands.
            read_termination (str): Output terminator for read commands.
        """

        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination)
        self.write('SYST:REM')          # Remote operation
        self.write('TRIG:SOUR IMM')     # Internal trigger

    def setup(self, func: str, meas_rate: str = '10', meas_range: str = 'MAX'):
        """Setup the instrument.

        Args:
            func (str): DMM function. See the 34401A user guide for a
                list of available functions.
            meas_rate (str): Integration time in number of power line
                cycles (0.02, 0.2, 1, 10, or 100).
            meas_range (str): Measurement range. Se the 34401A user
                guide for a list of available ranges.
        """
        self.write('FUNC "' + FUNCTIONS[func] + '"')
        print('=== HP34401A: ' + FUNCTIONS[func] + ' MEASUREMENT ===')
        if FUNCTIONS[func] not in ('CONT', 'DIOD'):
            self.write(FUNCTIONS[func] + ':NPLC ' + meas_rate)
            print('RATE:   ' + self.query(FUNCTIONS[func] + ':NPLC?'))
            self.write(FUNCTIONS[func] + ':RANG ' + meas_range)
            print('RANGE:  ' + self.query(FUNCTIONS[func] + ':RANG?'))

    def measure(self):
        """Trigger and read a measurement.

        Triggers the instrument for a measurement and queries the
        measured value.

        Returns:
            str: The measured value.
        """
        return self.query('READ?')


if __name__ == '__main__':
    hp = HP34401A('ASRL6::INSTR', timeout=5000)
    hp.setup('VDC', '10', '10')


