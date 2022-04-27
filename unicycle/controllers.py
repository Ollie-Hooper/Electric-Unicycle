from numpy import sign
from simple_pid import PID as _PID


class PID:
    def __init__(self):
        self.name = 'PID'
        self.pid = _PID(10, 2, 0.3, setpoint=0)  # pid = PID(Kp, Ki, Kd, setpoint=0)
        self.pid.output_limits = (-50, 50)
        self.setpoint = 0

    def __call__(self, *args, **kwargs):
        return self.pid(args[0])

    def update_setpoint(self, x):
        self.setpoint = x
        self.pid.setpoint = self.setpoint


class Linear:
    def __init__(self, coeff=-20, max_torque=50):
        self.name = 'Linear'
        self.coeff = coeff
        self.limit = max_torque
        self.setpoint = 0

    def __call__(self, *args, **kwargs):
        x = args[0] - self.setpoint
        o = self.coeff*x
        return min(o, sign(o) * self.limit, key=abs)

    def update_setpoint(self, x):
        self.setpoint = x


class Exponential:
    def __init__(self, k=-10, n=2, max_torque=50):
        self.name = 'Exponential'
        self.k = k
        self.n = n
        self.limit = max_torque
        self.setpoint = 0

    def __call__(self, *args, **kwargs):
        x = args[0] - self.setpoint
        o = self.k * self.n ** x
        return min(o, sign(o) * self.limit, key=abs)

    def update_setpoint(self, x):
        self.setpoint = x


class Polynomial:
    def __init__(self, coeff=(-15, 0, -10), max_torque=50):
        self.name = 'Polynomial'
        self.coeff = coeff
        self.limit = max_torque
        self.setpoint = 0

    def __call__(self, *args, **kwargs):
        x = args[0] - self.setpoint
        o = 0
        for n, c in enumerate(self.coeff):
            o += c * x ** (n + 1)
        return min(o, sign(o) * self.limit, key=abs)

    def update_setpoint(self, x):
        self.setpoint = x
