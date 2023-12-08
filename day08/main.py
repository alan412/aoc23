import argparse
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Directions:
   def __init__(self, line):
      self.index = 0
      self.line = line.strip()
   def get_next(self):
      result = self.line[self.index]
      self.index += 1
      if self.index >= len(self.line):
         self.index = 0
      return result

def part1(directions, dictMaps):
  steps = 0
  location = 'AAA'
  while location != 'ZZZ':
     nextDir = directions.get_next()
     print(f"{location} {nextDir}")
     if nextDir == 'L':
        location = dictMaps[location][0]
     else:
        location = dictMaps[location][1]
     steps += 1
  print(f"Num Steps: {steps}")

if __name__ == "__main__":
  args = parseArgs()
  dictMaps = {}
  directions = None
  for line in open(args.infile, 'r'):
     if directions:
          m = re.match(r'(\w+) = \((\w+), (\w+)', line)
          if m:
            dictMaps[m.group(1)] = (m.group(2), m.group(3))
     else:        
        directions = Directions(line)
  print(dictMaps)
  print(directions)
  part1(directions, dictMaps)