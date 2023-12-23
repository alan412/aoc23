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
      self.squares[Point(x,y)] = c
    self.maxX = x
    self.maxY = y 

  def is_valid(self, pt, d):
    allowed = {'>':(1,0), '<':(-1,0), 'v':(0,1), '^':(0,-1)}
    if pt.x < 0 or pt.x > self.maxX:
      return False
    if pt.y < 0 or pt.y > self.maxY:
      return False
    if self.squares[pt] == '#':
      return False
    elif self.squares[pt] == '.':
      return True
    elif d == allowed[self.squares[pt]]:
      return True
    return False

  def find_path(self, pt, visited_squares):
    dirs = [(0,-1), (0,1), (-1,0),(1,0)]
    paths = []

    if pt == self.dest:
      return visited_squares

    visited_squares.append(pt)

    for d in dirs:
      new_point = add_pt(pt, d)
      if self.is_valid(new_point, d) and not new_point in visited_squares:
        new_path = self.find_path(new_point, [sq for sq in visited_squares])
        if new_path:
          paths.append(new_path)
    # which path is longest
    longest = 0
    longestPath = None
    for path in paths:
      if path and len(path) > longest:
        longestPath = path
        longest = len(path)
        
    return longestPath

  def wrap(self, pt):
    return Point(pt.x % (self.maxX + 1), pt.y % (self.maxY + 1))  

  def find_start(self):
    return self.find_first(0)

  def find_dest(self):
    return self.find_first(self.maxY)

  def find_first(self, y):
    for x in range(self.maxX):
      if self.squares[(x, y)] == '.':
         return Point(x, y)
    return None
  def __repr__(self):
    return f"{self.squares} {self.maxX} {self.maxY}"

def part1(grid):
  start = grid.find_start()
  grid.dest = grid.find_dest()

  path = grid.find_path(start, [])
  print(f"Part 1: {len(path)}")

sys.setrecursionlimit(100_000)

if __name__ == "__main__":
  args = parseArgs()

  grid = Grid()
  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line, y)

  part1(grid)
  # part2(grid)