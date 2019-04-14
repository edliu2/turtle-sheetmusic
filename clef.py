import turtle
import math
import re


def drawline(t, length):
    """Draw a line of length 'length' at the turtle 't' current position and heading."""
    t.down()
    t.forward(length)
    t.up()
    t.backward(length)


def draw_5_line(t, length, gap):
    """Draws 5 lines of length 'length' spaced 'gap' units apart."""
    t.ht()
    t.speed(0)
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
        [a-g]                        # each note has a letter
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

        for measure in measure_list:
            note_charlist = list(filter(None, re.findall(pattern, measure)))
            note_charlist.append('|')
            print(note_charlist)
            for note in note_charlist:
                if note == '|':
                    # new_measure(x_start)
                    pass
                else:
                    print('{}-->{}'.format(note, treble_dict.get(note[0], 0)))
                    # new_note(x_start, treble_dict.get(note[0], 0), 'quarter')
                    pass

                x_start += x_spacing

    return


# return
def main():
    s = turtle.Screen()
    border = 0
    aspect_ratio = 1
    x_max = 630
    s.setworldcoordinates(0 - border, 20 - x_max / aspect_ratio / 2 - border, x_max - border,
                          x_max / aspect_ratio / 2 + 20 - border)
    # print(x_max / ((x_max / aspect_ratio / 2) + 20 - (20 - x_max / aspect_ratio / 2)))
    # make the stave
    liner = turtle.Turtle()
    draw_5_line(liner, x_max - border, 20)

    # draw the clef
    # arcy = turtle.Turtle()
    # draw_clef(arcy, 10, 25, -20)

    # read in a notestring and create note objects
    with open('test_notes.txt', 'r') as myfile:
        for line in myfile:
            list_of_notes = read_notes(line)

    # draw measurelines and notes
    player = turtle.Turtle()
    player.ht()
    player.speed(0)
    player.width(2)
    # for notes in list_of_notes:
    # notes.draw()

    s.exitonclick()


if __name__ == '__main__':
    main()
