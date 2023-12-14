import argparse

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Rocks():
  def __init__(self):
    self.mapSolidRocks = {}
    self.mapRollingRocks = {}
    self.maxY = 0
    self.maxX = 0

  def add_line(self, line, y):
    self.maxY = y
    for x, c in enumerate(line):
       if c == "O":
         if x > self.maxX:
           self.maxX = x
         self.mapRollingRocks[(x,y)] = c
       elif c == "#":
         self.mapSolidRocks[(x,y)] = c

  def __repr__(self):
    retVal = f"{self.mapRollingRocks} {self.mapSolidRocks}\n"
    for y in range(self.maxY + 1):
      for x in range(self.maxX + 1):
        if (x, y) in self.mapRollingRocks:
          retVal += "O"
        elif (x,y) in self.mapSolidRocks:
          retVal += "#"
        else:
          retVal += "."
      retVal += "\n"

    return retVal

  def move_rock(self, x, y):
    newY = y - 1
    if newY < 0:
      return y
    if (x,newY) in self.mapRollingRocks or (x,newY) in self.mapSolidRocks:
      print(f"Stopped at {x},{y}")
      return y
    return self.move_rock(x, y - 1)
    
  def tilt_north(self):
    y = 0

    for y in range(0, self.maxY + 1):
      for x in range(0, self.maxX + 1):
        rock = self.mapRollingRocks.get((x,y), None)
        if rock:
          newY = self.move_rock(x, y)
          print(f"Rock moved from {x},{y} to {newY}")
          if newY != y:
            del self.mapRollingRocks[(x,y)]
            self.mapRollingRocks[(x, newY)] = rock

  def score(self):
    total = 0
    y = 0
    print(self)
    for (x,y) in self.mapRollingRocks.keys():
      total += (self.maxY - y) + 1
    return total


if __name__ == "__main__":
  args = parseArgs()

  rocks = Rocks()
  for y, line in enumerate(open(args.infile, 'r')):
    rocks.add_line(line.strip(), y)
  print(rocks)
  rocks.tilt_north()
  print(f"Part 1: {rocks.score()}")