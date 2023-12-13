import argparse
import re
import sys
from functools import cache

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

@cache
def calculate_arrangements(pattern, counts):
  if not pattern:
    return len(counts) == 0
  if not counts:
    return '#' not in pattern
  
  result = 0

  if pattern[0] in ".?":
      result += calculate_arrangements(pattern[1:], counts)
  if pattern[0] in "#?" and \
     counts[0] <= len(pattern) and \
      "." not in pattern[:counts[0]] and \
      (counts[0] == len(pattern) or pattern[counts[0]] != "#"):
    result += calculate_arrangements(pattern[counts[0] + 1:], counts[1:])
  return result

class Springs:
  def __init__(self, line):
    (self.springs, numbers) = line.strip().split()
    self.numbers = [int(x) for x in numbers.split(",")]
    self.regex = None

  def unfold(self):
    self.springs = self.springs + '?' + \
                   self.springs + '?' + \
                   self.springs + '?' + \
                   self.springs + '?' + self.springs
    origNumbers = self.numbers.copy()
    self.numbers.extend(origNumbers)
    self.numbers.extend(origNumbers)
    self.numbers.extend(origNumbers)
    self.numbers.extend(origNumbers)

  def match(self, pattern):
    foundNumbers = []
    currPattern = 0
    for c in pattern:
      if c == '#':
        currPattern += 1
      elif c == '.':
        if currPattern != 0:
          foundNumbers.append(currPattern)
          currPattern = 0
    if currPattern != 0:
      foundNumbers.append(currPattern)
    
    return foundNumbers == self.numbers
  
  def cant_work(self, pattern):
    if not self.regex:
      regex_string = ""
      for number in self.numbers:
        if regex_string != "":
          regex_string += "[.\?]+"
        else:
          regex_string += "[.\?]*"
        regex_string += "[#\?]{" + str(number) +"}"
      regex_string += "[.\?]*"
      print(f"{regex_string} from {self.numbers}: {pattern}")
  
      self.regex = re.compile(regex_string)
    if not self.regex.fullmatch(pattern):
      return True
    return False

  def findMatches(self, pattern, i):
    # If it can't possibly work, go ahead and return 0
    if self.cant_work(pattern):
      return 0
    nextQuestion = pattern.find('?', i)
    if nextQuestion != -1:
      return self.findMatches(pattern[:nextQuestion] + '.' + pattern[nextQuestion + 1:], nextQuestion) \
             + self.findMatches(pattern[:nextQuestion] + '#' + pattern[nextQuestion + 1:], nextQuestion)
    
    if self.match(pattern):
      return 1
    return 0

  def bruteForce(self):
    return self.findMatches(self.springs, 0)
  
    
  def smarter(self):
    return calculate_arrangements(self.springs, tuple(self.numbers))

  def __repr__(self):
    return f"{self.springs} {self.numbers}"

def part1(data):
  total = 0
  for datum in data:
    datum.unfold()
    print(datum)
    numOptions = datum.smarter()
    total += numOptions
    print(f"{numOptions} {total}")

sys.setrecursionlimit(100_000)

if __name__ == "__main__":
  args = parseArgs()
  data = []
  for line in open(args.infile, 'r'):
    data.append(Springs(line))

  part1(data)