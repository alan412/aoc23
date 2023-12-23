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

class Block():
  def __init__(self, x, y, z, b):
    self.x = x
    self.y = y
    self.z = z
    self.brick = b
  def __repr__(self):
    return f"({self.x},{self.y},{self.z}) : {self.brick}"
  def is_supported(self):
    return self.z == 1 or (blocks.get((self.x, self.y, self.z - 1), self).brick != self.brick)

class Brick():
  def __init__(self, start, end):
    self.startZ = min(start[2], end[2])
    self.blocks = [Block(x,y,z,self) for x in range(start[0],end[0] + 1) for y in range(start[1],end[1] + 1) for z in range(start[2],end[2] + 1)]

  def is_falling(self):
    return not any(b.is_supported() for b in self.blocks)
  
def collapse(bricks):
  dropped = set()
  for brick in bricks:
    while brick.is_falling():
      for b in brick.blocks:
        blocks[b.x, b.y, b.z - 1] = blocks.pop((b.x, b.y, b.z))
        b.z -= 1
      dropped.add(brick)
  return len(dropped)

bricks = []
blocks = {}

if __name__ == "__main__":
  args = parseArgs()

  for y, line in enumerate(open(args.infile, 'r')):
    r = re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)
    bricks.append(Brick((int(r.group(1)), int(r.group(2)), int(r.group(3))), 
                        (int(r.group(4)), int(r.group(5)), int(r.group(6)))))
  
  bricks = sorted(bricks, key = lambda a:a.startZ )
  blocks = {(b.x, b.y, b.z): b for br in bricks for b in br.blocks}

  collapse(bricks)
  save_location = {b:k for k,b in blocks.items()}

  part1 = 0
  part2 = 0
  for i, br in enumerate(bricks):
    for b in save_location:
      b.x,b.y,b.z = save_location[b]
    blocks = {save_location[b]: b for b in save_location if b.brick != br}
    dropped = collapse(bricks[:i] + bricks[i + 1: ])
    if dropped == 0:
      part1 += 1
    part2 += dropped

  print("Part1", part1)
  print("Part2", part2)
