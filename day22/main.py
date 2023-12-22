import argparse
import sys
import re
import heapq
from collections import namedtuple
from functools import cache, total_ordering
from dataclasses import dataclass
import numpy as np

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

@dataclass()
class Point():
  x: int
  y: int
  z: int

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y, self.z - other.z)
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y, self.z + other.z)
  def __lt__(self, other):
    if self.z == other.z:
      if self.y == other.y:
        return self.x < other.x
      return self.y < other.y
    return self.z == other.z
  
@total_ordering
class Brick():
  def __init__(self, start_pt, end_pt):
    self.origin = start_pt
    self.end_pt = end_pt
    # self.size = end_pt - start_pt
    # assert self.size.x >= 0 and self.size.y >= 0 and self.size.z >= 0
  def drop_z(self, z_change):
    self.origin.z -= z_change
    self.end_pt.z -= z_change
  def intersect(self, other):
    if other.origin.z > self.end_pt.z or other.end_pt.z < self.origin.z:
      return False
    if other.origin.x > self.end_pt.x or other.end_pt.x < self.origin.x:
      return False
    if other.origin.y > self.end_pt.y or other.end_pt.y < self.origin.y:
      return False
    return True 
  def rests_on(self, other):
    if self.origin.z != other.origin.z + 1:
      print(f"1 - No Rest on {self} {other}")
      return False
    # otherwise, is any of the x and y the same
    if self.origin.x > other.end_pt.x or self.end_pt.x < other.origin.x:
      print(f"2 - No Rest on {self} {other}")
      return False
    if self.origin.y > other.end_pt.y or self.end_pt.y < other.origin.y:
      print(f"3 - No Rest on {self} {other}")
      return False
    return True

  def __lt__(self, other):
    return self.origin < other.origin
  def __eq__(self, other):
    return self.origin == other.origin
  def __repr__(self):
    return f"{self.origin}->{self.end_pt}"

class Grid():
  def __init__(self):
    self.bricks = []
  def add_line(self, line):
    r = re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)
    self.bricks.append(Brick(Point(int(r.group(1)), int(r.group(2)), int(r.group(3))), 
                      Point(int(r.group(4)), int(r.group(5)), int(r.group(6)))))
  def sort(self):
    self.bricks = sorted(self.bricks)
  
  def can_drop(self, brick, z):
    if brick.origin.z <= 1:
      return False
    newBrick = Brick(Point(brick.origin.x, brick.origin.y, brick.origin.z - z),
                     Point(brick.end_pt.x, brick.end_pt.y, brick.end_pt.z - z))
    for b in self.bricks:
      if b == brick:
        continue
      if b.intersect(newBrick):
        return False
    return True
  
  def fall(self):
    self.sort()
    print(self)
    for brick in self.bricks:
      while self.can_drop(brick, 1):
        brick.drop_z(1)

  def __repr__(self):
    return f"{self.bricks}"
  
  def how_many_can_be_removed(self):
    aboveBricks = []
    total = 0
    for brick in reversed(self.bricks):
      print(f"Looking at brick: {brick}")
      can_be_removed = True
      for brick2 in aboveBricks:
        if brick2.rests_on(brick):
          print(f"+++ {brick2}")
          can_be_removed = False
          break
      if can_be_removed:
        total += 1
        print(f"--")
      aboveBricks.append(brick)
    return total
def part1(grid):
  grid.fall()
  print("--- After fall ---")
  print(grid)
  grid.sort()
  print(f"Part 1: {grid.how_many_can_be_removed()}")

if __name__ == "__main__":
  args = parseArgs()

  grid = Grid()
  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line)

  part1(grid)
  # part2(grid)