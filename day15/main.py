import argparse
import re

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Step():
  def __init__(self, step):
    self.focal = None
    self.hash = None
    r = re.match(r"(\w+)=(\d+)", step)
    if r:
      self.text = r.group(1)
      self.focal = int(r.group(2))
    else:
      r = re.match(r"(\w+)-", step)
      self.text = r.group(1)
  
  def getHash(self):
    if not self.hash:   
      total = 0
      for c in self.text:
        val = ord(c)
        total += val
        total *= 17
        total = total & 0x0FF
      self.hash = total
    return self.hash
  def __repr__(self):
    return f"{self.text} {self.focal}"

class Box():
  def __init__(self):
    self.listLenses = []
  
  def add(self, step):
    for lens in self.listLenses:
      if step.text == lens.text:
        lens.focal = step.focal
        return
    self.listLenses.append(step)

  def remove(self, step):
    for lens in self.listLenses:
      if step.text == lens.text:
        self.listLenses.remove(lens)
        return

  def __repr__(self):
    return f"{self.listLenses}"
  
  def score(self, boxNum):
    total = 0
    for slot, lens in enumerate(self.listLenses):
      total += (boxNum + 1) * (slot + 1) * lens.focal

    return total


class InitializationSequence():
  def __init__(self, line):
    self.steps = [Step(x) for x in line.split(',')]
  def sum(self):
    total = 0
    for step in self.steps:
      total += step.getHash()
    return total
  def part2(self):
    boxes = {}
    for step in self.steps:
      box = boxes.get(step.getHash(), None)
      if not box:
        box = Box()
        boxes[step.getHash()] = box
      if step.focal is not None:   # It is an add, not a remove
        box.add(step)
      else:
        box.remove(step)
      print(f"{boxes}")
    total = 0
    for boxNum, box in boxes.items():
      total += box.score(boxNum)
    print(f"Total: {total}")

if __name__ == "__main__":
  args = parseArgs()

  for y, line in enumerate(open(args.infile, 'r')):
    sequence = InitializationSequence(line.strip())

  sequence.part2()
