class BMS:
    def __init__(self):
        self.version = "unknown"
        self.status = 0
        self.soc = 0
        self.current = 0
        self.cycle = 0
        self.temps = [0] * 4
        self.voltage = 0
        self.cellVoltages = [0] * 10
