from manim import * 


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()
        square.set_fill(BLUE_E, opacity=0.7, family=False)
        square.rotate(PI / 4)


        # Transforms
        self.play(Create(square)) 
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

        self.clear()

        # Positioning
        square = Square()
        square.set_fill(BLUE_E, opacity=0.7, family=False)
        square.rotate(PI / 4)

        square.next_to(circle, RIGHT, buff=1.0)
        self.play(Create(circle), Create(square))
        self.play(FadeOut(circle))

        self.clear()

        # Animating 
        square, circle = Square(), Circle()
        self.play(Create(square))
        self.play(square.animate.rotate(PI/4))
        self.play(Transform(square, circle))
        self.play(square.animate.set_fill(PINK, opacity=0.3))
        self.play(square.animate.shift(PI / 2))

        self.clear()

        # More Animating
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)

        self.play(left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2)
        self.wait()

        self.clear()

        # Transform! 
        self.transform()
        self.wait(0.5)  # wait for 0.5 seconds
        self.replacement_transform()
        
        self.clear()



    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()

        # Transform the whole "b" shape into "a" shape
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()

        # Just replaces the "b" shape in the scene 
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(a))






    