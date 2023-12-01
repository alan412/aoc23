import argparse
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class CalibrationLine:
   def convert(self, token):
      convertMap = {'one' : 1, 'two' : 2, 'three' : 3, 'four' : 4, 'five' : 5, 'six' : 6, 'seven' : 7, 'eight' : 8, 
                 'nine' : 9}      
      
      if token.isdigit():
         return int(token)
      return convertMap[token]
      
   def __init__(self, line):
      listTokens = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
      self.listNums = [self.convert(s) for s in listTokens]
      print(line, self.listNums)
   def value(self):
      return (self.listNums[0] * 10) + self.listNums[-1]

def part1(data):
  total = 0
  for item in data:
     total += item.value()
     print(f"Value: {item.value()}, Total: {total}")

if __name__ == "__main__":
  args = parseArgs()
  data = []
  for line in open(args.infile, 'r'):
     data.append(CalibrationLine(line))
  
  part1(data)