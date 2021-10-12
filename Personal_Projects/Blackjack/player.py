from card import *

class player:
    def __init__(self,money):
        self.cards = []
        self.chips = money

    def totalValue(self):
        value=0
        aces=[]
        #Get the value without the aces included
        for i in range(len(self.cards)):
            if(self.cards[i].value != 1):
                #Cards only worth up to 10
                value+=min(self.cards[i].value,10)
            else:
                aces.append(i)

        for i in range(len(aces)):
            if(value+(11*(len(aces)-i))>21):
                value+=1
            else:
                value+=11
            

        return value

    def addCard(self, card):
        self.cards.append(card)
        return
    
    def resetCards(self):
        self.cards = []
        return

    #Format of printing is "Your hand is: Ace of Spades & 10 of hearts"
    def printHand(self):
        for i in range(len(self.cards)):
            if(i == len(self.cards)-1 and i != 0):
                print(" & ",end="")
            elif(i > 0):
                print(", ",end="")

            print(self.cards[i].getValue() + " of " + self.cards[i].getSuit(),end="")


        print("")
        return
    
    def printHouse(self):
        print("The house has a ", end="")
        print((self.cards[0]).getValue() + " of " + self.cards[0].getSuit(),end="")
        print(". Their other card is hidden!")
    
    def win(self,money):
        self.chips += money
    
    def loss(self,money):
        self.chips -= money
