import argparse
import sys
import re
import heapq

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Grid():
  def __init__(self):
    self.lines = []
    self.maxY = 0
    self.maxX = 0

  def add_line(self, line, y):
    self.lines.append(line)
    self.maxX = len(line) - 1
    self.maxY = y
  
  def __repr__(self):
    retStr = ""
    for line in self.lines:
      retStr += line + "\n"
    return retStr
    
  def valid(self, x, y):
    if x < 0 or x > self.maxX or y < 0 or y > self.maxY:
      return False
    return True
  
  def run(self, min_distance, max_distance, goal_x, goal_y):
    DIRS = [(0,1), (1,0), (0,-1), (-1,0)]
    q = [(0, 0, 0, -1)]
    seen = set()
    costs = {}
    while q:
      cost, x, y, disallowed_dir = heapq.heappop(q)
      if x == goal_x and y == goal_y:
        return cost
      if (x, y, disallowed_dir) in seen:
        continue
      seen.add((x, y, disallowed_dir))
      for direction in range(4):
        cost_increase = 0
        if direction == disallowed_dir or (direction + 2) % 4 == disallowed_dir:
          # not allowed
          continue
        for distance in range(1, max_distance + 1):
          xx = x + DIRS[direction][0] * distance
          yy = y + DIRS[direction][1] * distance
          if self.valid(xx, yy):
            cost_increase += int(self.lines[yy][xx])
            if distance < min_distance:
              continue
            new_cost = cost + cost_increase
            if costs.get((xx, yy, direction), 1e100) <= new_cost:
              continue
            costs[(xx, yy, direction)] = new_cost
            heapq.heappush(q, (new_cost, xx, yy, direction))
        
  def part1(self):
    print(self)
    print(f"Part1 {self.run(1, 3, self.maxX, self.maxY)}")
    print(f"Part2 {self.run(4, 10, self.maxX, self.maxY)}")


if __name__ == "__main__":
  args = parseArgs()
  grid = Grid()

  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line.strip(), y)
  grid.part1()
  #grid.part2()