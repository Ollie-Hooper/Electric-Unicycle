import numpy as np

from numpy import sin, cos, arccos, arctan, pi, sign, sqrt


class Unicycle:

    def __init__(self, timestep, controller, controller_sample_time=0.005, delay=0.005):
        self.timestep = timestep

        self.wheel_mass = 3
        self.seatpost_mass = 0.5
        self.wheel_radius = 0.2
        self.seatpost_length = 0.9
        self.seat_length = 0.2
        self.wheel_inertia = (1 / 2) * self.wheel_mass * (self.wheel_radius ** 2)
        self.seatpost_inertia = self.seatpost_mass * (self.seatpost_length ** 2)
        self.up = -0.08
        self.ux = 0.08
        self.g = -9.81

        self.controller = controller

        self.controller_sample_time = controller_sample_time
        self.delay = delay

        self.last_timestep = -1e10
        self.last_output = 0
        self.delayed_p = RingBuffer(int(self.delay / self.timestep))

        self.rand_force = 0
        self.rand_force_t = 0.1
        self.std_force = 0.5
        self.last_rand_force_t = -1e10

    def model(self, y, t):
        m1 = self.wheel_mass
        m2 = self.seatpost_mass
        R = self.wheel_radius
        L = self.seatpost_length
        S = self.seat_length
        I1 = self.wheel_inertia
        I2 = self.seatpost_inertia
        up = self.up
        ux = self.ux
        g = self.g

        if t - self.last_rand_force_t > self.rand_force_t:
            F = np.random.normal(0, self.std_force)
            self.rand_force = F
            self.last_rand_force_t = t
        else:
            F = self.rand_force

        p_max = pi - (arccos(R / sqrt(L ** 2 + (S / 2) ** 2)) + arctan((S / 2) / L))

        p = y[0]
        dp = y[1]
        dx = y[2]

        delayed_p = self.delayed_p(p)

        if t - self.last_timestep > self.controller_sample_time:
            M = self.controller(delayed_p)  # -R * ux * 2.2 * 2 # -1.3983
            self.last_output = M
            self.last_timestep = t
        else:
            M = self.last_output

        d2p = ((m1 * (R ** 2) + I1 + m2 * (R ** 2)) * (
                up * dp - m2 * g * L * sin(p) - m2 * dx * dp * L * sin(p))
               + m2 * M * R * L * cos(p) - m2 * (ux) * dx * (R ** 2) * L * cos(p)) / (
                      (m1 * (R ** 2) + I1 + m2 * (R ** 2)) * (m2 * (L ** 2) + I2)
                      + (m2 ** 2) * (R ** 2) * (L ** 2) * (cos(p) ** 2))

        d2p += F / m2

        d2x = ((-M * R - ux * dx * (R ** 2)) / (m1 * (R ** 2) + I1 + m2 * (R ** 2)))
        - (m2 * (R ** 2) * L * cos(p)) * ((up * dp - m2 * g * L * sin(p) - m2 * dx * dp * L * sin(p))
                                          / ((m1 * (R ** 2) + I1 + m2 * (R ** 2)) * (m2 * (L ** 2) + I2) - (m2 ** 2) * (
                        R ** 2) * (L ** 2) * (cos(p) ** 2))
                                          + (m2 * M * R * L * cos(p) - m2 * (ux) * dx * (R ** 2) * L * cos(p))
                                          / (((m1 * (R ** 2) + I1 + m2 * (R ** 2)) ** 2) * (m2 * (L ** 2) + I2) - (
                        m1 * (R ** 2) + I1 + m2 * (R ** 2)) * ((m2 ** 2) * (R ** 2) * (L ** 2) * (cos(p) ** 2))))

        # Constant speed - ignore d2x calculation
        d2x = 0

        c = 0.2

        if abs(p) <= p_max:
            dydt = [dp, d2p, d2x]
        else:
            dydt = [-sign(p) * (1 / self.timestep) * (abs(p) - p_max), -(1 / self.timestep) * dp * (1 + c), d2x]

        return dydt, M, F


class RingBuffer:

    def __init__(self, delay):
        self.a = [0 for i in range(delay)]
        self.delay = delay

    def __call__(self, *args, **kwargs):
        self.a.append(args[0])
        return self.a.pop(0)
