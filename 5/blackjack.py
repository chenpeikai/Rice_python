# Mini-project #6 - Blackjack

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object
        

    def __str__(self):
        # return a string representation of a hand
        s = ""
        for card in self.cards:
            s = s + "%s " % (card)
        return "Hand countains %s" % (s)

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_pos = pos
        for card in self.cards:
            card.draw(canvas , card_pos)
            card_pos[0] += CARD_SIZE[0] + 10
            
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append( Card(suit,rank) )

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)
        
    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
        
    def __str__(self):
        # return a string representing the deck
        s = ""
        for card in self.cards:
            s = s + "%s " % (card)
        return "Deck countains %s" % (s) 


#define event handlers for buttons
def deal():
    global outcome, in_play,deck,deck,palyer,dealer
    
    deck.shuffle()
    palyer = Hand()
    dealer = Hand()

    palyer.add_card(deck.deal_card())
    palyer.add_card(deck.deal_card())
    
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    in_play = True

def hit():
    # replace with your code below
    global socers
    # if the hand is in play, hit the player
    if palyer.get_value() < 21:
        palyer.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    else:
        print("you have hust!")
        score  = score  - 1


def stand():
    # replace with your code below
    pass 
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global dealer,palyer,score

    palyer.draw(canvas, [100, 300])
    dealer.draw(canvas, [100,100])
    canvas.draw_text("score:%d" % (score) , [500,50] , 30 , "Red")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deck = Deck()

deal()
frame.start()


# remember to review the gradic rubric
