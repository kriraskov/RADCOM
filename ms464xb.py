from visa_instrument import Instrument

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
        self.write('LANG NATIVE')

    def close(self):
        """Close resource.

        Closes the PyVISA resource and return the instrument to local
        control. Wrapper method for `pyvisa.resources.Resource.close()`.
        """
        print('RTL')
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
        self.echo = echo
        self.write(f':SENS{channel}:SWE:TYP ' + f_sweep_type)
        if (f_center and f_span) and not (f_start or f_stop):
            self.write(f':SENS{channel}:FREQ:CENT {f_center}')
            self.write(f':SENS{channel}:FREQ:SPAN {f_span}')
        elif (f_start and f_stop) and not (f_center or f_span):
            self.write(f':SENS{channel}:FREQ:STAR {f_start}')
            self.write(f':SENS{channel}:FREQ:STOP {f_stop}')
        elif f_cw and not (f_center or f_span or f_start or f_stop):
            self.write(f':SENS{channel}:FREQ:CW {f_cw}')
        else:
            raise ValueError('Incorrect sweep specification.')
        self.write(f':SENS{channel}:SWE:POIN {n_points}')
        self.write(f':SOUR{channel}:POW:PORT{port} {power}')
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
        self.echo = echo
        self.write(f'SENS{channel}:SWE:TYP:POW')
        self.write(f'SENS{channel}:FREQ:CW {f_cw}')
        self.write(f':SOUR{channel}:POW:PORT{port}:LIN:POW:STAR {start}')
        self.write(f':SOUR{channel}:POW:PORT{port}:LIN:POW:STOP {stop}')
        self.write(f':SOUR{channel}:POW:PORT{port}:LIN:POW:POIN {n_points}')

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
        self.echo = echo
        self.write(f':CALC{channel}:PAR{trace}:DEF {param}')
        self.write(f':CALC{channel}:PAR{trace}:MARK{marker_no}:ACT')
        self.write(f':CALC{channel}:FORM LOGPH')
        self.write(f':CALC{channel}:PAR{trace}:MARK{marker_no}:X {x}')
        self.write('TRS;WFS')
        return self.query(f':CALC{channel}:PAR{trace}:MARK{marker_no}:Y?')

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
        self.write(f'TRS;WFS;SAVE "{filename}"')