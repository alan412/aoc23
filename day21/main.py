import argparse
import sys
import re
import heapq
from collections import namedtuple
from functools import cache
import numpy as np

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

Point = namedtuple("Point", "x y")

def add_pt(pt1, pt2):  # use tuple notation so we can add Points and reg tuples
  return Point(pt1[0] + pt2[0], pt1[1] + pt2[1])

class Grid():
  def __init__(self):
    self.squares = {}
    self.start = None
    self.maxX = 0
    self.maxY = 0
    self.positions = set()

  def add_line(self, line, y):
    for x, c in enumerate(line):
      if c == '#':
        self.squares[Point(x, y)] = '#'
      elif c == 'S':
        self.start = Point(x,y)
    self.maxX = x
    self.maxY = y

  def wrap(self, pt):
    return Point(pt.x % (self.maxX + 1), pt.y % (self.maxY + 1))  
  
  def step(self):
    newPos = set()
    for p in self.positions:
      for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pt = add_pt(p, d)
        if self.wrap(new_pt) not in self.squares:
          newPos.add(new_pt)
    self.positions = newPos

  def __repr__(self):
    return f"{self.start} {self.squares} {self.maxX} {self.maxY}"

def part1(grid):
  print(grid)
  num_times = 64
  for s in range(64 + 1):
    num_places = grid.num_places(grid.start, num_times)
  print(f"Pt1: After {num_times} times",len(num_places))

def part2(grid):
  print(grid)
  X,Y = [0,1,2], []
  target = (26501365 - 65) // 131
  grid.positions.clear()
  grid.positions.add(grid.start)
  for s in range(65 + 131*2 + 1):
    if s == 64:
      print(f"Part1: {len(grid.positions)}")
    if s%131 == 65:
      Y.append(len(grid.positions))
      print(f"{s} {len(grid.positions)}")
    grid.step()

  print("Solve polynomial after you get these 3")
  poly = np.rint(np.polynomial.polynomial.polyfit(X, Y, 2)).astype(int).tolist()
  print(poly, sum(poly[i]*target**i for i in range(3)))

if __name__ == "__main__":
  args = parseArgs()

  grid = Grid()
  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line, y)

  # part1(grid)
  part2(grid)