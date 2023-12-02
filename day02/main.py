import argparse
import re
from collections import namedtuple

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

Pick = namedtuple("Pick", ["red", "green", "blue"])

class Pick:
   def __init__(self, red, green, blue):
      self.red = red
      self.green = green
      self.blue = blue

class Game:     
   def __init__(self, line):
      (before, after) = line.split(':')
      self.gameNum = int(before[5:])
      self.picks = []
      picks = after.split(';')
      for pick in picks:
         blue = 0
         red = 0
         green = 0

         found = re.search("(\d+) blue", pick)
         if found:
            blue += int(found.group(1))
         found = re.search("(\d+) red", pick)
         if found:
            red += int(found.group(1))
         found = re.search("(\d+) green", pick)            
         if found:
            green += int(found.group(1))
         self.picks.append(Pick(red, green, blue))

   def possible(self, red, green, blue):
     for pick in self.picks:
        # print(f"{red} {green} {blue}:  {pick.red} {pick.blue} {pick.green}")
        if (red < pick.red) or (green < pick.green) or (blue < pick.blue):
           return False
     return True
   def power(self):
     red = 0
     green = 0
     blue = 0
     for pick in self.picks:
        red = max(red, pick.red)
        green = max(green, pick.green)
        blue = max(blue, pick.blue)
    
     return red * green * blue
           

def part2(data):
  total = 0
  for item in data:
     total += item.power()
  print(f"Part2 Total: {total}")
  
def part1(data):
  total = 0
  for item in data:
     if item.possible(12, 13, 14):
        print(f"Game {item.gameNum} possible")
        total += item.gameNum
  print(f"Total: {total}")

if __name__ == "__main__":
  args = parseArgs()
  data = []
  for line in open(args.infile, 'r'):
     data.append(Game(line))
  
  part1(data)
  part2(data)