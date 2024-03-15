import time
from dac import DAC
from visa_instrument import HP34401A, MS464xB
import csv


def sweep_dac_volt(dmm_resource, dac_port, dac_channel, sweep_volt,
                   dmm_rate='10', dmm_range='10'):
    readings = list()
    dmm = HP34401A(dmm_resource, timeout=5000)
    dmm.setup('VDC', dmm_rate, dmm_range)
    dac = DAC(dac_port)
    time.sleep(1)       # Make sure all channels are ready
    for volt in sweep_volt:
        dac.set_volt(dac_channel, volt)
        readings.append(dmm.measure())
    dac.close()
    return readings


def ps_freq_sweep(ps_id, vna_resource, dac_port, dac_channel, sweep_volt,
                  n_points, f_start, f_stop, directory):
    vna = MS464xB(vna_resource, timeout=20000)
    vna.setup(n_points=n_points, f_start=f_start, f_stop=f_stop,
              f_sweep_type='LIN')
    dac = DAC(dac_port)
    dac.set_volt(dac_channel, 0)
    time.sleep(1) 
    # Setup for tracking progress
    N = len(sweep_volt)
    next_threshold = 0.01
    i = 0
    print("Starting measurement")
    for volt in sweep_volt:
        dac.set_volt(dac_channel, volt)
        # Example: CMD297P34_cartman_ch1_1mV_8e9-12e9Hz_301pts
        vna.save_sweep(directory + 'CMD297P34_' + ps_id + '_dac_ch' +
                       str(dac_channel) + '_' + str(volt) + 'mV_' +
                       str(f_start / 1e9) + '-' + str(f_stop / 1e9) + 'GHz_'
                       + str(n_points) + 'pts.s2p')
        # Print and update every 10% of completed measurements
        if i / N >= next_threshold:
            print(f"Progress: {round(i / N * 100, 1)}%")
            next_threshold += 0.01
        i += 1
    dac.close()
    vna.close()

    
def estimated_time(iterations, t_step=0.82):
    total_time = t_step * iterations
    if total_time < 60:
        return f"Estimated time: {total_time}"


if __name__ == "__main__":    
    sweep = range(0, 10000+100, 100)

    # Approx time it takes for one step (seconds)
    # 0.84s for 301 pts, 14s for 6401 pts
    t_step = 14
    
    # Print estimated (approx.) time depending on number of steps at
    # start of script
    print("Estimated time until completed: " + str(t_step * len(sweep) / 60)
          + " minute(s)")
    
    t0 = time.time()
    try:
        ps_freq_sweep('randy', 'TCPIP0::192.168.96.47::inst0::INSTR', 'COM7',
                      1, sweep, 6401, f_start=10.5e9, f_stop=12.5e9,
                      directory='C:\\Users\\VectorStarUser\\Desktop\\RadCom_Exjobb\\QORVO_CMD297P34\\')
    except Exception as e:
        print(e)
        ms4644b = MS464xB('TCPIP0::192.168.96.47::inst0::INSTR', timeout=5000)
        ms4644b.close()
    
    print("Measurement finished in " + str((time.time() - t0) / 60) + "min")
