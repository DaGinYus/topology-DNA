import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Curve:
    def __init__(self, t_start, t_end, resolution):
        self.start = t_start
        self.end = t_end
        self.t = np.linspace(self.start, self.end, num = resolution)
        self.windingno = round((self.end - self.start) / (2 * np.pi))

    # x, y parametric function
    def x(self, t):
        return np.cos(t)

    def y(self, t):
        return np.sin(t)

    def winding(self, t):
        spiral_x = np.cos(self.t[:t.astype(int)])
        spiral_y = np.sin(self.t[:t.astype(int)])
        return (spiral_x, spiral_y)

X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -2, 2
RESOLUTION = 200
START, END = 0, 2 * np.pi
REF_X, REF_Y = 0, 0
FPS = 60

fig, ax = plt.subplots()
curve = Curve(START, END, RESOLUTION)

def set_axes(x_min, x_max, y_min, y_max):
    plt.axis([x_min, x_max, y_min, y_max])
    plt.axis("scaled")
    ax.spines["left"].set_position("center")
    ax.spines["top"].set_position("center")
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.tick_top()
    ax.set_xticks([])
    ax.set_yticks([])

def animate(i):
    ax.clear()
    ax.plot(curve.x(curve.t), curve.y(curve.t))
    ax.plot([REF_X, curve.x(i)], [REF_Y, curve.y(i)])
    ax.plot(curve.winding(i)[0], curve.winding(i)[1])
    set_axes(X_MIN, X_MAX, Y_MIN, Y_MAX)

ani = animation.FuncAnimation(fig, animate, frames = np.linspace(START, END, 100), interval = 1000 / FPS, repeat = True)
plt.show()
print(curve.windingno)
