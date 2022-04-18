# # Milestone Project 2 - Blackjack Game
# In this milestone project you will be creating a Complete BlackJack Card Game in Python.

# Here are the requirements:

# * You need to create a simple text-based [BlackJack](https://en.wikipedia.org/wiki/Blackjack) game
# * The game needs to have one player versus an automated dealer.
# * The player can stand or hit.
# * The player must be able to pick their betting amount.
# * You need to keep track of the player's total money.
# * You need to alert the player of wins, losses, or busts, etc...

# And most importantly:

# You must use OOP and classes in some portion of your game. 
# You can not just use functions in your game. 
# Use classes to help you define the Deck and the Player's hand. 
# There are many right ways to do this, so explore it well!

# Feel free to expand this game. Try including multiple players. 
# Try adding in Double-Down and card splits! 

import random
import time
import os

def clrscr():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
        'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#Defining the hand class. 
#Every player will have a hand containing cards
class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0

    #Printing the cards in the hand and the total value
    def __str__(self, align=0):
        output = ""
        #Left align for players, some tabs for the dealer
        if align == 0:
            for c in self.cards:
                output += c.ranksuit() + '\n'
            output += f'\tTotal Hand: {self.value}'
        else:
            for c in self.cards:
                output += f'{" ":>60}' + c.ranksuit() + f'\n'
            output += f'{" ":>50} {self.value} :Total Hand'
        return output

    #Returns the value of the hand
    def handvalue(self):
        return self.value

    #Returns if the hand is busted
    def handbusted(self):
        if self.value > 21:
            return True
        else:
            return False

    #Add a card to the hand and calculate at the same time the total hand value
    def add(self, card):
        self.cards.append(card)
        if self.value > 10 and card.value == 11:
            self.value += 1
        else:
            self.value += card.value

    def isblackjack(self):
        if len(self.cards) and self.value==21:
            return True
        else:
            return False

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def ranksuit(self):
        return f'{self.rank} of {self.suit}'

    def value(self):
        return self.value

#A deck of cards
class Deck:
    #For each suit and rank, create a card object 
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit,rank))
    
    #Imports random for shuffling the deck
    def shuffle_cards(self):
        random.shuffle(self.cards)

    #Deals one to the player and removes it from the deck
    def deal_one(self):
        return self.cards.pop()


class Player:

    def __init__(self, name, money):
        self.name = name
        self.money = int(money)
        self.hand = Hand()
        self.busted = False

    #Prints Player name and his actual money
    def __str__(self):
        return 'Player name:\t'+self.name+'\nTotal money:\t'+str(self.money)

    #Winning or losing money
    def win(self, wsum):
        self.money += int(wsum)
        self.busted = False

    #Display the remaining money
    def remaining_money(self):
        return self.money

    def betting(self, amount):
        if self.remaining_money()<amount:
            return False
        else:
            self.money -= amount
            self.bet = amount
            return True

    #Adding a card to his hand
    def add_cards(self,card):
        self.hand.add(card)

    #Prints his hand
    def printhand(self):
        print(self.hand)

    #Cleans his hand of cards
    def clearhand(self):
        del self.hand
        self.hand = Hand()
    
    def handvalue(self):
        return self.hand.handvalue()

    def isBusted(self):
        if self.hand.handbusted():
            self.busted = True
        return self.busted

#Defining the dealer class as a child of Player
class Dealer(Player):
    def printhand(self):
        print(self.hand.__str__(1))
    
    #The dealer have to grab cards until it reaches 17
    def plays(self):
        if self.hand.value >= 17:
            return False
        else:
            return True

#Welcome message
def printwelcome():
    print("*"*80)
    print("{0:<10}{1:^60}{2:>10}".format("*","Sir, this is a Casino", "*"))
    print("*"*80)
    print("{0:<10}{1:^60}{2:>10}".format("*","Black Jack vs the house","*"))
    print("{0:<10}{1:^60}{2:>10}".format("*","Good Luck !","*"))
    print("*"*80)

#End message 
def printend():
    print("*"*80)
    print("{0:<10}{1:^60}{2:>10}".format("*","Well, we hope you had fun at least","*"))
    print("{0:<10}{1:^60}{2:>10}".format("*","See you next time","*"))
    print("*"*80)

#Prints house win and clear hands
def housewins():
    print(f"{'*** House wins ***':^50}")
    player1.clearhand()
    dealer.clearhand()
#Prints hand won, adds the money to the player and clear hands
def playerwins():
    print(f"{'*** Hand won ***':^50}")
    player1.win(bet*2)
    player1.clearhand()
    dealer.clearhand()

#Main program
if __name__ == "__main__":

    #Initialize the deck and the dealer
    deck = Deck()
    deck.shuffle_cards()
    dealer = Dealer("Dealer", 90000)
    
    #Welcome message
    printwelcome()
    #Requesting user data
    money = ""
    maxplayers = [1,2,3]
    playerslist = []
    totalplayers = 0
    while totalplayers not in maxplayers:
        totalplayers = int(input("Number of players (Max 3): "))
        if totalplayers not in maxplayers:
            print("Sorry you must input a valid option")
    for p in range(totalplayers):
        name = input("Please insert your name: ")
        while money.isdigit() is False:
            money = input("How much money do you want to lose: ")
            print(" - NEXT VICTIM - ")
            if money.isdigit() is False:
                print("You must input a number")
                time.sleep(1)
        playerslist.append(Player(name, money))
        money = ""

    #Main game loop
    while len(playerslist) > 0:
        for p in playerslist:
            while True:
                clrscr()
                print(f"{'Welcome':^60}")
                print(p)
                print('How much do you want to bet? (0 for leaving the table)')
                #Check for integer input
                try:
                    bet = int(input('Bet: '))
                    if bet == 0:
                        playerslist.pop(0) #removes the player from the playerlist
                        break
                    elif p.betting(bet):
                        p.add_cards(deck.deal_one())
                        p.add_cards(deck.deal_one())
                        break
                    else:
                        print("Sorry, you don't have enough money")
                        time.sleep(1)
                        continue
                except:
                    print('You must input a number')
                    time.sleep(1)
                    continue
        #2 cards for the dealer
        dealer.add_cards(deck.deal_one())
        dealer.add_cards(deck.deal_one())
        while True:
            clrscr()
            for p in playerslist:
                print(p)
                print(f'Money in play: {p.bet:>10}')
                print("-"*20)
                print('PLAYER HAND')
                p.printhand()
                if p.isBusted():
                    print("*"*10 + "BUSTED :(")
                print("="*60)
                time.sleep(1)
            print(f'{" ":>60}DEALER HAND')
            dealer.printhand()
            if dealer.isBusted():
                print("Dealer Busted")
                for p in playerslist:
                    if not p.isBusted():
                        p.win(p.bet*2)
                    p.clearhand()
                dealer.clearhand()
                time.sleep(2)
                break
            #Determining the winner 
            # if player1.hand.handbusted() or dealer.hand.isblackjack(): 
            #     housewins()
            #     time.sleep(2)
            #     break
            # elif dealer.hand.handbusted() or player1.hand.isblackjack() or (player1.hand.isblackjack() and dealer.hand.isblackjack()):
            #     playerwins()
            #     time.sleep(2)
            #     break
            # elif pchoice == 1:
            #     if player1.handvalue()>dealer.handvalue():
            #         playerwins()
            #     else:
            #         housewins()
            #     time.sleep(2)
            #     break
            # else:
            try:
            #Choice to make for each player
                for p in playerslist:
                    if not p.isBusted():
                        print(f"PLAYER: {p.name}")
                        print('1. Stand')
                        print('2. Hit')
                        pchoice = int(input("Choice: "))
                        if pchoice == 2:
                            p.add_cards(deck.deal_one())
                        elif pchoice == 1:
                            #If the player choses to stand, the dealer keeps playing
                            if dealer.plays():
                                dealer.add_cards(deck.deal_one())
                            continue
                        else:
                            print('You must choose a valid option')
                            time.sleep(1)
                            continue
                # TODO #
                # Need to continue here what happens after there are no more plays available
                # Winner detection here
            except: 
                print('Sorry, you must choose a valid option')
                time.sleep(1)
                continue
printend()
time.sleep(3)
