import argparse
from enum import Enum
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class HandType(Enum):
   FIVE_OF_A_KIND = 7
   FOUR_OF_A_KIND = 6
   FULL_HOUSE = 5
   THREE_OF_A_KIND = 4
   TWO_PAIR = 3
   ONE_PAIR = 2
   HIGH_CARD = 1

   def __lt__(self, other):
      if self.__class__ is other.__class__:
         print(f"{self} {other}")
         return self.value < other.value
      return NotImplemented

valMap = {'A' : 14, 'K' : 13, 'Q' : 12, 'J' : 11, 'T' : 10, '9' : 9, '8' : 8, '7' : 7, '6' : 6,
          '5' : 5, '4' : 4, '3' : 3, '2' : 2, '1' : 1}
class Hand:
   def __init__(self, line):
      (self.hand, bid) = line.strip().split(" ")
      self.bid = int(bid)
      dictCards = {}
      for c in self.hand:                  
         dictCards[c] = dictCards.get(c, 0) + 1
      sorted_cards = sorted(dictCards.items(), key=lambda x:x[1], reverse = True)
      self.handType = HandType.HIGH_CARD
      if sorted_cards[0][1] == 5:
         self.handType = HandType.FIVE_OF_A_KIND
      elif sorted_cards[0][1] == 4:
         self.handType = HandType.FOUR_OF_A_KIND
      elif sorted_cards[0][1] == 3:
         if sorted_cards[1][1] == 2:
            self.handType = HandType.FULL_HOUSE
         else:
            self.handType = HandType.THREE_OF_A_KIND
      elif sorted_cards[0][1] == 2:
         if sorted_cards[1][1] == 2:
            self.handType = HandType.TWO_PAIR
         else:
            self.handType = HandType.ONE_PAIR
   def __lt__(self, other):
      if self.__class__ is other.__class__:
         if self.handType == other.handType:
            # This needs the code here to look at each
            for i in range(5):
               if self.hand[i] == other.hand[i]:
                  continue
               else:
                  return valMap[self.hand[i]] < valMap[other.hand[i]] 
         else:
           return self.handType < other.handType
      return NotImplemented
      
   def __repr__(self):
      return f"{self.hand} {self.handType} {self.bid}"
def part1(data):
   sortedData = sorted(data)
   total = 0
   for rank, hand in enumerate(sortedData):
      total += (rank + 1) * hand.bid  
      print(f"Rank: {rank} Hand:{hand} ")
      
   print(f"Total: {total}")

if __name__ == "__main__":
  args = parseArgs()
  data = []
  for line in open(args.infile, 'r'):
     data.append(Hand(line))
  
  print(data)
  part1(data)
