import argparse
import sys
import re
from enum import Enum

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Space():
  def __init__(self, c):
    self.mirrorType = c
    self.energized = False
  def __repr__(self):
    return self.mirrorType

class Dir(Enum):
  UP = 1
  DOWN = 2
  LEFT = 3
  RIGHT = 4

class Beam():
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.direction = direction
  def __repr__(self):
    return f"{self.x},{self.y} {self.direction}"

  def move(self, space):
    newDir = self.direction
    match space.mirrorType:
      case '|':
        match self.direction:
          case Dir.LEFT | Dir.RIGHT:
            return [Beam(self.x, self.y - 1, Dir.UP), Beam(self.x, self.y + 1, Dir.DOWN)]
      case '-':
        match self.direction:
          case Dir.UP | Dir.DOWN:
            return [Beam(self.x -1, self.y, Dir.LEFT), Beam(self.x + 1, self.y, Dir.RIGHT)]
      case '/':
        match self.direction:
          case Dir.LEFT:
            newDir = Dir.DOWN
          case Dir.DOWN:
            newDir = Dir.LEFT
          case Dir.RIGHT:
            newDir = Dir.UP
          case Dir.UP:
            newDir = Dir.RIGHT
      case '\\':
        match self.direction:
          case Dir.LEFT:
            newDir = Dir.UP
          case Dir.UP:
            newDir = Dir.LEFT
          case Dir.RIGHT:
            newDir = Dir.DOWN
          case Dir.DOWN:
            newDir = Dir.RIGHT       
    match newDir:
      case Dir.UP:
        return [Beam(self.x, self.y - 1, newDir)]
      case Dir.DOWN:
        return [Beam(self.x, self.y + 1, newDir)]
      case Dir.LEFT:
        return [Beam(self.x - 1, self.y, newDir)]
      case Dir.RIGHT:
        return [Beam(self.x + 1, self.y, newDir)]
  
class Grid():
  def __init__(self):
    self.spaces = {}
    self.alreadyBeen = {}
    self.maxY = 0
    self.maxX = 0

  def add_line(self, line, y):
    for x, c in enumerate(line):
      self.spaces[(x,y)] = Space(c)
    self.maxX = len(line)
    self.maxY = y
  
  def laser_step(self, beam):
    seen = self.alreadyBeen.get((beam.x, beam.y, beam.direction), None)
    if seen:
      return
    self.alreadyBeen[(beam.x, beam.y, beam.direction)] = True
    space = self.spaces.get((beam.x, beam.y), None)
    if space:
      space.energized = True
      listBeams = beam.move(space)
      # print(f"{beam} -> {listBeams}")
      for beam in listBeams:
        self.laser_step(beam)
  
  def part1(self):
    self.laser_step(Beam(0, 0, Dir.RIGHT))

    num_energized = 0
    display = ""
    num_spots = 0
    for y in range(self.maxY + 1):
      for x in range(self.maxX):
        space = self.spaces.get((x,y), None)
        if space:
          if space.energized:
            num_energized += 1
            display += "#"
          else:
            display += "."
      display += "\n"

    # print(display)

    print(f"Energized: {num_energized}")



sys.setrecursionlimit(100_000)

if __name__ == "__main__":
  args = parseArgs()
  grid = Grid()

  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line, y)
  grid.part1()