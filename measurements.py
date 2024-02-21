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
    dac.set_volt(dac_channel, 0)
    time.sleep(1)
    for volt in sweep_volt:
        dac.set_volt(dac_channel, volt)
        readings.append(dmm.read_val())
    dac.close()
    return readings


if __name__ == "__main__":
    sweep = range(0, 8000, 1)
    dac_volt = sweep_dac_volt('ASRL7::INSTR', 'COM5', 1, sweep)

    with open('dac_ch1_twisted.csv', 'w') as file:
        wr = csv.writer(file)
        wr.writerow(dac_volt)

    plt_data = np.genfromtxt("dac_ch1.csv", delimiter=',')
    plt.plot(np.array(sweep) / 1000, plt_data)
    plt.xlabel("Input Voltage")
    plt.ylabel("Output Voltage")
    plt.show()
