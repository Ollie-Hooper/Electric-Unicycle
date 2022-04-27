import matplotlib.pyplot as plt
import numpy as np

from numpy import degrees, radians

from unicycle.controllers import PID, Linear, Exponential, Polynomial
from unicycle.model import Unicycle
from unicycle.plotting import run_animation, plot_chart
from unicycle.solver import solve


def main():
    y0 = np.array([radians(5), 0, 1])  # inital [theta, dtheta, dx]
    fps = 60
    length = 30
    t = np.linspace(0, length, length * 1001)
    h = t[1] - t[0]

    pid = PID()
    l = Linear()
    e = Exponential()
    p = Polynomial()

    controller = l

    unicycle = Unicycle(h, controller)

    y, M, F = solve(unicycle.model, y0, t)
    x = (h * y[:, 2]).cumsum()

    plot_chart(f"Seatpost angle - {controller.name} controller", degrees(y[:, 0]), t, 'phi (degrees)', 'time (s)')
    plot_chart(f"Velocity of unicycle - {controller.name} controller", y[:, 2], t, 'v (m/s)', 'time (s)')
    plot_chart(f"{controller.name} controller torque", M, t, 'tau (Nm)', 'time (s)')
    plot_chart("Random pertubations", F, t, 'force (N)', 'time (s)')

    run_animation(y, x, unicycle, fps, length)


if __name__ == "__main__":
    main()
