# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global count
    frame = simplegui.create_frame("guess number" , 300 ,300)
    frame.add_button("range100" , range100)
    frame.add_button("range1000" , range1000)
    frame.add_input("input_guess" , input_guess , 100)
    # remove this when you add your code    
    frame.start()


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    # remove this when you add your code    
    global count
    count = random.randint(0,100)

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global count
    count = random.randint(0,1000)
    
    
def input_guess(guess):
    # main game logic goes here	
    guess_num = int(guess)
    if(count > guess_num):
        print("higher")
    elif(count < guess_num):
        print("lower")
    else:
        print("you are right")
    # remove this when you add your code
    
# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

