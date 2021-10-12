class card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit

  def getValue(self):
      if self.value == 1:
          return "Ace"
      elif self.value == 11:
          return "Jack"
      elif self.value == 12:
          return "Queen"
      elif self.value == 13:
          return "King"
      else:
          return str(self.value)
    
  def getSuit(self):
    if self.suit==1:
        return "Spades"
    elif self.suit==2:
        return "Hearts"
    elif self.suit==3:
        return "Clubs"
    else:
        return "Diamonds"