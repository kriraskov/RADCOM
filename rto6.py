from visa_instrument import Instrument


class RTO6(Instrument, Measurement):
    def __init__(self, resource_name: str, query_delay: float = 0.,
                 timeout: float = 0., write_termination: str = '\n',
                 read_termination: str = '\n', echo: bool = False):
        super().__init__(resource_name, query_delay, timeout,
                         write_termination, read_termination, echo)
        self._resource.write('*RST;*CLS;*ESE 1;*SRE 32')
        self._resource.write('CHAN1:STAT OFF')
        
    def setup(self, channel, h_scale=None, h_range=None, v_scale=None,
              v_range=None, samp_rate=None, resolution=None, rec_length=None, 
              trig_lvl=None, v_pos=0.0, h_pos=0.0, h_ref=50.,
              echo=True):
        self.echo = echo
        self.write(f'CHAN{channel}:STAT ON')
        
        if h_scale and not h_range:
            self.write(f'TIM:SCAL {h_scale}')
        elif h_range and not h_scale:
            self.write(f'TIM:RANG {h_range}')
        elif h_scale and h_range:
            raise ValueError('Incorrect horizontal range specification.')
            
        if v_scale and not v_range:
            self.write(f'CHAN{channel}:SCAL {v_scale}')
        elif v_range and not v_scale:
            self.write(f'CHAN{channel}:RANG {v_range}')
        elif v_scale and v_range:
            raise ValueError('Incorrect vertical range specification.')
        
        if samp_rate and not resolution:
            self.write('ACQ:POIN:AUTO RES')
            self.write(f'ACQ:SRAT {samp_rate}')
        elif resolution and not samp_rate:
            self.write('ACQ:POIN:AUTO RES')
            self.write(f'ACQ:RES {resolution}')
        elif samp_rate and resolution:
            raise ValueError('Incorrect resolution.')
            
        if rec_length:
            self.write('ACQ:POIN:AUTO RECL')
            self.write(f'ACQ:POIN {rec_length}')
            
        if trig_lvl:
            self.write(f'TRIG1:SOUR CHAN{channel}')
            self.write(f'TRIG1:LEV{channel} {trig_lvl}')
            
        self.write(f'TIM:HOR:POS {h_pos}')
        self.write(f'TIM:REF {h_ref}')
        self.write(f'CHAN{channel}:POS {v_pos}')
        
    def math(self, num, expr, v_range=None, v_scale=None, echo=False):
        self.echo = echo
        self.write(f"CALC:MATH{num} '{expr}'")
        self.write(f'CALC:MATH{num}:STAT ON')
        
        if v_scale and not v_range:
            self.write(f'CALC:MATH{num}:VERT:SCAL {v_scale}')
        elif v_range and not v_scale:
            self.write(f'CALC:MATH{num}:VERT:RANG {v_range}')
        elif v_scale and v_range:
            raise ValueError('Incorrect vertical range specification.')
            
    def zoom(self, diagram='Diagram1', name='Zoom1', x_start=None, x_stop=None,
             x_cent=None, x_span=None, y_start=None, y_stop=None, y_cent=None,
             y_span=None, ref_ch=1):
        if (x_start is not None or x_stop is not None) \
            and (x_cent is not None or x_span is not None):
            # Specify EITHER start and stop OR center and span.
            raise ValueError('Incorrect vertical-zoom specification.')
            
        if x_cent is not None and x_span is not None:
            # Convert to start and stop. Required to create new zoom.
            x_start = x_cent - x_span / 2
            x_stop = x_cent + x_span / 2
        elif x_start is None or x_stop is None:
            # No information given. Use current settings.
            x_cent = float(self.query('TIM:HOR:POS?'))
            x_span = float(self.query('TIM:RANG?'))
            x_start = x_cent - x_span / 2
            x_stop = x_cent + x_span / 2
        
        if (y_start is not None or y_stop is not None) \
            and (y_cent is not None or y_span is not None):
            # Specify EITHER start and stop OR center and span.
            raise ValueError('Incorrect vertical-zoom specification.')
            
        if y_cent is not None and y_span is not None:
            # Convert to start and stop. Required to create new zoom.
            y_start = y_cent - y_span / 2
            y_stop = y_cent + y_span / 2
        elif (y_start is None or y_stop is None):
            # No information given. Use current settings.
            y_cent = float(self.query(f'CHAN{ref_ch}:POS?'))
            y_span = float(self.query(f'CHAN{ref_ch}:RANG?'))
            y_start = y_cent - y_span / 2
            y_stop = y_cent + y_span / 2
            
        self.write(f"LAY:ZOOM:ADD '{diagram}', VERT, OFF, {x_start}, "
                   f"{x_stop}, {y_start}, {y_stop}, '{name}'")
        
    def measure(self, src1, src2=None, count=1e3, category='AMPT',
                param='AMPL', stat=None):
        self.write('MEAS1 ON')                         # New measurement group
        self.write(f'MEAS1:SOUR {src1}')               # Measurement source
        
        if src2:
            self.write(f'MEAS1:SSRC {src2}')           # Second source
            
        self.write(f'MEAS:CAT {category}')
        self.write(f'MEAS:MAIN {param}')               # What to measure
        
        if stat:
            self.write('MEAS1:STAT ON')                # Statistics
            val = self.query(f'MEAS1:RES:{stat}?')
        else:
            val = self.query('MEAS1?')                 # Measure actual value

        return val
    

if __name__ == '__main__':
    rto6 = RTO6('TCPIP0::192.168.96.40::inst0::INSTR', timeout=5000)

    try:
        rto6.setup(1, v_scale=5e-3, h_scale=10e-6, samp_rate=10e9,
                   rec_length=1e6)
        rto6.setup(3, v_scale=100e-3, trig_lvl=200e-3)
        rto6.math(1, 'FIR(userdef,Ch1,"C:\\Users\\Instrument\\Desktop\\fir_bpf_100MHz\\fir_bpf_100MHz_bw_300kHz_10GSaps_100001taps.csv")',
                  v_scale=50e-6, echo=True)
        rto6.zoom(x_cent=0, x_span=100e-9, y_cent=0, y_span=500e-6)
        print('Phase: ' + rto6.measure('C3W1', 'M1', param='PHAS', stat='AVG'))
        rto6.close()
    except:
        rto6.close()
