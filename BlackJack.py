from tkinter import *
import random
from tkinter import messagebox


def load_card_images(card_list):
    suits = ['heart', 'diamond', 'club', 'spade']
    face_cards= ['king', 'queen', 'jack']

    if TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    for suit in suits:
        for card in range(1,11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = PhotoImage(file=name)
            card_list.append((card, image))
    for suit in suits:
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = PhotoImage(file=name)
            card_list.append((10,image))


def deal_card(frame):
    next_card = deck.pop(0)  # pop retrieves the item and removes it, default index position is last
    deck.append(next_card)  # add the retrieved card to the back of deck to avoid running out of cards
    Label(frame,image=next_card[1], relief='raised').pack(side='left')
    return next_card


def score_hand(hand):
    # calculate total score
    # only one ace has value 11
    score = 0
    ace = False
    for card in hand:
        card_value = card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 21 and ace :
            score -= 10
            ace = False
    return score


def initial_deal():
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    player_card_frame.destroy()
    dealer_card_frame = Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    player_card_frame = Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    # Create the list to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []
    initial_deal()


def deal_dealer():
    dealer_score = score_hand(dealer_hand)

    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer Wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player Wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer Wins!")
    else:
        result_text.set("Draw!")


def deal_player():
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins!")
    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer Wins!")


def shuffle():
    random.shuffle(deck)


def exxit():
    popup = messagebox.askyesno('Exit!', 'Do you really want to quit?')
    if popup == 1:
        mainWindow.quit()


def play():
    initial_deal()
    mainloop()


mainWindow = Tk()
mainWindow.title('BlackJack_Game')
# my_width = mainWindow.winfo_screenwidth()
# my_height = mainWindow.winfo_screenheight()
# mainWindow.geometry('{}x{}+0+0'.format(my_width, my_height))
# mainWindow.geometry('%dx%d+0+0' % (my_width, my_height))
mainWindow.geometry('%dx%d+0+0' % (600, 400))
# %d is a placeholder for numeric in a string
# +0 defines the x and y co-ordinates for origin
mainWindow.configure(bg='green')

# making the interface
result_text = StringVar()
result = Label(mainWindow, textvariable=result_text, font=('Helvetica', 10))
result.grid(row=0, column=0, columnspan=3)
result.configure(bg='green', fg='white')

# making main frame
card_frame = Frame(mainWindow, relief="sunken", borderwidth=1, bg="green")
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)
dealer_score_label = IntVar()
player_score_label = IntVar()
# player_score = 0
# player_ace = False
Label(card_frame, text="Dealer", bg="green", fg='white').grid(row=0, column=0)
Label(card_frame, textvariable=dealer_score_label, bg="green", fg="white").grid(row=1, column=0)
Label(card_frame, text="Player", bg="green", fg="white").grid(row=2, column=0)
Label(card_frame, textvariable=player_score_label, bg='green', fg='white').grid(row=3, column=0)

# dealer frame to hold cards
dealer_card_frame = Frame(card_frame, bg="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
# player frame to hold cards
player_card_frame = Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
# button frame
button_frame = Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

# buttons
dealer_button = Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = Button(button_frame, text='New Game', command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = Button(button_frame, text='Shuffle', command=shuffle)
shuffle_button.grid(row=0, column=3)

quit_button = Button(button_frame, text='Exit Game!', command=exxit)
quit_button.grid(row=0, column=4)

cards = []
load_card_images(cards)
deck = list(cards) + list(cards) + list(cards)
random.shuffle(deck)
player_hand = []
dealer_hand = []


if __name__ == "__main__":
    play()