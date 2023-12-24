import argparse
import sys
import re
import heapq
from collections import namedtuple
from functools import cache, total_ordering
from dataclasses import dataclass
import numpy as np
import z3

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

@dataclass
class Coord():
  x : int
  y : int
  z : int
  def __add__(self, other):
    return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

class Hail():
  def __init__(self, line):
    (position_str, velocity_str) = line.split("@")
    position_list = [int(num) for num in position_str.split(",")]
    velocity_list = [int(num) for num in velocity_str.split(",")]
    self.position = Coord(position_list[0], position_list[1], position_list[2])
    self.velocity = Coord(velocity_list[0], velocity_list[1], velocity_list[2])
    self.p2 = self.position + self.velocity

    self.a = self.p2.y - self.position.y
    self.b = self.position.x - self.p2.x
    self.c = self.a * (self.position.x) + self.b * (self.position.y)

  def __repr__(self):
    return f"P: {self.position}, V: {self.velocity}"
  def intersect(self, other, min_val, max_val):
    # determinant
    det = self.a * other.b - other.a * self.b
    
    # parallel line
    if det == 0:
      return False
    
    x = ((other.b * self.c) - (self.b * other.c)) / det
    y = ((self.a * other.c) - (other.a * self.c)) / det

    # is it outside the test area
    if x < min_val or x > max_val or y < min_val or y > max_val:
      return False
    
    # is it in the past?
    # newX = posX + velX * time
    # newX - posX = velX * time
    # (newX - posX) / velX = time
    if ((x - self.position.x) / self.velocity.x) < 0 or (
        (x - other.position.x) / other.velocity.x) < 0:
      return False

    return True

hailstones = []

def part1():
  num_intersections = 0
  for index, hail in enumerate(hailstones):
    for index2, hail2 in enumerate(hailstones[index + 1:]):
       if hail.intersect(hail2, 200000000000000, 400000000000000):
         print(f"{hail} and {hail2} intersect")
         num_intersections += 1
  print(f"Pt1: {num_intersections}")
     
def part2():
  pxr, pyr, pzr, vxr, vyr, vzr = z3.Reals("pxr pyr pzr vxr vyr vzr")
  solver = z3.Solver()
  # only 3 hailstones are needed here;  each creates 1 variable and 3 equations, for a total of 9 vars and 9 eqs
  for k, h in enumerate(hailstones[:3]):
    tK = z3.Real(f"t{k}")
    solver.add(tK > 0)
    solver.add(pxr + tK * vxr == h.position.x + tK * h.velocity.x)
    solver.add(pyr + tK * vyr == h.position.y + tK * h.velocity.y)
    solver.add(pzr + tK * vzr == h.position.z + tK * h.velocity.z)
  
  solver.check()
  total = sum(solver.model()[var].as_long() for var in [pxr, pyr, pzr])
  print(f"Pt2: {total}")

if __name__ == "__main__":
  args = parseArgs()

  for y, line in enumerate(open(args.infile, 'r')):
    hailstones.append(Hail(line.strip()))

  # part1()
  part2()
#  print("Part1", part1)
#  print("Part2", part2)
