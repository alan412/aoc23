import argparse
import re
import sys

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class TelescopeView:
  def __init__(self):
    self.galaxies = []
    self.rows = {}
    self.cols = {}
  def addGalaxy(self, x, y):
    if y in self.rows:
      self.rows[y].append(x)
    else:
      self.rows[y] = [x]
    if x in self.cols:
      self.cols[x].append(y)
    else:
      self.cols[x] = [y]
  
  def __repr__(self):
    return f"{self.galaxies}, Rows: {self.rows}, Cols: {self.cols}"
  
  def expand(self, maxSize):
    rowTranslate = {}
    colTranslate = {}

    rowDiff = 0
    for y in range(maxSize + 1):
      if y not in self.rows:
        rowDiff += 1
      else:
        rowTranslate[y] = y + rowDiff
    
    colDiff = 0
    for x in range(maxSize + 1):
      if x not in self.cols:
        colDiff += 1
      else:
        colTranslate[x] = x + colDiff
    
    for row in self.rows:
      for col in self.rows[row]:
        self.galaxies.append((rowTranslate[row], colTranslate[col]))

    for i, galaxy in enumerate(self.galaxies):
      print(f"{i}: {galaxy}")
  
def shortestDistance(galaxy1, galaxy2):
  (x1, y1) = galaxy1
  (x2, y2) = galaxy2
  return abs(x2 - x1) + abs(y2 - y1)


def part1(telescopeView):
  total = 0
  for i, galaxy1 in enumerate(telescopeView.galaxies):
    for galaxy2 in telescopeView.galaxies[i + 1:]:
      distance = shortestDistance(galaxy1, galaxy2) 
      total += distance
      print(f"{galaxy1} {galaxy2}: {distance} {total}")


if __name__ == "__main__":
  args = parseArgs()
  telescopeView = TelescopeView()
  maxSize = 0
  for y, line in enumerate(open(args.infile, 'r')):
     for x, ch in enumerate(line.strip()): 
        if ch != '.':
          telescopeView.addGalaxy(x, y)
        if x > maxSize:
          maxSize = x
  telescopeView.expand(maxSize)
  part1(telescopeView)



  