import argparse
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

def parse_part1(line):
  (before, after) = line.strip().split(":")
  return [int(time) for time in after.split(' ') if time]

def parse_part2(line):
  (before, after) = line.strip().split(":")
  return int("".join([time for time in after.split(' ') if time]))

def numberWays(milliseconds, millimeters):
   num_ways = 0
   for x in range(milliseconds):
      speed = x
      time = milliseconds - x
      if (time * speed) > millimeters:
         num_ways += 1        
      if(x % 100_000 == 0):
         print(f"X: {x}")    
   return num_ways

def part2(time, distance):
   print(f"{time} {distance}")
   print(f"{numberWays(time, distance)}")

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
  time = 0
  distance = 0

  for line in open(args.infile, 'r'):
     if len(times) == 0:
        times = parse_part1(line)
        time = parse_part2(line)
     else:
        distances = parse_part1(line)
        distance = parse_part2(line)
  part1(times, distances)
  part2(time, distance)