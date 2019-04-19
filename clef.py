import turtle
import math


def drawline(t, length):
    """Draw a line of length 'length' at the turtle 't' current position and heading."""
    t.down()
    t.forward(length)
    t.up()
    t.backward(length)


def draw_5_line(t, length, gap):
    """Draws 5 lines of length 'length' spaced 'gap' units apart."""
    for i in range(5):
        drawline(t, length)
        t.left(90)
        t.forward(gap)
        t.right(90)


def draw_partof_circle(t, radius, frac, goleft, startwide, endwide, n=100):
    """Draws a partial circle or arc approximated by a polygon.
    Line width is linearly interpolated from starting and ending values.

    :param t: the Turtle object
    :param radius: the size of the circle
    :param frac: the fraction of circle to be drawn (i.e. 0.5 for a semicircle)
    :param goleft: boolean variable that determines which direction to turn the turtle. (left is True, right False)
    :param startwide: the initial line width
    :param endwide: the final line width
    :param n: the number of points to approximate the circle (default 100)
    """
    steps = int(n * frac)
    # print(t.heading())
    if goleft:  # goleft true
        for i in range(steps):
            t.forward(radius * 2 * math.sin(math.pi / n))
            t.width(startwide + (i / steps) * (endwide - startwide))
            t.left(360 / n)
    else:  # goright
        for i in range(steps):
            t.forward(radius * 2 * math.sin(math.pi / n))
            t.width(startwide + (i / steps) * (endwide - startwide))
            t.right(360 / n)
    # print(t.heading())


def draw_clef(t, tilt, x, y):
    """Draws a treble clef starting at position (x,y) with tilt angle 'tilt' using Turtle t.
    May not work for tilt angles other than 10.
    """
    t.up()
    t.seth(0)
    t.goto(x + 3, y)
    t.dot(12)
    t.ht()
    t.goto(x, y)
    t.right(90 - tilt)
    t.down()
    draw_partof_circle(t, 10, 0.5, True, 2, 1)  # this doesn't change heading
    t.backward((y + 100) / math.cos(tilt))
    draw_partof_circle(t, 25, 0.15, False, 1, 6)
    t.right(90)
    draw_partof_circle(t, 25, 0.25, False, 3, 8)
    t.seth(226)
    t.width(8)
    t.forward(18)
    draw_partof_circle(t, 30, 0.22, True, 8, 3)
    draw_partof_circle(t, 30, 0.14, True, 3, 2)
    t.seth(tilt + 10)
    draw_partof_circle(t, 20, 0.42, True, 2, 8)
    t.seth(180 + tilt)
    draw_partof_circle(t, 15, 0.4, True, 8, 1)


def quarternote(t, x, y, half=False, stem=True):
    """Draws a music note at position (x,y).
    half - boolean variable that disables note filling if true
    """
    t.seth(0)
    if y <= -20:
        t.up()
        t.goto(x - 10, y)
        t.down()
        t.forward(25)
    t.up()
    t.goto(x, y - 8)
    t.down()
    if half == False:
        t.begin_fill()
    flatoval(t, 10)
    t.end_fill()
    if stem:  # draw the stem
        t.circle(10, 90)
        t.seth(90)
        t.forward(70)


def halfnote(t, x, y):
    """Draws a half note."""
    quarternote(t, x, y, half=True)


def wholenote(t, x, y):
    """Draws a whole note."""
    quarternote(t, x, y, half=True, stem=False)


def flatoval(turtle, r):  # Horizontal Oval
    """Draw a horizontal oval with "size" r.
    """
    for loop in range(2):
        # turtle.circle(r, 90)
        # turtle.circle(r / 2, 90)
        draw_partof_circle(turtle, r, 0.25, True, 1, 4, 25)
        draw_partof_circle(turtle, r / 2, 0.25, True, 4, 1, 25)


def draw_measure(t, init_gap, measure_gap, num_lines):
    t.left(90)
    drawline(t, 80)
    t.right(90)
    t.forward(init_gap)
    t.left(90)
    drawline(t, 80)
    for i in range(num_lines):
        t.right(90)
        t.forward(measure_gap)
        t.left(90)
        drawline(t, 80)


# def notes(notestring):
#     pass
# for char in notestring:

# return coordinates


s = turtle.Screen()
border = 0
aspect_ratio = 1
x_max = 630
s.setworldcoordinates(0 - border, 20 - x_max / aspect_ratio / 2 - border, x_max - border,
                      x_max / aspect_ratio / 2 + 20 - border)
# print(x_max / ((x_max / aspect_ratio / 2) + 20 - (20 - x_max / aspect_ratio / 2)))
# make the stave
liner = turtle.Turtle()
liner.ht()
liner.speed(0)
draw_5_line(liner, x_max - border, 20)

# draw the clef
arcy = turtle.Turtle()
arcy.speed(0)
draw_clef(arcy, 10, 25, -20)

# draw measurelines
meas = turtle.Turtle()
meas.ht()
meas.width(2)
draw_measure(meas, 190, 150, 3)

# draw notes
# notes('CCGGHHG*FFEEDDC*')
player = turtle.Turtle()
player.ht()
player.speed(0)
player.width(2)
quarternote(player, 70, -20)
# quarternote(player, 100, -20)
# quarternote(player, 130, 20)
# quarternote(player, 160, 20)
# quarternote(player, 220, 30)
# quarternote(player, 250, 30)
# halfnote(player, 280, 20)
# quarternote(player, 370, 10)
# quarternote(player, 400, 10)
# quarternote(player, 430, 0)
# quarternote(player, 460, 0)
# quarternote(player, 520, -10)
# quarternote(player, 550, -10)
# halfnote(player, 580, -20)

s.exitonclick()
