import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Curve:
    def __init__(self, t_start, t_end, resolution):
        self.start = t_start
        self.end = t_end
        self.t = np.linspace(self.start, self.end, num = resolution)
        self.windingno = 0
        self.theta = 0
        self.spiral_x = []
        self.spiral_y = []

    # x, y parametric function
    def x(self, t):
        return np.cos(t)

    def y(self, t):
        return np.sin(t)

    def vector(self, t):
        """returns vector from reference point to curve at time t"""
        self.v = [self.x(t) - REF_X, self.y(t) - REF_Y]
        return self.v[0], self.v[1]

    def get_theta(self, t):
        """calculates angle between vector and horizontal unit vector"""
        self.vector(t)
        v_mag = np.sqrt(self.v[0] ** 2 + self.v[1] ** 2)
        v_hat = np.divide(self.v, v_mag)
        unit_v = [REF_X + 1, REF_Y]
        dot = np.vdot(unit_v, v_hat) # cos
        cross = np.cross(unit_v, v_hat) # sin
        angle = np.arctan2(cross, dot)

        # convert angle to positive if negative
        if angle < 0:
            angle += 2 * np.pi
        return angle

    def count_winds(self, t):
        """checks if vector has rotated past origin and updates windingno"""
        TIMESTEP = 0.2
        adjustment = self.windingno * 2 * np.pi
        self.theta = self.get_theta(t) + self.windingno * 2 * np.pi
        theta_future = self.get_theta(t + TIMESTEP) + self.windingno * 2 * np.pi # theta gets reset to 0 when it passes origin
        if theta_future < self.theta:
            self.windingno += 1
    
    def winding(self, t):
        """draws spiral representation of winding around reference point"""
        self.count_winds(t)
        r = 0.02 * self.theta
        self.spiral_x.append(r * np.cos(self.theta))
        self.spiral_y.append(r * np.sin(self.theta))
        return self.spiral_x, self.spiral_y

    
X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -2, 2
RESOLUTION = 200
START, END = 0, 4 * np.pi
REF_X, REF_Y = 0, 0
FPS = 60
STEP = 50

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
    # plot vector
    vector_x, vector_y = curve.vector(i)
    ax.plot([REF_X, vector_x], [REF_Y, vector_y])
    # plot spiral
    spiral_x, spiral_y = curve.winding(i)
    ax.plot(spiral_x, spiral_y)
    ax.text(X_MIN + 0.5, Y_MAX - 1, "winding number = %d" %curve.windingno, horizontalalignment = "left", verticalalignment = "bottom")
    set_axes(X_MIN, X_MAX, Y_MIN, Y_MAX)

ani = animation.FuncAnimation(fig, animate, frames = np.linspace(START, END, STEP), interval = 1000 / FPS, repeat = False)
plt.show()
