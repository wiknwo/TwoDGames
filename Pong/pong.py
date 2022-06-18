"""
Pong is a table tennis-themed twitch arcade sports video 
game, featuring simple two-dimensional graphics, 
manufactured by Atari and originally released in 1972. It 
was one of the earliest arcade video games.

The player controls an in-game paddle by moving it 
vertically across the left or right side of the screen. 
They can compete against another player controlling a 
second paddle on the opposing side. Players use the 
paddles to hit a ball back and forth. The goal is for 
each player to reach eleven points before the opponent; 
points are earned when one fails to return the ball to the 
other.
"""
import turtle

"""Setting up the window"""
window = turtle.Screen()
window.title("Pong by @wiknwo")
window.bgcolor("black") # Set background color
window.setup(width=800, height=600) # Set size of window
window.tracer(0) # Stops window from updating which allows us to speed up the game

"""Adding paddles and ball"""
# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0) # Speed of animation set to maximum possible speed
paddle_a.shape("square") # By default, the shape is 20 x 20 pixels
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1) # Stretch the width by a factor of 5 making the paddle 20 x 5 = 100 pixels tall and 20 pixels wide
paddle_a.penup() # Turtles by definition draw a line as they are moving and we don't want this to happen so we call the penup() method
paddle_a.goto(-350, 0) # Set starting coordinates of paddle_a: In the game, [0, 0] is in the middle. Minus is to the left and Plus is to the right

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0) # Speed of animation set to maximum possible speed
paddle_b.shape("square") # By default, the shape is 20 x 20 pixels
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1) # Stretch the width by a factor of 5 making the paddle 20 x 5 = 100 pixels tall and 20 pixels wide
paddle_b.penup() # Turtles by definition draw a line as they are moving and we don't want this to happen so we call the penup() method
paddle_b.goto(350, 0) # Set starting coordinates of paddle_b: In the game, [0, 0] is in the middle

# Ball
ball = turtle.Turtle()
ball.speed(0) # Speed of animation set to maximum possible speed
ball.shape("circle") # By default, the shape is 20 x 20 pixels
ball.color("white")
ball.penup() # Turtles by definition draw a line as they are moving and we don't want this to happen so we call the penup() method
ball.goto(0, 0) # Set starting coordinates of ball: In the game, [0, 0] is in the middle
ball.dx = 0.25 # Every time the ball moves in the x-direction, it will move by 0.25 pixels
ball.dy = 0.25

"""Scoring mechanism: drawing the score on the screen"""
score_a = 0
score_b = 0
pen = turtle.Turtle() # Defining a pen with which we will draw the score on the screen. Every turtle starts out in the middle of the screen unless you move it somewhere
pen.speed(0)
pen.color("white")
pen.penup() # We don't want to draw a line when pen moves
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

"""Functions: Breaking the problem down into subproblems"""
def paddle_a_up():
    """Method to move paddle a up"""
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    """Method to move paddle a down"""
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    """Method to move paddle b up"""
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    """Method to move paddle b down"""
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

"""Keyboard bindings"""
window.listen() # Tells Turtle to listen for keyboard input
window.onkeypress(paddle_a_up, 'w') # When the user presses 'w' (Lowercase 'w' so uppercase won't work) call the function paddle_a_up()
window.onkeypress(paddle_a_down, 's') 
window.onkeypress(paddle_b_up, "Up") # 'Up' represents the up arrow key in Turtle
window.onkeypress(paddle_b_down, "Down")

# Game Loop
while True:
    window.update()
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking: Top and bottom borders
    # Compare the ball's y-coordinate with
    # the border. Height of the border is set to 600 that
    # means the top y-coordinate is 300 and the bottom 
    # y-coordinate is -300. However, the ball is 20 x 20 pixels
    # so we will split the difference

    # Checking top border
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1 # Reverses the direction of the ball

    # Checking bottom border
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1 # Reverses the direction of the ball

    # Border checking: Left and right borders
    # We set the width to 800 so that means 400 on the left
    # and -400 on the right.

    # Checking right border: Ball passed paddle and is off the screen
    if ball.xcor() > 390:
        ball.goto(0, 0) # Reset ball to the centre
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Checking left border: Ball passed paddle and is off the screen
    if ball.xcor() < -390:
        ball.goto(0, 0) # Reset ball to the centre
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Ball collision with paddle: when ball touches paddle it will reverse
    # Compare the x and y coordinates of the paddle and the ball.
    # paddle_b is at 350 so the x coordinate of the centre is 350.
    # The centre is 20 x 100 (width x height). So we need to
    # make sure the ball is in range and if it is we will call that
    # a bounce.

    # Ball collision with paddle_b
    # ball.xcor() > 340: Means the edges of the ball and paddle_b are basically touching
    if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1

    # Ball collision with paddle_a
    if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1    