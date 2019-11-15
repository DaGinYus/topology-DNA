import time
from manimlib.imports import *

class Shapes(Scene):
    def construct(self):
        circle = Circle(fill_color = GOLD_A, fill_opacity = 1)
        square = Square(color = PURPLE_A)
        line = Line(np.array([0,1,0]), np.array([0,-1,0]))

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeIn(line), FadeOut(square)) # FadeOut fades out square, even though it transformed to circle
        self.play(Rotating(line))
        time.sleep(2)
        self.play(FadeOut(line))
