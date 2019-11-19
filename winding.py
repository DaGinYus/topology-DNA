import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Curve:
    def __init__(self, t_start, t_end, resolution):
        self.start = t_start
        self.end = t_end
        self.t = np.linspace(self.start, self.end, num = resolution)
        self.theta = 0
        self.spiral_x = []
        self.spiral_y = []

    # x, y parametric function
    def x(self, t):
        return np.cos(t)

    def y(self, t):
        return np.sin(t)

    def vector(self, t):
        """Returns vector from reference point to curve at time t."""
        self.v = [self.x(t) - REF_X, self.y(t) - REF_Y]

    def angle(self, t):
        """Calculates angle between vector and horizontal unit vector."""
        self.vector(t)
        v_mag = np.sqrt(self.v[0] ** 2 + self.v[1] ** 2)
        v_hat = np.divide(self.v, v_mag)
        v_base = [1, 0]
        dot = np.vdot(v_base, v_hat) # cos
        cross = np.cross(v_base, v_hat) # sin
        angle = np.arctan2(cross, dot)
        # convert angle if negative
        if angle < 0:
            angle += np.pi
        return angle

    def sum_angle(self, t):
        """Sums changes in angle to calculate theta.
           It is implemented this way so it can handle winding and unwinding.
           Make sure this is only called ONCE"""
        TIMESTEP = (self.end - self.start) / RESOLUTION

        theta1, theta2 = self.angle(t), self.angle(t + TIMESTEP)
        delta = theta2 - theta1
        print(delta)
        self.theta += delta

    def windingno(self):
        """Uses winding number formula (theta(b) - theta(a)) / 2pi to update winding number.
           Assume that theta_0 = 0."""
        return np.floor(self.theta / (2 * np.pi))

    def spiral(self, t):
        """Graphs a spiral visualization of the winding number."""
        self.sum_angle(t)
        r = 0.02 * self.theta # scaling factor for spiral
        self.spiral_x.append(r * np.cos(self.angle(t)) + REF_X)
        self.spiral_y.append(r * np.sin(self.angle(t)) + REF_Y)

    # def count_winds(self, t):
    #     """checks if vector has rotated past initial point and updates windingno"""
    #     TIMESTEP = (self.end - self.start) / RESOLUTION
        
    #     adjustment = self.windingno * 2 * np.pi
    #     self.theta = self.get_theta(t) - self.theta_0
    #     theta_future = self.get_theta(t + TIMESTEP) - self.theta_0

    #     self.theta += adjustment
    #     theta_future += adjustment

    #     if theta_future < self.theta:
    #         self.windingno += 1
    
    # def winding(self, t):
    #     """draws spiral representation of winding around reference point"""
    #     self.count_winds(t)
    #     r = 0.02 * (self.theta - self.theta_0)
    #     print(self.theta)
    #     self.spiral_x.append(r * np.cos(self.theta + self.theta_0) + REF_X)
    #     self.spiral_y.append(r * np.sin(self.theta + self.theta_0) + REF_Y)
    #     return self.spiral_x, self.spiral_y

    
X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -2, 2
RESOLUTION = 200
START, END = 0, 2 * np.pi
REF_X, REF_Y = -0, 0
FPS = 60

fig, ax = plt.subplots()
curve = Curve(START, END, RESOLUTION)

def set_axes(x_min, x_max, y_min, y_max):
    plt.axis("scaled")
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
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
    ax.plot([REF_X, curve.x(i)], [REF_Y, curve.y(i)])
    # plot spiral
    curve.spiral(i)
    ax.plot(curve.spiral_x, curve.spiral_y)
    # display winding number in real time
    ax.text(X_MIN, Y_MAX, "winding number = %d" %curve.windingno(), horizontalalignment = "left", verticalalignment = "bottom")
    set_axes(X_MIN, X_MAX, Y_MIN, Y_MAX)

ani = animation.FuncAnimation(fig, animate, frames = np.linspace(START, END, RESOLUTION), interval = 1000 / FPS, repeat = False)
plt.show()
