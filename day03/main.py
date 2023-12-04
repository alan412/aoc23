import argparse
import re
from collections import namedtuple

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class PartNumber:
   def __init__(self, val, y, startX, endX):
      self.val = val;
      self.y = y
      self.startX = startX
      self.endX = endX
   def __repr__(self):
      return f"{self.val} {self.y}:{self.startX}-{self.endX}"

class Schematic:
   def __init__(self):
      self.symbols = {}
      self.partNumbers = []
      self.lines = []
   def addLine(self, line):
      lineNum = len(self.lines)
      self.lines.append(line)
      startX = None
      endX = 0
      for x, c in enumerate(line):
         if c.isdigit():
            if startX == None:
               startX = x
            endX = x
         else:
            if c != '.':
               self.symbols[(lineNum, x)] = c
            if startX != None:
               self.partNumbers.append(PartNumber(int(line[startX:endX + 1]), lineNum, startX, endX))
               startX = None
   
   def hasSymbolAround(self, part):      
      for y in range((part.y - 1), (part.y + 2)):
         for x in range ((part.startX - 1), (part.endX + 2)):
            if (y, x) in self.symbols:
               print(f" {y},{x} {self.symbols[(y,x)]}")
               return True
  
      return False
   

if __name__ == "__main__":
  args = parseArgs()
  data = []
  schematic = Schematic()

  for line in open(args.infile, 'r'):
     schematic.addLine(line)
  
  total = 0
  for part in schematic.partNumbers:
     if schematic.hasSymbolAround(part):
        total += part.val
        print(f"Part: {part} Total: {total}")
     else:
        print(f"Part - no symbol: {part} Total: {total}")

  print(f"Total:{total}")
        
