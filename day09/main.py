import argparse
from itertools import pairwise

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

def diffList(prevList):
  newList = []
  for item_1, item_2 in pairwise(prevList):
      newList.append(item_2 - item_1)
  return newList

class History:   
   def __init__(self, line):
      self.lists =[[int(num) for num in line.strip().split()]]
      self.lists[0].reverse()
      index = 0
      while any(self.lists[index]):
         self.lists.append(diffList(self.lists[index]))
         index += 1

   def solve(self):
      i = len(self.lists) - 1
      self.lists[i].append(0)
      while i > 0:
         self.lists[i - 1].append(self.lists[i][-1] + self.lists[i -1][-1])
         i -= 1
         
      print(f"{self.lists}")
      return self.lists[0][-1]
   def __repr__(self):
      return f"{self.lists[0]}"
      
def part1(data):
   total = 0
   for datum in data:
      total += datum.solve()
 
   print(f"Total: {total}")

if __name__ == "__main__":
  args = parseArgs()
  data = []
  for line in open(args.infile, 'r'):
     data.append(History(line))
  
  part1(data)
