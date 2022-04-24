"""
Milestone Project 2 - Blackjack Game
In this milestone project you will be creating a Complete BlackJack Card Game in Python.

Here are the requirements:

* You need to create a simple text-based [BlackJack](https://en.wikipedia.org/wiki/Blackjack) game
* The game needs to have one player versus an automated dealer.
* The player can stand or hit.
* The player must be able to pick their betting amount.
* You need to keep track of the player's total money.
* You need to alert the player of wins, losses, or busts, etc...

And most importantly:

You must use OOP and classes in some portion of your game.
You can not just use functions in your game.
Use classes to help you define the Deck and the Player's hand.
There are many right ways to do this, so explore it well!

Feel free to expand this game. Try including multiple players.
Try adding in Double-Down and card splits!
"""

import random
import time
import os

def clrscr():
    """Method for clearing the screen"""
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

SUITS = ('Hearts','Diamonds','Spades','Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
        'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Hand:
    """
        A card hand class to playing BlacKJack
        Methods for printing, checking hand value, adding cards to the hand
        checking if the hand is busted or if it's a BlackJack
    """
    def __init__(self):
        """Initialises the hand with an empty set of cards and a value of 0"""
        self.cards = []
        self.value = 0

    def __str__(self, align=0):
        """
            Printing the cards in the hand and the total value
            If it's a player it aligns to the left, and right for the dealer
            Arguments:
                        0 (Default) : aligns the elements to the left
                        1           : aligns the elements to the right

        """
        output = ""
        if align == 0:
            for card in self.cards:
                output += card.ranksuit() + '\n'
            output += f'\tTotal Hand: {self.value}'
        else:
            for card in self.cards:
                output += f'{" ":>60}' + card.ranksuit() + '\n'
            output += f'{" ":>50} {self.value} :Total Hand'
        return output

    def handvalue(self):
        """Returns the value of the hand"""
        return self.value

    def handbusted(self):
        """Returns if the hand is busted"""
        if self.value > 21:
            return True
        else:
            return False

    def add(self, card):
        """Add a card to the hand and calculate at the same time the total hand value"""
        self.cards.append(card)
        if self.value > 10 and card.value == 11:
            self.value += 1
        else:
            self.value += card.value

    def isblackjack(self):
        """Determines if the hand is a BlackJack"""
        if len(self.cards)==2 and self.value==21:
            return True
        else:
            return False

    def clear_hand(self):
        """
            Method to clearing the hand
        """
        while self.cards:
            self.cards.pop()
        del self.cards
        self.cards=[]
        self.value=0

class Card:
    """
        Gaming card class.
        Initialises the class with all the possibles combinations of suit
        and rank, and assigns a value to each one by the rules of
        BlackJack
    """
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]

    def ranksuit(self):
        """Method for printing the rank and suit"""
        return f'{self.rank} of {self.suit}'

class Deck:
    """
        Creates a deck, with methods to shuffle cards
        and deal one to the player
    """
    def __init__(self):
        """For each suit and rank, create a card object"""
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))

    def shuffle_cards(self):
        """Imports random for shuffling the deck"""
        random.shuffle(self.cards)

    def deal_one(self):
        """Deals one to the player and removes it from the deck"""
        return self.cards.pop()


class Player:
    """
        A Player class with some methods to play Blackjack
    """
    #Initialises the player with an empty hand and an empty bet
    def __init__(self, p_name, p_money):
        self.name = p_name
        self.money = int(p_money)
        self.hand = Hand()
        self.busted = False
        self.bet = 0

    def __str__(self):
        """Prints Player name and his actual money"""
        return 'Player name:\t'+self.name \
                +'\nTotal money:\t'+str(self.money)

    def win(self):
        """
            If the players wins, we add the wsum to his actual money
            and set the busted status to false
        """
        self.money += self.bet*2

    def tie(self):
        """ If the player ties with the house """
        self.money += self.bet

    def remaining_money(self):
        """ Returns the actual player money """
        return self.money

    def betting(self, amount):
        """
            If the player is able to bet, make change the class attribute and remove that from
            his total ammount
            Argument:
                    amount: amount of money trying to bet
        """
        if self.remaining_money()<amount:
            return False
        else:
            self.money -= amount
            self.bet = amount
            return True

    def add_cards(self,card):
        """Adding a card to his hand"""
        self.hand.add(card)

    def printhand(self):
        """Prints his hand"""
        print(self.hand)

    def clearhand(self):
        """
            Cleans his hand of cards and sets the busted
            status to False
        """
        self.hand.clear_hand()
        self.busted=False

    def handvalue(self):
        """Returns the player hand value"""
        return self.hand.handvalue()
    def is_busted(self):
        """
            Calls the hand method to check if the player is busted
            and returns the busted status
        """
        if self.hand.handbusted():
            self.busted = True
        return self.busted

class Dealer(Player):
    """
        Dealer class child of Player. Inherits the same attibutes
        but adds a method that returns True if the dealer is
        able to keep playing the hand
    """
    def printhand(self):
        """
            Prints the dealer hand and passes 1 as parameter to the
            print function to make it align to the right
        """
        print(self.hand.__str__(1))

    def plays(self):
        """The dealer have to grab cards until it reaches 17"""
        if self.hand.value >= 17:
            return False
        else:
            return True

class Round:
    """
        The playing round. Keeps track of how many players are left in the
        round.
        Takes the game dealer as parameter. The dealer always plays
        If the player choices to stand, he gets removed for the
        'playing' round and the round ends when there are no more
        players left
    """
    def __init__(self, game_dealer):
        self.player = []
        self.dealer = game_dealer

    def add_player(self, round_player):
        """Adds the player that invoked the method to the 'playing' players"""
        self.player.append(round_player)

    def remove_player(self, round_player):
        """
        Removes the round_player for the round and clears his hand
        """
        self.player.remove(round_player)

    def has_players(self):
        """Returns True if the round still has players playing in it"""
        if self.player:
            return True
        else:
            return False

    def player_list(self):
        """Returns a list with the players remaining"""
        return self.player

    def clear_round(self,players_list):
        """
            Clears each player, the player list and dealer
            Argurments:
                player_list: a list containing the players that will
                            have his hands cleared
        """
        for round_player in players_list:
            round_player.clearhand()
            del round_player
        del self.player
        dealer.clearhand()
        self.player = []

############################ Printing Functions ###################################
#Welcome message
def printwelcome():
    """Prints the welcome message"""
    print("*"*80)
    print("{0:<10}{1:^60}{2:>10}".format("*","Sir, this is a Casino", "*"))
    print("*"*80)
    print("{0:<10}{1:^60}{2:>10}".format("*","Black Jack vs the house","*"))
    print("{0:<10}{1:^60}{2:>10}".format("*","Good Luck !","*"))
    print("*"*80)

#End message
def printend():
    """Print the ending message where there are no players in the casino"""
    print("*"*80)
    print("{0:<10}{1:^60}{2:>10}".format("*","Well, we hope you had fun at least","*"))
    print("{0:<10}{1:^60}{2:>10}".format("*","See you next time","*"))
    print("*"*80)



################# MAIN PROGRAM
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
        try:
            totalplayers = int(input("Number of players (Max 3): "))
            if totalplayers not in maxplayers:
                print("Sorry you must input a valid option")
        except ValueError:
            print("Sorry you must input a valid option")

    for p in range(totalplayers):
        name = input("Please insert your name: ")
        while money.isdigit() is False:
            money = input("How much money do you want to lose: ")
            if money.isdigit() is False:
                print("You must input a number")
                time.sleep(1)
        print(" - NEXT VICTIM - ")
        playerslist.append(Player(name, money))
        money = ""

    ### MAIN GAME LOOP
    while playerslist:
        #Start the round
        game_round=Round(dealer)
        #for player in playerslist:
        ##Need to use a index, because in the for loop, when I delete the
        #player element with playerlist.remove(player), the index gets
        #reduced by one and the second element gets in the first position
        #so the loop exits immediately when there are just 2 elements
        #and the first one leaves the table
        i=0
        while i < len(playerslist):
            while True:
            #Loop for checking value types
                clrscr()
                print(f"{'Welcome':^60}")
                print(playerslist[i])
                print('How much do you want to bet?\
                        (0 for leaving the table)')
                #Check for integer input
                try:
                    bet=int(input("BET: "))
                    if bet==0:
                        #Removes the player for the player pool
                        playerslist.pop(i)
                        #Move the index backwards for accounting
                        #the lost player
                        i-=1
                        break
                    else:
                        if playerslist[i].betting(bet):
                            #If the player is able to bet, add 2 cards
                            #to his hand and add the player to the
                            #round
                            playerslist[i].add_cards(deck.deal_one())
                            playerslist[i].add_cards(deck.deal_one())
                            game_round.add_player(playerslist[i])
                            break
                        else:
                            print("Sorry, you don't have enough money")
                            time.sleep(1)
                            continue
                except (TypeError, ValueError):
                    #If the input it's not a number, redo the loop
                    #for the current player
                    print('You must input a number')
                    time.sleep(1)
                    continue
            i+=1

        if game_round.has_players():
            #2 cards for the dealer if there are players in the round
            #If there aren't any players in the casino, no need for
            #adding the cards to the dealer
            dealer.add_cards(deck.deal_one())
            dealer.add_cards(deck.deal_one())

        #While there are players in the round, keep the hit
        #and stand loop
        times_played = 0
        while game_round.has_players():
            if times_played > 0:
            #Ask for input after the first round
                #for player in game_round.player_list():
                #Same thing, need to use and index because of the for loop
                #limitations when deleting items
                i=0
                round_players=game_round.player_list()
                while i<len(round_players):
                    if round_players[i].is_busted() \
                        or round_players[i].hand.isblackjack():
                        #Remove the current player for the round if
                        #he is busted or has a blackjack
                        game_round.remove_player(round_players[i])

                    else:
                        #Ask for user input whether Stand or Hit
                        while True:
                            #Loop for checking for value type
                            try:
                                print(f"PLAYER: {round_players[i].name}")
                                print('1. Stand')
                                print('2. Hit')
                                pchoice = int(input("Choice: "))
                                if pchoice==2:
                                    #If the player choses to hit, add a card
                                    round_players[i].add_cards(deck.deal_one())
                                    i+=1 #move the index forward
                                    break
                                elif pchoice==1:
                                    #Remove the current player from the round
                                    game_round.remove_player(round_players[i])
                                    break
                            except ValueError():
                            #Wrong selection
                                print('You must choose a valid option')
                                time.sleep(1)
                #The dealer takes 1 card if he is able to play
                #after all the player have chosen
                if dealer.plays():
                    dealer.add_cards(deck.deal_one())

            #Choice step has ended, print all the players
            #and dealer hand
            clrscr()
            for player in playerslist:
                #Players hands
                print(player)
                print(f'Money in play: {player.bet:>10}')
                print("-"*20)
                print('PLAYER HAND')
                player.printhand()
                print("="*60)
                #time.sleep(1)

            #Show the dealer hand
            print(f'{" ":>60}DEALER HAND')
            dealer.printhand()

            #Evaluate if the dealer is either busted or
            #has a blackjack
            if dealer.is_busted() or dealer.hand.isblackjack():
                #time.sleep(1)
                break
            #increase the times the players have played the round
            times_played+=1

        ### NO MORE PLAYERS IN THE ROUND
        #If the dealer can still plays, keeps adding cards
        if playerslist:
            #If there are players in the casino, print hands
            clrscr()
            while dealer.plays():
                #The dealer keep adding cards if he can still play
                dealer.add_cards(deck.deal_one())
            #Print all hands again and the end of round
            for player in playerslist:
                print(player)
                print(f'Money in play: {player.bet:>5}')
                print("-"*20)
                print('PLAYER HAND')
                player.printhand()
                if player.is_busted():
                    print(f"{'*'*25} BUSTED {'*'*25}")
                elif player.hand.isblackjack():
                    print(f"{'*'*25} BLACKJACK {'*'*25}")
                else:
                    print("="*60)
                time.sleep(1)
            print(f'{" ":>60}DEALER HAND')
            dealer.printhand()
            print("*"*20)
            print("End of the Round")
            print("*"*20)
            if dealer.is_busted():
                #If the dealer is busted, everyone that are not busted
                #will win
                print("DEALER BUSTED")
                for player in playerslist:
                    if not player.is_busted():
                        print(f"Player: {player.name} WINS {player.bet}")
                        player.win()
                    else:
                        print(f"Player: {player.name} LOSSES {player.bet}")
            elif dealer.hand.isblackjack():
                #if the dealer has blackjack, everyone that has a
                #blackjack will tie with the house
                print("DEALER BLACKJACK")
                for player in playerslist:
                    if player.hand.isblackjack():
                        print(f"Player: {player.name}\
                            TIES WITH THE HOUSE {player.bet}")
                        player.tie()
                    else:
                        print(f"Player: {player.name} LOSSES {player.bet}")
            else:
                #If the dealer is not busted and doesn't have a blackjack
                #compare each player hand with the dealer
                for player in playerslist:
                    if player.handvalue()>dealer.handvalue() and (not player.is_busted()):
                        print(f"Player: {player.name} WINS {player.bet}")
                        player.win()
                    elif player.handvalue()>dealer.handvalue()\
                                        and (not player.is_busted()):
                        print(f"Player: {player.name}\
                            TIES WITH THE HOUSE {player.bet}")
                        player.win()
                    else:
                        print(f"Player: {player.name} LOSSES {player.bet}")
            #Wait for user input before continue
            input("Press ENTER to continue")
            game_round.clear_round(playerslist)
        else:
            printend()
time.sleep(3)
