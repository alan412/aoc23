import argparse
import sys
import re
import heapq

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Instruction():
  def __init__(self, dir, num, color):
    translate = {'0' : 'R', '1' : 'D', '2' : 'L', '3' : 'U'} 
    self.num = int(color[0:5], 16)
    self.dir = translate[color[5]]
    self.color = num

  def __repr__(self):
    return f"{self.dir} {self.num} {self.color}"

def tadd(first, second):
  return (first[0] + second[0], first[1] + second[1])

class Grid():
  def __init__(self):
    self.map = {}
    self.currentPos = (0,0)
    self.largestX = 0
    self.largestY = 0
    self.smallestX = 0
    self.smallestY = 0
    self.corners = [(0,0)]
    self.perimeter = 0

  def add_line(self, line, y):
    r = re.match("(R|D|L|U) (\d+) \(\#([0-9a-f]+)", line)
    newInstruction = Instruction(r.group(1), int(r.group(2)), r.group(3))
    print(newInstruction, line)

    change = (0, 0)
    match newInstruction.dir:
       case 'R':
        change = (1, 0)
       case 'D':
        change = (0, 1)
       case 'L':
        change = (-1, 0)
       case 'U':
        change = (0, -1)
    
    # for i in range(newInstruction.num):
    #    self.currentPos = tadd(self.currentPos, change)
    #    self.map[self.currentPos] = '#'
    #    self.largestX = max(self.largestX, self.currentPos[0])
    #    self.smallestX = min(self.smallestX, self.currentPos[0])

    #    self.largestY = max(self.largestY, self.currentPos[1])
    #    self.smallestY = min(self.smallestY, self.currentPos[1])
    self.currentPos = tadd(self.currentPos, (change[0] * newInstruction.num, change[1] * newInstruction.num))
    self.corners.append(self.currentPos)
    self.perimeter += newInstruction.num
    print(self.corners)

  def volume(self):
    return abs(sum(
      (self.corners[i - 1][1] + self.corners[i][1]) * (self.corners[i - 1][0] - self.corners[i][0])
      for i in range(len(self.corners)) 
    )) // 2 + self.perimeter // 2 + 1
  
  def __repr__(self):
     return f"{self.map}"
  
  def valid(self, x, y):
    return self.smallestX <= x <= self.largestX and self.smallestY <= y <= self.largestY
      
  def fill(self, x, y, start_color, color_to_update):
    color = self.map.get((x,y), '')
    if color != start_color:
      return
    elif color == color_to_update:
      return
    else:
      self.map[(x,y)] = color_to_update
      neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
      for n in neighbors:
        if self.valid(n[0], n[1]):
          self.fill(n[0],n[1],start_color,color_to_update)
  def fill_bfs(self, x, y, start_color, color_to_update):
    queue = []
    queue.append([x,y])
    self.map[(x,y)] = color_to_update

    while queue:
      (x, y) = queue.pop()
      neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
      for n in neighbors:
        if self.valid(n[0], n[1]):
          color = self.map.get(n, '')
          if color == start_color:
            self.map[n] = color_to_update
            queue.append(n)

  def print_as_grid(self):
    for y in range(self.smallestY, self.largestY + 1):
      display = ""
      for x in range(self.smallestX, self.largestX + 1):
        if (x, y) in self.map:
          display += "#"
        else:
          display += "."
      print(display)

  def part1(self):
    #print(self)
    #print(f"Number dug: {len(self.map)}")
    # self.print_as_grid()
    #print("----After Filling----")
    
    #self.fill(1, 1, '', '#')
    #self.fill_bfs(1, 1, '', '#')
    # self.print_as_grid()
    #print(f"Number dug: {len(self.map)}")
    print(f"Part 2: Volume {self.volume()}")

sys.setrecursionlimit(100_000)

if __name__ == "__main__":
  args = parseArgs()
  grid = Grid()

  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line.strip(), y)
  grid.part1()
  #grid.part2()