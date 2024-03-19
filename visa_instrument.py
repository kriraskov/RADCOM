import pyvisa

FUNCTIONS = {'AAC': 'CURR:AC', 'CURR:AC': 'CURR:AC', 'ADC': 'CURR:DC',
             'CURR:DC': 'CURR:DC', 'CONT': 'CONT', 'DIODE': 'DIOD',
             'DIOD': 'DIOD', 'FREQ': 'FREQ', 'OHMS': 'RES', 'RES': 'RES',
             'VAC': 'VOLT:AC', 'VOLT:AC': 'VOLT:AC', 'VDC': 'VOLT:DC',
             'VOLT:DC': 'VOLT:DC'}


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
        if self.echo:
            print(cmd)
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
        print(self._resource.query('*RST;*CLS;*ESE 1;*SRE 32;*IDN?'))
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
        print(self._resource.query('*RST;*CLS;*ESE 1;*SRE 32;*IDN?'))
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


class N6700B(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\r\n', echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        print(self._resource.query('*IDN?'))

    def set_volt(self, volt: float, channel: int):
        self.write('VOLT ' + str(volt) + ',(@' + str(channel) + ')')

    def set_current(self, current: float, channel: int):
        self.write('CURR ' + str(current) + ',(@' + str(channel) + ')')

    def enable_output(self, channel: int):
        self.write('OUTP ON,(@' + str(channel) + ')')

    def disable_output(self, channel: int):
        self.write('OUTP OFF,(@' + str(channel) + ')')


class MS464xB(Instrument):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False):
        """MS464xB constructor.

        Initialize the resources need to remotely control the MS464xB
        network analyzer with VISA. To list available devices, use
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
        print(self._resource.query('*IDN?'))
        self.write('LANG NATIVE')

    def close(self):
        """Close resource.

        Closes the PyVISA resource and return the instrument to local
        control. Wrapper method for `pyvisa.resources.Resource.close()`.
        """
        self._resource.write('RTL')
        self._resource.close()

    def freq_setup(self, n_points: int, power: float, f_center: float = None,
                   f_span: float = None, f_start: float = None,
                   f_stop: float = None, f_cw: float = None,
                   f_sweep_type: str = 'LIN', channel: int = 1, port: int = 1,
                   echo: bool = True):
        """Setup a frequency sweep on a port.

        Configure the frequency sweep and port power levels. Specify
        frequency range either as (`f_center`, `f_span`) OR as
        (`f_start`, `f_stop`). Alternatively, configure the CW mode by
        setting `f_cw`.

        Args:
            n_points: Number of measurement points for frequency sweep.
            power: Port power.
            f_center: Center frequency. Use together with `f_span`.
            f_span: Sweep span. Use together with `f_center`.
            f_start: Start frequency. Use together with `f_stop`.
            f_stop: Stop frequency. Use together with `f_start`.
            f_cw: CW frequency.
            f_sweep_type: Frequency sweep type (`LIN` or `LOG`).
            channel: Channel to configure.
            port: Port to configure.
            echo: Echo commands.
        """
        sense = ':SENS' + str(channel)
        sourc = ':SOUR' + str(channel) + ':POW:PORT' + str(port) + ' '
        self.echo = echo
        self.write(sense + ':SWE:TYP ' + f_sweep_type)
        if (f_center and f_span) and not (f_start or f_stop):
            self.write(sense + ':FREQ:CENT ' + str(f_center))
            self.write(sense + ':FREQ:SPAN ' + str(f_span))
        elif (f_start and f_stop) and not (f_center or f_span):
            self.write(sense + ':FREQ:STAR ' + str(f_start))
            self.write(sense + ':FREQ:STOP ' + str(f_stop))
        elif f_cw and not (f_center or f_span or f_start or f_stop):
            self.write(sense + ':FREQ:CW ' + str(f_cw))
        else:
            raise ValueError('Incorrect sweep specification.')
        self.write(sense + ':SWE:POIN ' + str(n_points))
        self.write(sourc + str(power))
        self.write(':FORM:SNP:FREQ HZ')  # Set unit of s2p file to Hz
        self.write(':FORM:SNP:PAR LOGPH')  # Log-Phase format of s2p file

    def power_setup(self, f_cw: float, n_points: int, start: float,
                    stop: float, channel: int = 1, port: int = 1,
                    echo: bool = True):
        """Setup a power sweep on a port.

        Args:
            f_cw: CW frequency.
            n_points: Number of measurement points.
            start: Start power.
            stop: Stop power.
            channel: Channel to configure.
            port: Port to configure.
            echo: Echo commands.
        """
        sourc = ':SOUR' + str(channel) + ':POW:PORT' + str(port)
        sense = ':SENS' + str(channel)
        self.echo = echo
        self.write(sense + ':SWE:TYP:POW')
        self.write(sense + ':FREQ:CW ' + str(f_cw))
        self.write(sourc + ':LIN:POW:STAR ' + str(start))
        self.write(sourc + ':LIN:POW:STOP ' + str(stop))
        self.write(sourc + ':LIN:POW:POIN ' + str(n_points))

    def measure(self, x: int, param: str = 'S11', marker_no: int = 1,
                channel: int = 1, trace: int = 1, echo: bool = False):
        """Measure a parameter.

        Measure the specified parameter at a measurement point.

        Args:
            x: x-coordinate for measurement.
            param: Parameter to measure.
            marker_no: Marker number.
            channel: Channel to read.
            trace: Trace to read.
            echo: Echo commands.

        Returns: Measured value at the specified x-coordinate.
        """
        calc = ':CALC' + str(channel)
        par = ':PAR' + str(trace)
        self.echo = echo
        self.write(calc + par + ':DEF ' + param)
        self.write(calc + par + ':MARK' + str(marker_no) + ':ACT')
        self.write(calc + ':FORM LOGPH')
        self.write(calc + par + ':MARK' + str(marker_no) + ':X ' + str(x))
        self.write('TRS;WFS')
        return self.query(calc + par + ':MARK' + str(marker_no) + ':Y?')

    def save_sweep(self, filename: str, echo: bool = False):
        """Perform and save a sweep.

        Initiates a sweep and waits until the sweep is finished before
        saving the sweep locally on the instrument.

        Args:
            filename: Full path name of the saved file.
            echo: Echo commands.
        """
        # Lightning 37xxxx commands - refer to PM Supplement and 37xxxx PM
        # Trigger sweep, wait full sweep, save to path
        self.echo = echo
        self.write('TRS;WFS;SAVE "' + filename + '"')


if __name__ == '__main__':
    ms4644b = MS464xB('TCPIP0::192.168.96.47::inst0::INSTR', timeout=5000)

    try:
        # ms4644b.setup(n_points=301, f_start=8E9, f_stop=13E9, f_sweep_type='LIN')
        # ms4644b.save_sweep('C:\\Users\\VectorStarUser\\Desktop\\RadCom_Exjobb\\QORVO_CMD297P34\\test1.s2p')
        # ms4644b.measure(11.25e9)
        ms4644b.close()
    except:
        ms4644b.close()
