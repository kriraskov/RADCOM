from visa_instrument import Instrument


FUNCTIONS = {'AAC': 'CURR:AC', 'CURR:AC': 'CURR:AC', 'ADC': 'CURR:DC',
             'CURR:DC': 'CURR:DC', 'CONT': 'CONT', 'DIODE': 'DIOD',
             'DIOD': 'DIOD', 'FREQ': 'FREQ', 'OHMS': 'RES', 'RES': 'RES',
             'VAC': 'VOLT:AC', 'VOLT:AC': 'VOLT:AC', 'VDC': 'VOLT:DC',
             'VOLT:DC': 'VOLT:DC'}


class HP34401A(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False):
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
                         write_termination, read_termination, echo)
        # Reset; clear status register; enable OPC; enable std event
        self._resource.write('*RST;*CLS;*ESE 1;*SRE 32')
        self.write('SYST:REM')  # Remote operation
        self.write('TRIG:SOUR IMM')  # Internal trigger

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