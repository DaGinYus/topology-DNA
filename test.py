from manimlib.imports import *

class Shapes(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
