import argparse
import sys
import re
import heapq
from collections import namedtuple
from functools import cache, total_ordering
from dataclasses import dataclass
import numpy as np
import random
import z3

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

wires = {}

def parseLine(line):
  (src, dest) = line.split(':')
  destList = dest[1:].split(' ')
  for d in destList:
    wires[src] = wires.get(src, []) + [d]
    wires[d] = wires.get(d, []) + [src]

def get_comp_size(root, cut):
  nodes = [root]
  seen = {root}

  while nodes:
    new_nodes = []
    for node in nodes:
      for neighbor in wires[node]:
        if neighbor in seen or (node, neighbor) in cut or (neighbor, node) in cut:
          continue
        seen.add(neighbor)
        new_nodes.append(neighbor)
      nodes = new_nodes
  return len(seen)

def get_path(start, end):
  prev = {start: start}
  nodes = [start]
  seen = {start}
  while nodes:
    new_nodes = []
    for node in nodes:
      for neighbor in wires[node]:
        if neighbor in seen:
          continue
        seen.add(neighbor)
        prev[neighbor] = node
        new_nodes.append(neighbor)
    nodes = new_nodes
  
  if prev.get(end) is None:
    return None
  
  path = []
  node = end
  while node != start:
    path.append(node)
    node = prev[node]
  path.append(start)
  return path[::-1]

def part1():
  uses = {}
  for _ in range(10000):
    a, b = random.sample(list(wires.keys()), 2)
    path = get_path(a, b)
    for i in range(len(path) - 1):
      edge = tuple(sorted([path[i], path[i+1]]))
      uses[edge] = uses.get(edge, 0) + 1
  s_uses = sorted(uses.items(), key = lambda x: x[1], reverse=True)

  banned = [p[0] for p in s_uses[:3]]

  s1, s2 = get_comp_size(banned[0][0], banned), get_comp_size(banned[0][1], banned)
  print(s1*s2)

if __name__ == "__main__":
  args = parseArgs()

  for y, line in enumerate(open(args.infile, 'r')):
    parseLine(line.strip())
  
  part1()
  # part2()
#  print("Part1", part1)
#  print("Part2", part2)
