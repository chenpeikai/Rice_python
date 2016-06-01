# Implementation of classic arcade game Pong

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = [WIDTH - HALF_PAD_WIDTH , HEIGHT/2]
paddle2_pos = [HALF_PAD_WIDTH , HEIGHT/2]
ball_pos = [WIDTH/2 , HEIGHT/2]
ball_vel = [1,1]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2 , HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [random.randrange(1, 3),random.randrange(1, 3)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(1, 3),random.randrange(1, 33)]
def botton_handler():
    new_game()
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,paddle1_vel
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    if ball_pos[1] + BALL_RADIUS >= 400 or ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = -ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos , BALL_RADIUS ,12, "Red")
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] + paddle1_vel + HALF_PAD_HEIGHT < HEIGHT and paddle1_pos[1] + paddle1_vel - HALF_PAD_HEIGHT >0:
        paddle1_pos[1] = paddle1_pos[1] + paddle1_vel
    if paddle2_pos[1] + paddle2_vel + HALF_PAD_HEIGHT< HEIGHT and paddle2_pos[1] + paddle2_vel - HALF_PAD_HEIGHT> 0:
        paddle2_pos[1] = paddle2_pos[1] + paddle2_vel
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0] - HALF_PAD_WIDTH , paddle1_pos[1] + HALF_PAD_HEIGHT],
                        [paddle1_pos[0] + HALF_PAD_WIDTH , paddle1_pos[1] + HALF_PAD_HEIGHT],
                        [paddle1_pos[0] + HALF_PAD_WIDTH , paddle1_pos[1] - HALF_PAD_HEIGHT],
                        [paddle1_pos[0] - HALF_PAD_WIDTH , paddle1_pos[1] - HALF_PAD_HEIGHT]],
                       PAD_WIDTH , "White")
    canvas.draw_polygon([[paddle2_pos[0] - HALF_PAD_WIDTH , paddle2_pos[1] + HALF_PAD_HEIGHT],
                        [paddle2_pos[0] + HALF_PAD_WIDTH , paddle2_pos[1] + HALF_PAD_HEIGHT],
                        [paddle2_pos[0] + HALF_PAD_WIDTH , paddle2_pos[1] - HALF_PAD_HEIGHT],
                        [paddle2_pos[0] - HALF_PAD_WIDTH , paddle2_pos[1] - HALF_PAD_HEIGHT]],
                       PAD_WIDTH , "White")
    # determine whether paddle and ball collide    
    if ball_pos[0] + BALL_RADIUS + PAD_WIDTH > WIDTH:
        if ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            score1 = score1 + 1
            spawn_ball(LEFT)
    elif ball_pos[0] - BALL_RADIUS - PAD_WIDTH < 0:
        if ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            score2 = score2 + 1
            spawn_ball(RIGHT)
    # draw scores
    canvas.draw_text(str(score1) , [WIDTH/2+80 , 50] , 60 , "Yellow")
    canvas.draw_text(str(score2) , [WIDTH/2-80 , 50] , 60 , "Yellow")
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 3
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("restart" , botton_handler , 80)

# start frame
new_game()
frame.start()

