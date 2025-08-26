import numpy as np

from go1_py.state import BMS


def parse(payload):
    bms = BMS()
    bms.version = f"{payload[0]}.{payload[1]}"
    bms.status = payload[2]
    bms.soc = payload[3]
    bms.current = np.frombuffer(payload[4:8].tobytes(), dtype=np.int32)[0]
    bms.cycle = np.frombuffer(payload[8:10].tobytes(), dtype=np.uint16)[0]
    bms.temps = payload[10:14]
    bms.cellVoltages = np.frombuffer(payload[14:34].tobytes(), dtype=np.uint16)
    bms.voltage = bms.cellVoltages.sum()
    return bms
