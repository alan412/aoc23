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

class Node():
  def __init__(self, pt):
    self.pt = pt
    self.connections = {}
  def add_edge(self, node, weight=1):
    self.connections[node] = weight
  def remove_edge(self, node):
    del self.connections[node]
  def remove_thyself(self):
    keys = list(self.connections.keys())
    assert len(keys) == 2
    keys[0].add_edge(keys[1], self.connections[keys[0]] + self.connections[keys[1]])
    keys[1].add_edge(keys[0], self.connections[keys[1]] + self.connections[keys[0]])
    keys[0].remove_edge(self)
    keys[1].remove_edge(self)
  
class Grid():
  def __init__(self):
    self.squares = {}
    self.start = None
    self.maxX = 0
    self.maxY = 0
    self.positions = set()
    self.cache = {}
    self.graph = None
    self.longest = 0

  def add_line(self, line, y):
    for x, c in enumerate(line):
      self.squares[Point(x,y)] = c
    self.maxX = x
    self.maxY = y 

  def create_graph(self):
    self.graph = Node(self.find_start())
    self.dest = self.find_dest()
    nodes = {}
    nodes[self.graph.pt] = self.graph
    for x in range(self.maxX + 1):
      for y in range(self.maxY + 1):
        if (x,y) in self.squares and self.squares[(x,y)] in ".^<>v":
          nodes[(x,y)] = Node((x,y))

    for node in nodes.values():
      dirs = [(0,1),(0,-1),(1,0),(-1,0)]
      for d in dirs:
        new_point = add_pt(node.pt, d)
        if new_point in nodes:
          node.add_edge(nodes[new_point])
    
    self.graph = nodes[self.graph.pt]
    # graph made, now collapse
    for node in nodes.values():
      if len(node.connections) == 2:   # One way only 
        node.remove_thyself()
  
  @cache
  def calculate_path(self, visited_squares, output=False):
    total_weight = 0
    prev_square = visited_squares[0]
    for square in visited_squares[1:]:
      if output: 
        print(f"{prev_square.pt}->{square.pt}: {square.connections[prev_square]}")
      total_weight += square.connections[prev_square]
      prev_square = square
    return total_weight

  def find_path(self, node, visited_squares):
    # t_parameters = (node.pt, tuple(visited_squares))
    # cache_result = self.cache.get(t_parameters, None)
    # if cache_result:
    #   return cache_result

    visited_squares.append(node)
    paths = []

    for n in node.connections.keys():
      if n in visited_squares:
        continue
      if n.pt == self.dest:
        visited_squares.append(n)
        paths.append(visited_squares)
      else:
        new_path = self.find_path(n, [sq for sq in visited_squares])
        if new_path:
          paths.append(new_path)
    
    # which path is longest
    longest = 0
    longestPath = None
    for path in paths:
      length_path = self.calculate_path(tuple(path))
      if length_path > longest:
        longestPath = path
        longest = length_path
        if length_path > self.longest:
          self.longest = length_path
          print(f"New Longest: {self.longest}")
    
    # self.cache[t_parameters] = longestPath
    return longestPath
  
  def print_nodes(self, node, visited):
    print("Node", node.pt, len(node.connections))
    visited.add(node)
    for n in node.connections:
      if n not in visited:
        self.print_nodes(n, visited)
 
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
  grid.create_graph()
  print("Starting Find Path")
  visited = set()
  grid.print_nodes(grid.graph, visited)
  path = grid.find_path(grid.graph, [])
  length = grid.calculate_path(tuple(path), output=True)
  print(f"Part 1: {length}")

sys.setrecursionlimit(100_000)

if __name__ == "__main__":
  args = parseArgs()

  grid = Grid()
  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line, y)

  part1(grid)
  # part2(grid)