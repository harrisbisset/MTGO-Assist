import turtle
t = turtle.Turtle()


class Shape():
    def __init__(self):
        self.lineThickness = 1

    def erase(self, proportions):
        pass

class Circle(Shape):
    def __init__(self):
        pass

    def draw(self, proportions):
        t.circle(proportions)

class Square(Shape):
    def __init__(self):
        pass

    def draw(self, proportions):
        for i in range(0,3):
            t.forward(proportions)
            t.left(90)

class Triangle(Shape):
    def __init__(self):
        pass

    def draw(self, proportions):
        pass

shaperClass = Shape()

while True:
    #loop
    shapeToDraw = input("What shape do you want to draw?")
    dimenions = input("What dimensions should the shape be?")
    if shapeToDraw.lower() == 'triangle':
        Triangle.draw(dimenions)
    elif shapeToDraw.lower() == 'circle':
        #dimensions is a single value, which is the radius of the circle
        Circle.draw(dimenions)
    elif shapeToDraw.lower() == 'square':
        #dimenions is a single value, which is the length of a side
        Square.draw(dimenions)
    else:
        print(shapeToDraw + ' is not a valid shape to draw!')