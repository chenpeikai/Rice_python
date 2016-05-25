# template for "Stopwatch: The Game"
try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# define global variables

time_message = '0:00.0'
score_str = "0/0"
is_stop = True
tick = 0
total_num = 0
right_num = 0
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    ms = t%10
    s = (t%600 - ms)/10
    minute = t/600
    my_str = "%d:%02d.%d"%(minute , s , ms)
    return my_str
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global is_stop
    is_stop = False
    timer.start()
#check if you had stop it right
def stop_handler():
    global total_num , right_num , score_str
    if is_stop is True:
        return
    total_num = total_num + 1
    if tick%10 == 0 and tick%50 == 0:
        right_num = right_num + 1
    score_str = "%d/%d"%(right_num,total_num)
def reset_handler():
    global time_message,tick,is_stop
    tick = 0
    timer.stop()
    time_message = '0:00.0'
    is_stop = True
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tick,time_message
    tick  = tick + 1
    time_message = format(tick)

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(time_message,(120,150),30,"White")
    canvas.draw_text(score_str,(240,30),30,"Red")
# create frame
frame = simplegui.create_frame("clock" , 300 , 300)
timer = simplegui.create_timer(100, timer_handler)
# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button("start",start_handler,100)
frame.add_button("stop",stop_handler,100)
frame.add_button("reset",reset_handler,100)
# start frame
frame.start()
# Please remember to review the grading rubric

