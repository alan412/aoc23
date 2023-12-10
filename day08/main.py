import argparse
import re
from math import lcm

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

def done(locations):
    for location in locations:
      if location[2] != 'Z':
          return False
    return True

def part2(directions, dictMaps):
  steps = 0
  locations = []
  stepsZ = []
  for location in dictMaps.keys():
    if location[2] == 'A':
        locations.append(location)
        stepsZ.append(0)

  while not done(locations):     
    nextDir = directions.get_next()
    if nextDir == 'L':        
        for i, location in enumerate(locations):
          locations[i] = dictMaps[location][0]
    else:
        for i, location in enumerate(locations):
          locations[i] = dictMaps[location][1]
    steps += 1
    for i, location in enumerate(locations):
       if location[2] == 'Z':
          if stepsZ[i] == 0:
             stepsZ[i] = steps
    
    totalMultiplied = 1
    for z in stepsZ:
       totalMultiplied *= z

    if totalMultiplied:
       print(f"Total by Multiplication: {totalMultiplied} {stepsZ}")   
       print(f"LCM: {lcm(*stepsZ)}")       

  print(f"Part 2 Num Steps: {steps}")

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
  # part1(directions, dictMaps)
  part2(directions, dictMaps)