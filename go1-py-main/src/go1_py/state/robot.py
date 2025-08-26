class Version:
    def __init__(self):
        self.hardware = "--"
        self.software = "--"


class SN:
    def __init__(self):
        self.product = "--"
        self.id = "--"


class DistanceWarning:
    def __init__(self):
        self.front = 0
        self.back = 0
        self.left = 0
        self.right = 0


class Robot:
    def __init__(self):
        self.version = Version()
        self.sn = SN()
        self.temps = [0] * 20
        self.mode = 0
        self.gaitType = 0
        self.obstacles = [255] * 4
        self.state = "invalid"
        self.distanceWarning = DistanceWarning()
