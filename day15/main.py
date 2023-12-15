import argparse

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Step():
  def __init__(self, step):
    self.text = step
  def getHash(self):
    total = 0
    for c in self.text:
      val = ord(c)
      total += val
      total *= 17
      total = total & 0x0FF
    return total

class InitializationSequence():
  def __init__(self, line):
    self.steps = [Step(x) for x in line.split(',')]
  def sum(self):
    total = 0
    for step in self.steps:
      total += step.getHash()
    return total

if __name__ == "__main__":
  args = parseArgs()
  step = Step("HASH")
  print(f"HASH: {step.getHash()}")

  for y, line in enumerate(open(args.infile, 'r')):
    sequence = InitializationSequence(line.strip())
    print(f"Part1: {sequence.sum()}")