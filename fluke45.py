from visa_instrument import Instrument


class FLUKE45(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False):
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
                         write_termination, read_termination, echo)
        # Reset; clear status register; enable OPC; enable std event
        self._resource.write('*RST;*CLS;*ESE 1;*SRE 32')
        self.write('TRIG 3')  # External trigger with settling delay.

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