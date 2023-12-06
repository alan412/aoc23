import argparse
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

def parse(line):
  (before, after) = line.strip().split(":")
  return [int(time) for time in after.split(' ') if time]

def numberWays(milliseconds, millimeters):
   num_ways = 0
   for x in range(milliseconds):
      speed = x
      time = milliseconds - x
      if (time * speed) > millimeters:
         num_ways += 1
   return num_ways
      
def part1(times, distances):
  total = 1
  for i in range(len(times)):
     num_ways = numberWays(times[i], distances[i])
     total *= num_ways
     print(f"{num_ways} : {total}")

if __name__ == "__main__":
  args = parseArgs()
  times = []
  distances = []
  for line in open(args.infile, 'r'):
     if len(times) == 0:
        times = parse(line)
     else:
        distances = parse(line)
  part1(times, distances)