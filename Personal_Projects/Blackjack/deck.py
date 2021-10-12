from card import *
import random

class deck:
    #Establishes a fresh deck in constructor, excluding jokers
    def __init__(self):
        self.cards = []
        #1-Ace, 11-13 - JQK
        for i in range(1,14):
            #Represents each suit
            for j in range(1,5):
                self.cards.append(card(i,j))

    def draw(self):
        #Fetch a random card in the current deck
        index = random.randint(0,len(self.cards)-1)
        #Pop this from the deck and return the card for use
        return self.cards.pop(index)
    
    #Resets the deck when the hand is over
    def showDeck(self):
        for i in range(len(self.cards)):
            print(str(self.cards[i].value)+str(self.cards[i].suit))
        return