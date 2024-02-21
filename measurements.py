import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from dac import DAC
from visa_instrument import Fluke45


def sweep_dac_volt(dmm_resource, dac_port, dac_channel, sweep_volt,
                   dmm_rate="S", dmm_range=3):
    readings = list()
    dmm = Fluke45(dmm_resource)
    dmm.setup("VDC", dmm_rate, dmm_range)
    dac = DAC(dac_port)
    time.sleep(1)       # Make sure all channels are ready
    for volt in sweep_volt:
        dac.set_volt(dac_channel, volt)
        readings.append(dmm.read_val())
    dac.close()
    return readings


if __name__ == "__main__":
    sweep = range(0, 8000, 1)
    t0 = time.time()
    dac_volt = sweep_dac_volt('ASRL7::INSTR', 'COM5', 4, sweep)
    print("Measurement finished in " + str(time.time() - t0) + "s")

    with open('dac_ch4.csv', 'w') as file:
        wr = csv.writer(file)
        wr.writerows([np.array(sweep) / 1000, dac_volt])
