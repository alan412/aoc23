import argparse
import re
from collections import namedtuple

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Card:     
   def __init__(self, line):
      (before, after) = line.split(':')
      self.cardNum = int(before[5:])
      (winning, have) = after.split('|')
      self.winnerList = [int(x) for x in winning.split(' ') if x]
      self.haveList = [int(x) for x in have.split(' ') if x]
      self.numMatches = self.calcNumMatches()

   def calcNumMatches(self):
    numMatches = 0
    for winner in self.winnerList:
       if winner in self.haveList:
          numMatches += 1
    return numMatches
         
   def score(self):
    if self.numMatches == 0:
      return 0
    result = 1
    for x in range(self.numMatches - 1):
     result *= 2
    return result

def part1(cards):
  total = 0
  for card in cards:
    result = card.score()
    total += result
    print(f"{card.cardNum} = {result}")
  print(f"Total: {total}")

def part2(cards):
  cardDict = {}
  for card in cards:
    cardDict[card.cardNum] = 1
  
  for card in cards:
    addlCards = cardDict[card.cardNum]
    for i in range(card.numMatches):
      cardDict[card.cardNum + i + 1] += addlCards
    print(cardDict)

  totalCards = 0
  for numberCards in cardDict.values():
    totalCards += numberCards

  print(f"Total: {totalCards}")

if __name__ == "__main__":
  args = parseArgs()
  data = []
  for line in open(args.infile, 'r'):
     data.append(Card(line))
  
  part1(data)
  part2(data)
