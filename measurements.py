import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from dac import DAC
from visa_instrument import HP34401A


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


if __name__ == "__main__":
    sweep = range(0, 10, 1)
    t0 = time.time()
    dac_volt = sweep_dac_volt('ASRL6::INSTR', 'COM3', 6, sweep)
    print("Measurement finished in " + str(time.time() - t0) + "s")

    with open('dac_ch1_hp34401a.csv', 'w') as file:
        wr = csv.writer(file)
        wr.writerows([np.array(sweep) / 1000, dac_volt])
