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
    # retVal = f"{self.mapRollingRocks} {self.mapSolidRocks}\n"
    retVal = ""
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
      return y
    return self.move_rock(x, y - 1)
    
  def tilt_north(self):
    y = 0

    for y in range(0, self.maxY + 1):
      for x in range(0, self.maxX + 1):
        rock = self.mapRollingRocks.get((x,y), None)
        if rock:
          newY = self.move_rock(x, y)
          
          if newY != y:
            del self.mapRollingRocks[(x,y)]
            self.mapRollingRocks[(x, newY)] = rock
  
  def rotate_ccw(self):
    newMapRollingRocks = {}
    newMapSolidRocks = {}
    for (x, y) in self.mapRollingRocks.keys():
      newMapRollingRocks[(self.maxY - y, x)] = self.mapRollingRocks[(x,y)]

    for (x, y) in self.mapSolidRocks.keys():
      newMapSolidRocks[(self.maxY - y, x)] = self.mapSolidRocks[(x,y)]

    newMaxX = self.maxY
    newMaxY = self.maxX
    
    self.maxX = newMaxX
    self.maxY = newMaxY

    self.mapRollingRocks = newMapRollingRocks
    self.mapSolidRocks = newMapSolidRocks
  
  def get_state(self):
    return tuple(self.mapRollingRocks.keys())
  
  def score(self):
    total = 0
    y = 0
    for (x,y) in self.mapRollingRocks.keys():
      total += (self.maxY - y) + 1
    return total

def part2(rocks):
  cycles = 1000000000
  states = dict() 
  loop_start = 0
  loop_size = 0
  for k in range(cycles):
    for i in range(4):
       rocks.tilt_north()
       rocks.rotate_ccw()
    cur_state = rocks.get_state()
    if cur_state in states:
      loop_size = k - states[cur_state]
      loop_start = states[cur_state]
      break
    else:
      states[cur_state] = k
  if loop_size:
    step = (cycles - (loop_start + 1)) % loop_size

    for m in range(step):
      for i in range(4):
        rocks.tilt_north()
        rocks.rotate_ccw()
  print(f"After {cycles}: \n{rocks}")
  print(f"Part 2: {rocks.score()}")

def part1(rocks):
  rocks.tilt_north()
  print(f"Part 1: {rocks.score()}")

if __name__ == "__main__":
  args = parseArgs()

  rocks = Rocks()
  for y, line in enumerate(open(args.infile, 'r')):
    rocks.add_line(line.strip(), y)
  # part1(rocks)
  part2(rocks)
  