import os, sys, subprocess

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from numpy import sin, cos, pi, floor, ceil

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def plot_chart(title, y, x, y_label, x_label):
    plt.plot(x, y)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.show()


def run_animation(y, x, unicycle, fps, length):
    h = unicycle.timestep
    y = y[::int((1 / fps) / h)]
    x = x[::int((1 / fps) / h)]

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))
    axes.set_ylim(0, 1.5)
    axes.set_xlim(-2.25, 2.25)
    og_xlim = axes.get_xlim()
    og_ylim = axes.get_ylim()
    # plt.style.use("ggplot")
    plt.style.use('dark_background')
    plt.axis('off')

    # Wheel
    lin1 = axes.plot([], [], color="white", linewidth=2.5)
    # SaddlePost
    lin2 = axes.plot([], [], color="white", linewidth=2)
    # Saddle
    lin3 = axes.plot([], [], color="white", linewidth=5)
    # Ground
    lin4 = axes.plot([], [], linestyle=(0, (4, 8)), color="brown", linewidth=5)
    # Background Trees
    lin5 = axes.plot([], [], color="red", linewidth=5)
    lines = [lin1, lin2, lin3, lin4, lin5]

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        theta = y[:, 0][i]
        dx = y[:, 2][i]
        displacement = x[i]

        r = unicycle.wheel_radius
        l = unicycle.seatpost_length
        w = unicycle.seat_length

        wheel = -displacement / r

        x1 = [r * cos(a) + displacement for a in np.linspace(wheel, 1.8 * pi + wheel, 51)]
        y1 = [r * sin(a) + r for a in np.linspace(wheel, 1.8 * pi + wheel, 51)]

        x2 = [displacement + a * sin(theta) for a in np.linspace(0, l, 2)]
        y2 = [r + a * cos(theta) for a in np.linspace(0, l, 2)]

        x3 = [displacement + l * sin(theta) - a * cos(theta) for a in np.linspace(-w / 2, w / 2, 2)]
        y3 = [r + l * cos(theta) + a * sin(theta) for a in np.linspace(-w / 2, w / 2, 2)]

        lines[0][0].set_data(x1, y1)
        lines[1][0].set_data(x2, y2)
        lines[2][0].set_data(x3, y3)

        # The following is to create a dynamic axis

        raw_xlim1, raw_xlim2 = axes.get_xlim()

        speed_lim = abs(dx / 10)

        x_lim1 = raw_xlim1 + speed_lim
        x_lim2 = raw_xlim2 - speed_lim

        max_x = max(*x1, *x2, *x3) + 1.5 # Add 0.5 to make sure the axis is not too small
        min_x = min(*x1, *x2, *x3) - 1.5 

        # is this what makes it jump?
        if max_x > x_lim2:
        # if max_x > x_lim2 and dx > 0:
            diff = max_x - x_lim2
            axes.set_xlim(raw_xlim1 + diff, raw_xlim2 + diff)
            # fig.canvas.resize_event()
        elif min_x < x_lim1:
        # elif min_x < x_lim1 and dx < 0:
            diff = abs(min_x - x_lim1)
            axes.set_xlim(raw_xlim1 - diff, raw_xlim2 - diff)
            # fig.canvas.resize_event()

        new_xlim1, new_xlim2 = axes.get_xlim()
        ground_length = (new_xlim2 - new_xlim1)

        # Render ground
        x4 = [floor(new_xlim1), floor(new_xlim1) + ground_length + 1]
        y4 = [0, 0]
        lines[3][0].set_data(x4, y4)
        # Render trees
        # x5 = [floor(new_xlim1) + a * ground_length / 4 for a in range(4)]
        # for a in range(4):
        #     x5 = [floor(new_xlim1) + a * ground_length / 4, floor(new_xlim1) + a * ground_length / 4]
        #     y5 = [0, r]
        #     # lines[4][0].set_data(x5, y5)
        # x5 = [floor(new_xlim1) + 1 * ground_length / 4 ] # was a
        # y5 = [0, 0]
        # lines[4][0].set_data(x5, y5)

        return lines

    anim = animation.FuncAnimation(fig, animate, frames=fps * length, blit=False)

    if sys.platform == "win32":
        plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg.exe'
    
    writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Group 8'), bitrate=1800)

    anim.save('animation.mp4', writer=writer)

    open_file('animation.mp4')
