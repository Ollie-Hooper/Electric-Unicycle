import matplotlib.pyplot as plt
import numpy as np

from numpy import degrees, radians

from unicycle.controllers import PID, Exponential, Polynomial
from unicycle.model import Unicycle
from unicycle.plotting import run_animation, plot_chart
from unicycle.solver import solve


def main():
    y0 = np.array([radians(15), 0, 0.2]) # inital [theta, dtheta, dx]
    fps = 30
    length = 20
    t = np.linspace(0, length, length*1001)
    h = t[1] - t[0]

    pid = PID()
    e = Exponential()
    p = Polynomial()

    unicycle = Unicycle(h, p)

    y, M, F = solve(unicycle.model, y0, t)
    x = (h * y[:, 2]).cumsum()

    plot_chart("Seatpost angle", degrees(y[:, 0]), t, 'phi (degrees)', 'time (s)')
    plot_chart("Velocity of unicycle", y[:, 2], t, 'v (m/s)', 'time (s)')
    plot_chart("Controller torque", M, t, 'tau (Nm)', 'time (s)')
    plot_chart("Random pertubations", F, t, 'force (N)', 'time (s)')

    run_animation(y, x, unicycle, fps, length)


if __name__ == "__main__":
    main()
