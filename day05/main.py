import argparse
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Map:
   def __init__(self, line):
      listTokens = line.split()
      self.destStart = int(listTokens[0])
      self.srcStart = int(listTokens[1])
      self.length = int(listTokens[2])
   def translate(self, src):
      if (src < self.srcStart) or src > (self.srcStart + self.length):
         return None
      return self.destStart + (src - self.srcStart)
      
   def __repr__(self):
      return f"{self.destStart} {self.srcStart} {self.length}"

class MapGroup:
   def __init__(self, line):
      match = re.match(r'(\w+)-to-(\w+) map:', line)
      self.src = match.group(1)
      self.dest = match.group(2)
      self.maps = [] 
   def add(self, line):
      self.maps.append(Map(line))
   def translate(self, src):
      for m in self.maps:
         d = m.translate(src)
         if d:
            return d
      return src

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
  
  part1(seeds, data)