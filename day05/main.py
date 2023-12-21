import argparse
import re
from collections import namedtuple

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class TranslateRange:
   def __init__(self, srcStart, length, adjust=0):
      self.start = srcStart
      self.length = length
      self.adjust = adjust
   def __eq__(self,other):
        if other == None:
           return False
        return self.start == other.start and self.length == other.length and self.adjust == other.adjust
   def __hash__(self):
        return hash(str(self))
   def __repr__(self):
      return f"{self.start} {self.length} {self.adjust}"
         
   
class Map:
   def __init__(self, line):
      listTokens = line.split()
      destStart = int(listTokens[0])
      self.start = int(listTokens[1])
      self.length = int(listTokens[2])
      self.adjust = destStart - self.start
   def __lt__(self, other):
      return self.start < other.start
   
   def translate(self, src):
      if (src < self.start) or src > (self.start + self.length):
         return None
      return src + self.adjust
   
   def __repr__(self):
      return f"{self.offset} {self.start} {self.length}"

class MapGroup:
   def __init__(self, line):
      match = re.match(r'(\w+)-to-(\w+) map:', line)
      self.src = match.group(1)
      self.dest = match.group(2)
      self.maps = [] 
   def add(self, line):
      self.maps.append(Map(line))
   
   def sort(self):
      self.maps = sorted(self.maps)

   def translate(self, src):
      for m in self.maps:
         d = m.translate(src)
         if d:
            return d
      return src
   
   def translate_range(self, pairs):
      for start, end in pairs:
        for m in self.maps:
          yield (start, min(m.start, end))
          yield (max(m.start, start) + m.adjust, min(m.start + m.length, end) + m.adjust)
          start = max(start, min(m.start + m.length, end))
        yield (start, end)
      
   def __repr__(self):
      retVal = f"\n{self.src}->{self.dest}"
      for map in self.maps:
         retVal += f"\n {map}"
      return retVal

def part1(seeds, data):
   closestDest = 200_000_000_000_000_000 # should be MAX_INT
   for seed in seeds:
      src = seed
      for group in data:
         src = group.translate(src)
      print(f"{seed}->{src}")
      if src < closestDest:
         closestDest = src
   print(f"Closest: {closestDest}")

def solve(data, seeds):
  for m in data:
    m.sort()
    seeds = [(a, b) for a, b in m.translate_range(seeds) if a < b]
  return min(a for a, b in seeds)

def part2(seeds, data):
   answer2 = solve(data, ((x, x+y) for x, y in zip(seeds[::2], seeds[1::2])))
   print("Pt2", answer2)

if __name__ == "__main__":
  args = parseArgs()
  data = []
  seeds = []
  currGroup = None
  for line in open(args.infile, 'r'):
     line = line.strip()
     if len(seeds) == 0:
        (before, after) = line.split(":")
        seeds = [int(num) for num in after.split(" ") if num]
     else:
        if not line:
           currGroup = None
        elif currGroup == None:
           currGroup = MapGroup(line)
           data.append(currGroup)
        else:
           currGroup.add(line)
  
  # part1(seeds, data)
  part2(seeds, data)