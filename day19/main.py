import argparse
import sys
import re
import heapq

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Range():
  def __init__(self, lower, upper):
    self.lower = lower
    self.upper = upper
  def size(self):
    if self.upper > self.lower:
      return (self.upper - self.lower) + 1
    return 0
  def intersect(self, other):
    lower = max(self.lower, other.lower)
    upper = min(self.upper, other.upper)
    return Range(lower, upper)
  def __repr__(self):
    return f"({self.lower}->{self.upper})"

class Rule():
  def __init__(self, rule):
    self.varCheck = None
    self.comparison = None
    self.value = None
    self.dest = None
    r = re.match("([xmas])([<>])(\d+):(\w+)", rule)
    if r:
      self.varCheck = r.group(1)
      self.comparison = r.group(2)
      self.value = int(r.group(3))
      self.dest = r.group(4)
    else:
      self.dest = rule
  def runRange(self, mapWorkflow, ranges):
    if not self.comparison:
      return mapWorkflow[self.dest].runRange(mapWorkflow, ranges), {k:None for k in 'xmas'}
    
    old_range = ranges[self.varCheck]
    complement_ = ranges[self.varCheck]

    if self.comparison == '<':
      range_ = old_range.intersect(Range(1, self.value - 1))
      complement_ = old_range.intersect(Range(self.value, 4000))
    if self.comparison == '>':
      range_ = old_range.intersect(Range(self.value + 1, 4000))
      complement_ = old_range.intersect(Range(1, self.value))
    
    new_ranges = dict(ranges)
    new_ranges[self.varCheck] = range_

    complement_ranges = dict(ranges)
    complement_ranges[self.varCheck] = complement_

    return mapWorkflow[self.dest].runRange(mapWorkflow, new_ranges), complement_ranges

  def process_part(self, part):
    if not self.comparison:
      return self.dest
    if self.comparison == '<':
      match self.varCheck:
        case 'x':
          if part.x < self.value:
            return self.dest
        case 'm':
          if part.m < self.value:
            return self.dest
        case 'a':
          if part.a < self.value:
            return self.dest
        case 's':
          if part.s < self.value:
            return self.dest
    else:
      match self.varCheck:
        case 'x':
          if part.x > self.value:
            return self.dest
        case 'm':
          if part.m > self.value:
            return self.dest
        case 'a':
          if part.a > self.value:
            return self.dest
        case 's':
          if part.s > self.value:
            return self.dest
    return None

  def __repr__(self):
    if self.comparison:
      return f"{self.varCheck}{self.comparison}{self.value}->{self.dest}"
    else:
      return f"->{self.dest}"

class Workflow():
  def __init__(self, line):
    r = re.match("(\w+){(.*)}", line)
    self.name = r.group(1)
    self.rules = [Rule(ruleText) for ruleText in r.group(2).split(",")]
  def __repr__(self):
    return f"{self.name}: {self.rules}"
  def process_part(self, part):
    for rule in self.rules:
       dest = rule.process_part(part)
       if dest:
         print(f"{part} -> {dest}")
         return dest
    return None
  
  def runRange(self, mapWorkflow, ranges):
    if self.name == 'A':
      total = 1
      for k in 'xmas':
        total *= ranges[k].size()
      return total
    if self.name == 'R':
      return 0
    total = 0
    for rule in self.rules:
      (result, ranges) = rule.runRange(mapWorkflow, ranges)
      total += result
    return total
    
    
class Part():
  def __init__(self, line):
    r = re.match("{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line)
    self.x = int(r.group(1))
    self.m = int(r.group(2))
    self.a = int(r.group(3))
    self.s = int(r.group(4))
  def score(self):
    return self.x + self.m + self.a + self.s
  
  def __repr__(self):
    return f"(x:{self.x}, m:{self.m}, a:{self.a}, s:{self.s})"

def part1(workflows, parts):
  mapWorkflow = dict()
  accepted = []
  for workflow in workflows:
    mapWorkflow[workflow.name] = workflow
  for part in parts:
    dest = mapWorkflow['in'].process_part(part)
    while dest != 'R' and dest != 'A':
      dest = mapWorkflow[dest].process_part(part)
    if dest == 'A':
      accepted.append(part)
  total = 0
  for part in accepted:
    print(part)
    total += part.score()
  print(f"Part1: {total}")


def part2(workflows):
  mapWorkflow = dict()
  mapWorkflow['A'] = Workflow('A{A}')
  mapWorkflow['R'] = Workflow('R{R}')
  for workflow in workflows:
    mapWorkflow[workflow.name] = workflow
  ans = mapWorkflow['in'].runRange(mapWorkflow, {k: Range(1,4000) for k in 'xmas'})
  print(f"Part2: {ans}")

if __name__ == "__main__":
  args = parseArgs()
  
  workflows = []
  parts = []

  inParts = False
  for y, line in enumerate(open(args.infile, 'r')):
    line = line.strip()
    if not line:
      inParts = True
      continue
    if not inParts:
      workflows.append(Workflow(line))
    else:
      parts.append(Part(line))
  #part1(workflows, parts)
  part2(workflows)