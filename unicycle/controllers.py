from numpy import sign
from simple_pid import PID as _PID


class PID:
    def __init__(self):
        self.pid = _PID(10, 0, 0, setpoint=0)
        self.pid.output_limits = (-50, 50)

    def __call__(self, *args, **kwargs):
        return self.pid(args[0])


class Exponential:
    def __init__(self, k=-10, n=2, max_torque=50):
        self.k = k
        self.n = n
        self.limit = max_torque

    def __call__(self, *args, **kwargs):
        x = args[0]
        o = self.k * self.n ** x
        return min(o, sign(o) * self.limit, key=abs)


class Polynomial:
    def __init__(self, coeff=(-10, 0, -10), max_torque=50):
        self.coeff = coeff
        self.limit = max_torque

    def __call__(self, *args, **kwargs):
        x = args[0]
        o = 0
        for n, c in enumerate(self.coeff):
            o += c * x ** (n+1)
        return min(o, sign(o) * self.limit, key=abs)
