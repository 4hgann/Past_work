from deck import deck
from player import player
import os

def draw(player,deck):
    return player.addCard(deck.draw())

def houseWin(house,user,bet):
    house.win(bet)
    user.loss(bet)

def userWin(house,user,bet):
    house.loss(bet)
    user.win(bet)

def compare(house,user,bet):
    #Player wins
    if(user.totalValue() > house.totalValue()):
        print('You win!')
        userWin(house,user,bet)
    else:
        print('Lose!')
        houseWin(house,user,bet)


def houseDraw(house,deck):
    print("The house started with: ",end="")
    house.printHand()
    input('(Enter to continue...)')
    while(house.totalValue() < 17):
        house.addCard(deck.draw())
        print("The house draws and their new hand is: ",end="")
        house.printHand()
        input('(Enter to continue...)')
    print('The house finishes drawing cards and stays')
    return

def getBuyIn():
    while True:
        try:
            money=input('How much money do you want to cash in? The dealer will begin with twice your amount\n')
            return int(money)
        except:
            print("That wasn't a valid amount to cash in, try again")
        os.system('cls||clear')

#Both house and user start with two cards
def setupHands(user,house,deck):
    house.addCard(deck.draw())
    house.addCard(deck.draw())
    user.addCard(deck.draw())
    user.addCard(deck.draw())

def getBet(user):
    while True:
        try:
            money=input('Insert your bet for this round\n')
            if(user.chips < int(money)):
                print('You can\'t bet more than you have!')
            elif(int(money)<1):
                print('You need to bet something!')
            else:
                return int(money)
        except:
            print("That wasn't a valid bet")

def hit(user,deck):
    draw(user,deck)
    print("Your hand is: ", end="")
    user.printHand()


def playRound(house,user):
    freshDeck = deck()
    setupHands(user,house,freshDeck)
    bet = getBet(user)
    pot=2*bet


    print('The pot is: $' +str(pot))

    #house.printHand() Uncomment to see the dealers entire hand
    house.printHouse()
    print("Your hand is: ", end="")
    user.printHand()
    choice = input('Do you want to Fold (F), Hit (H) or Stay(S)?\n').lower()
    while True:
        if(choice == 'h'):
            hit(user,freshDeck)
            if user.totalValue() > 21:
                print('Sorry, you went bust!')
                houseWin(house,user,bet)
                break
        elif(choice == 'f'):
            print('You back out.., why? You already bet?')
            houseWin(house,user,bet)
            break
        elif(choice == 's'):
            houseDraw(house,freshDeck)
            if(house.totalValue() > 21):
                print('The house went bust, you win!')
                userWin(house,user,bet)
                break
            else:
                compare(house,user, bet)
                break
        else:
            print('That wasn\'t an option, try again')

        choice = input('Do you want to Fold (F), Hit (H) or Stay(S)?\n').lower()
    return


if __name__ == "__main__":
    print('Welcome to Henry\'s Blackjack game! Note that the dealer stands on a soft 17')
    money=getBuyIn()
    house = player(money*2)
    user = player(money)
    playRound(house,user)
    while True:
        if(user.chips <= 0):
            print('You went broke')
            input('Press enter to close the game')
            break
        
        print('You currently have: $' + str(user.chips))
        choice = input('Do you want to play another round? Yes (Y) or No (N)')
        os.system('cls||clear')
        print('You currently have: $' + str(user.chips))
        if(choice.lower()=='no' or choice.lower()=='n'):
            print('You cashed out with $' + str(user.chips))
            break
        elif(choice.lower()=='yes' or choice.lower()=='y'):
            #Reset hands and play another round
            user.resetCards()
            house.resetCards()
            playRound(house,user)
        else:
            print('Sorry, that wasn\'t an option. Try again')

    print('Come back another time!')