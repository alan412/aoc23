import argparse
import sys
import re
import heapq

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Pulse():
  def __init__(self, src, destination, low):
    self.src = src
    self.destination = destination
    self.low = low
  def __repr__(self):
    val = "LOW" if self.low else "HIGH"
    return f"{self.src}->{self.destination}:{val}"
  
class Module():
  def __init__(self, line):
    r = re.match("([%|&]?)(\w+) -> ([\w, ]+)", line)
    self.type = r.group(1)
    self.name = r.group(2)
    self.destinations = r.group(3).split(", ")
    self.src_memory = None
    self.state = False
    self.setup_connections()
   
  def setup_connections(self):
    for dest in self.destinations:
      destList = connections_by_dest.get(dest, None)
      if destList == None:
        destList = []
        connections_by_dest[dest] = destList
      destList.append(self.name)

  def process_pulse(self, pulse, time):
    pulse_time = pulses.get(time + 1, None)
    if pulse_time == None:
      pulse_time = []
      pulses[time + 1] = pulse_time

    pulse_out = pulse.low
    if self.type == '%': # Flip flop
      if pulse.low:
        self.state = not self.state
        pulse_out = not self.state
      else:
        return
    elif self.type == '&': # conjunction
      if not self.src_memory:
        self.src_memory = {}
        for src in connections_by_dest[self.name]:
          self.src_memory[src] = True
      self.src_memory[pulse.src] = pulse.low
      all_high = True
      for memory in self.src_memory:
        if self.src_memory[memory] != False:
          all_high = False
          break
      pulse_out = all_high
    for dest in self.destinations:
      pulse_time.append(Pulse(self.name, dest, pulse_out)) 

  def __repr__(self):
    return f"{self.type} {self.name} {self.src_memory} {self.state} -> {self.destinations}"

def score(pulses):
  time = 1
  total_low = 1   # include button original one
  total_high = 0
  pulseList = pulses.get(time, None)
  while pulseList:
    for pulse in pulseList:
      if pulse.low == True:
        total_low += 1
      else:
        total_high += 1
    time += 1
    pulseList = pulses.get(time, None)
  return total_low, total_high

def part1(modules):
  global pulses 
  total_low = 0
  total_high = 0
  for buttonPress in range(1_000):
    modules['broadcaster'].process_pulse(Pulse('button', 'broadcast', True), 0)
    time = 1
    pulseList = pulses.get(time, None)
    while pulseList:
       for pulse in pulseList:
          if pulse.destination in modules:
            modules[pulse.destination].process_pulse(pulse, time)
       time += 1
       pulseList = pulses.get(time, None)
    low, high = score(pulses)
    total_low += low
    total_high += high
    # print(f"{buttonPress} - {total_low}, {total_high}: {pulses}")
    pulses = {}
  print(f"Part1: {total_low * total_high}")

def part2(modules):
  global pulses
  button_presses = 0
  done = False
  while not done:
    modules['broadcaster'].process_pulse(Pulse('button', 'broadcast', True), 0)
    time = 1
    num_rx_low_pulses = 0
    num_rx_high_pulses = 0
    pulseList = pulses.get(time, None)
    while pulseList:
       for pulse in pulseList:
          # Not happy about this, basically figured out it was an lcm problem from reddit
          # and then figured it out specific for my input set by changing this to each of the four
          # that fed in (after making a graphviz of the whole thing)
          if pulse.src == 'kv' and not pulse.low:
            print(f"{button_presses}: {pulse}")
          if pulse.destination == 'rx':
            if pulse.low:
              num_rx_low_pulses += 1
            else:
              num_rx_high_pulses += 1
          elif pulse.destination in modules:
            modules[pulse.destination].process_pulse(pulse, time)
       time += 1
       pulseList = pulses.get(time, None)
    if num_rx_low_pulses == 1:
      done = True
      print(f"After {button_presses + 1} press")
    else:
      button_presses += 1
      pulses = {}

modules = {}
# map of time plus list  
pulses = {}

connections_by_dest = dict()

if __name__ == "__main__":
  args = parseArgs()

  for y, line in enumerate(open(args.infile, 'r')):
    new_module = Module(line.strip())
    modules[new_module.name] = new_module

  # part1(modules)
  part2(modules)