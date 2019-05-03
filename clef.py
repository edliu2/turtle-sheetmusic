import turtle
import math
import re


def drawline(t, length):
    """Draw a line of length 'length' at the turtle 't' current position and heading."""
    t.down()
    t.forward(length)
    t.up()
    t.backward(length)


def draw_n_line(t, n, length, gap):
    """Draws 5 lines of length 'length' spaced 'gap' units apart."""
    t.ht()
    t.speed(0)
    for i in range(n):
        drawline(t, length)
        t.left(90)
        t.forward(gap)
        t.right(90)


def draw_partof_circle(t, radius, frac, goleft=True, startwide=2, endwide=2, n=100):
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
    t.speed(0)
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
    t.width(2)
    if y <= -20:
        t.up()
        t.goto(x - 10, y + y % 20)
        draw_n_line(t=t, n=y // -20, length=25, gap=20)
    elif y >= 100:
        t.up()
        t.goto(x - 10, 100)
        draw_n_line(t=t, n=y // 20 - 4, length=25, gap=20)
    t.up()
    t.goto(x, y - 8)
    t.down()
    if half == False:
        t.begin_fill()
    flatoval(t, 10)
    t.end_fill()
    if stem:  # draw the stem
        if y <= -30:  # notes lower than high C
            t.circle(10, 90)  # circle around to right side
            t.seth(90)
            t.forward(40 - y)  # draw stem
        elif -30 < y < 50:
            t.circle(10, 90)
            t.seth(90)
            t.forward(70)
        elif 50 <= y <= 100:
            t.seth(-90)
            t.forward(65)
        elif y > 100:
            t.seth(-90)
            t.forward(y - 45)


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

def eighth_rest(t,x,y=50):
    t.up()
    t.ht()
    t.goto(x - 8, y)
    t.down()
    t.width(2)
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    t.seth(0)
    clef.draw_partof_circle(t,13,0.21,n=100,startwide=3,endwide=2)
    t.backward(33)

def sixteenth_rest(t,x):
    eighth_rest(t,x,50)
    eighth_rest(t,x-6,30)


def read_notes(notestring, x_start=70, x_spacing=30, y_spacing=10):
    """ Reads in a string from ABC-notation file and creates note objects.
    Does not handle headers at the moment.
    """
    header = re.match(r'.:', notestring)
    if header:  # Headers are currently not supported
        return None
    else:
        measure_list = notestring.split('|')
        pattern = re.compile(r'''
        
        (_?[_=^]?\^?                 # accidentals (optional)
        [a-gz]                        # each note has a letter
        [,']?)                       # followed by punctuation for low or high octave (optional)
        (/?\d*)                      # followed by length modifier (optional, also extract length for spacing)
        
        ''', flags=re.IGNORECASE | re.VERBOSE)
        note_names = ('C,', 'D,', 'E,', 'F,', 'G,', 'A,', 'B,',
                      'C', 'D', 'E', 'F', 'G', 'A', 'B',
                      'c', 'd', 'e', 'f', 'g', 'a', 'b',
                      "c'", "d'", "e'", "f'", "g'", "a'", "b'")
        y_values = range(-9 * y_spacing, 19 * y_spacing, y_spacing)
        treble_dict = dict(zip(note_names, y_values))
        # print(treble_dict)

        note_object_list = []
        for measure in measure_list:
            note_charlist = list(filter(None, re.findall(pattern, measure)))
            note_charlist.append('|')
            # print(note_charlist)
            for note in note_charlist:
                if note == '|':
                    m = Measure(x_start)
                    note_object_list.append(m)
                elif note[0] == 'z':
                    z = Rest(x_start)
                    note_object_list.append(z)
                else:
                    print('{}-->{}'.format(note, treble_dict.get(note[0], 0)))
                    n = Note(x_start, treble_dict.get(note[0], 0), 'quarter')
                    print(n)
                    note_object_list.append(n)

                x_start += x_spacing
        return note_object_list


class Note:
    """ Note class that represents the type and coordinates of a note."""

    def __init__(self, x=0, y=0, type='quarter'):
        """Create a new Note object at (x,y) with a given type."""
        self.x = x
        self.y = y
        self.type = type

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getType(self):
        return self.type

    def draw(self, t):
        if self.type == 'quarter':
            quarternote(t, self.x, self.y)
        elif self.type == 'half':
            halfnote(t, self.x, self.y)

    def __str__(self):
        return '{} note at ({}, {})'.format(self.type, self.x, self.y)


class Measure:
    """ Measure class that represents the location of a measure line."""

    def __init__(self, x=0):
        """Create a new Measure object at x."""
        self.x = x

    def getX(self):
        return self.x

    def draw(self, t):
        t.up()
        t.ht()
        t.goto(self.x, 0)
        t.seth(90)
        t.down()
        t.forward(80)

    def __str__(self):
        return "Measure at x = " + str(self.x)

class Rest:
    """ Rest class that represents the location and type of a rest."""

    def __init__(self, x=0,type='quarter'):
        """Create a new Rest object at x."""
        self.x = x
        self.type = type

    def getX(self):
        return self.x

    def draw(self, t):
        t.up()
        t.ht()
        t.goto(self.x - 8, 72)
        t.seth(-45)
        t.down()
        t.width(3)
        t.forward(25.3)
        t.right(90)
        t.forward(2.2)
        t.width(6)
        t.forward(16.8)
        t.width(3)
        t.forward(2.2)
        t.left(90)
        t.forward(15.1)
        t.backward(1)
        t.right(140)
        draw_partof_circle(t, 10, 0.52, startwide=5, endwide=5)
        t.width(2)

    def __str__(self):
        return "{} rest at x = {}".format(self.type, self.x)


def main():
    s = turtle.Screen()
    border = 0
    aspect_ratio = 1
    x_max = 1200
    s.setworldcoordinates(0 - border, 20 - x_max / aspect_ratio / 2 - border, x_max - border,
                          x_max / aspect_ratio / 2 + 20 - border)
    # print(x_max / ((x_max / aspect_ratio / 2) + 20 - (20 - x_max / aspect_ratio / 2))) should be aspectratio
    # make the stave
    liner = turtle.Turtle()
    draw_n_line(liner, 5, x_max - border, 20)

    # draw the clef
    # arcy = turtle.Turtle()
    # draw_clef(arcy, 10, 25, -20)

    # read in a notestring and create note objects
    with open('test_notes.txt', 'r') as myfile:
        list_of_notes = []
        for line in myfile:
            n = read_notes(line)
            list_of_notes += n

    # draw measurelines and notes
    player = turtle.Turtle()
    player.ht()
    player.speed(0)
    player.width(2)

    for notes in list_of_notes:
        print(notes)
        notes.draw(player)

    s.exitonclick()


if __name__ == '__main__':
    main()
