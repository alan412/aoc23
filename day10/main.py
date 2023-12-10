import argparse
import re
import sys

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Pipe:
  def __init__(self, x, y, char):
    self.x = x
    self.y = y
    self.char = char
  def connectsTo(self):
    match self.char:
      case '|':
        return [(self.x, self.y+1), (self.x, self.y-1)]
      case '-':
        return [(self.x-1, self.y), (self.x+1, self.y)]
      case 'L':
        return [(self.x, self.y-1), (self.x+1, self.y)]
      case 'J':
        return [(self.x, self.y-1), (self.x-1, self.y)]
      case '7':
        return [(self.x, self.y+1), (self.x-1, self.y)]
      case 'F':
        return [(self.x, self.y+1), (self.x+1, self.y)]
    return []

  def __repr__(self):
    return f"({self.x}, {self.y} {self.char})"


pipes = {}
startPipe = None
sys.setrecursionlimit(100_000)

# Recursion - 
def make_path(prevPipe, currPipe):
  path = [currPipe]
  for connection in currPipe.connectsTo():
    if connection in pipes and connection != (prevPipe.x, prevPipe.y):
      nextPipe = pipes[connection]
      if nextPipe == startPipe:
        path.append(nextPipe)
        return path
      new_path = make_path(currPipe, nextPipe)
      if new_path:
        path.append(nextPipe)
        for pipe in new_path:
          path.append(pipe)
  return path

def part1():
  print(f"Start: {startPipe}")
  for (x,y) in [(startPipe.x - 1, startPipe.y),
                (startPipe.x, startPipe.y - 1),
                (startPipe.x + 1, startPipe.y),
                (startPipe.x, startPipe.y + 1)]:
    if (x,y) in pipes:
      path = make_path(startPipe, pipes[x,y])
      if path:
        print(f"Path found: {path}, Length: {len(path) / 2}")
        return path

dots = []

maxSize = 0

def isInside(startX, y, dictPath):
  numLines = 0
  for x in range(startX):
    if (x,y) in dictPath:
      ch = pipes[(x,y)].char
      if ch in ['|','J','L']:  # Either needs or doesn't need S depending on input
        numLines += 1
  if numLines % 2:
    return True
  return False

def part2(path):
  dictPath = {}
  numInside = 0

  for pt in path:
    dictPath[(pt.x, pt.y)] = True

  tiles = []
  for x in range(maxSize):
    for y in range(maxSize):
      if (x,y) not in dictPath:
        tiles.append((x,y))

  for (x,y) in tiles:
    if isInside(x, y, dictPath):
      numInside += 1
      print(f"{x},{y} is Inside")

  print(f"Total: {numInside}")





if __name__ == "__main__":
  args = parseArgs()
  for y, line in enumerate(open(args.infile, 'r')):
     for x, ch in enumerate(line.strip()): 
        if ch != '.':
          pipes[(x,y)] = Pipe(x, y, ch)
        if ch == 'S':
          startPipe = pipes[(x,y)]
        if ch == '.':
          dots.append((x,y))
        if y > maxSize:
          maxSize = y
        if x > maxSize:
          maxSize = x

  path = part1()
  part2(path)
  