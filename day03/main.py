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
      self.box = {}
   
   def makeBox(self):
      for y in range((self.y - 1), (self.y + 2)):
        for x in range ((self.startX - 1), (self.endX + 2)):
           if y == self.y and (x >= self.startX) and (x <= self.endX):
               pass
           else:
               self.box[(y,x)] = True

   def nextTo(self, y, x):
      if len(self.box) == 0:
         self.makeBox()
      return (y,x) in self.box
      
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
            if c != '.' and c != '\n':
               self.symbols[(lineNum, x)] = c
            if startX != None:
               self.partNumbers.append(PartNumber(int(line[startX:x]), lineNum, startX, endX))
               startX = None
   
   def hasSymbolAround(self, part):      
      for y in range((part.y - 1), (part.y + 2)):
         for x in range ((part.startX - 1), (part.endX + 2)):
            if (y, x) in self.symbols:
               return True           
      return False
   
   def partsNext(self, y, x):
      parts = []
      for part in self.partNumbers:
         if part.nextTo(y, x):
            parts.append(part)
      return parts

   def aroundGears(self):
      total = 0
      for ((y, x), c) in self.symbols.items():
         if c == '*':
            print(f"{y} {x} {c}")
            parts = self.partsNext(y, x)
            print(parts)
            if len(parts) == 2:
              gearRatio = parts[0].val * parts[1].val
              total += gearRatio
      return total              



   

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

  print(f"Part1 Total:{total}")
  print(f"Part2 Total:{schematic.aroundGears()}")
        
