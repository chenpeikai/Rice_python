# implementation of card game - Memory

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
cards = []
exposed = []
turns = 0
pair_count = 0
pair_pos = []
# helper function to initialize globals
def new_game():
    global cards,exposed,turns,pair_pos
    cards = range(0,8)
    cards = cards + cards
    random.shuffle(cards)
    exposed = [False]*16
    turns = 0
    pair_count = 0
    pair_pos = [0]*2
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global turns,exposed,pair_count,pair_pos
    click_pos = pos[0] // 50
    if exposed[click_pos] == True:
        return
    turns += 1
    label.set_text("Turns = %d"%(turns))
    if pair_count < 2:
        exposed[click_pos] = True
        pair_pos[pair_count] = click_pos
        pair_count += 1
    else:
        pair_count = 0
        if cards[pair_pos[0]] != cards[pair_pos[1]]:
            exposed[pair_pos[0]] = False
            exposed[pair_pos[1]] = False
        pair_pos[pair_count] = click_pos
        exposed[click_pos] = True
        pair_count += 1
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards,exposed
    for card_index in range(len(cards)):
        card_pos = 50 * card_index
        canvas.draw_text(str(cards[card_index]), [card_pos,80],100,"White")
    for card_index in range(len(cards)):
        cover_pos_start = 50 * card_index
        cover_pos_end = 50 * (card_index + 1)
        if exposed[card_index] == False:
            canvas.draw_polygon([(cover_pos_start, 0), (cover_pos_start, 100), (cover_pos_end, 100),(cover_pos_end, 0)], 1, 'White','Green')
        


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
