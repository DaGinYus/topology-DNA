import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Curve:
    """class for managing space curves"""
    
    def __init__(self, t_start, t_end, resolution):
        self.t = np.linspace(t_start, t_end, num = resolution)

    # x, y parametric function
    def x(self, t):
        return np.cos(t)
    def y(self, t):
        return np.sin(t)
    
    def theta(self, t_value):
        """angle as vector winds around reference point"""
        self.theta = self.t[t_value]
        return self.theta

    def winding(self, start, end):
        return round((self.theta(end), self.theta(start)) / (2 * np.pi))


X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -2, 2
RESOLUTION = 200
START, END = 0, 2 * np.pi
REF_X, REF_Y = 0, 0
FPS = 60

fig, ax = plt.subplots()

# set up graph axes
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

curve = Curve(START, END, RESOLUTION)
ax.plot(curve.x(curve.t), curve.y(curve.t))

def animate(i):
    ax.clear()
    ax.plot(curve.x(curve.t), curve.y(curve.t))
    ax.plot([REF_X, curve.x(i)], [REF_Y, curve.y(i)])
    set_axes(X_MIN, X_MAX, Y_MIN, Y_MAX)

ani = animation.FuncAnimation(fig, animate, frames = np.linspace(START, END), interval = 1000 / FPS)
plt.show()
