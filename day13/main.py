import argparse

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()

class Pattern():
  def __init__(self):
    self.rows = []
    self.cols = []

  def add_line(self, line):
    self.rows.append(line)

  def __repr__(self):
    retStr = ""
    for line in self.rows:
      retStr += line + "\n"
    return retStr

  def returnDiff(self, row1, row2):
   #  print(f"Comparing Row {row1} {row2}")
    if row1 < 0:
      return 0
    if row2 >= len(self.rows):
      return 0
  # for part 2, is it only off by one....
    numDiff = 0
    for i in range(len(self.rows[row1])):
      if self.rows[row1][i] != self.rows[row2][i]:
        numDiff += 1
    return numDiff

  def isVertical(self, i):
    numDiff = 0
    for j in range(i + 1):
      numDiff += self.returnDiff(i - j, i + j + 1)
      if numDiff > 1:
        return False
    return (numDiff == 1)
  
  def findVerticalMirror(self):
    for i in range(len(self.rows) - 1):
      if self.isVertical(i):
        return i + 1
    return 0


  def transpose(self):
    cols = []
    for i in range(len(self.rows[0])):
      cols.append("")
    for i, row in enumerate(self.rows):
      for j, c in enumerate(row):
        cols[j] += c
    self.rows = cols

  def score(self):
    vertScore = self.findVerticalMirror()
    if vertScore:
      return 100 * vertScore
    self.transpose()
    horizScore = self.findVerticalMirror()
    return horizScore

def part1(data):
  total = 0
  for datum in data:
    score = datum.score()
    total += score
    print(f"{score} {total}")

if __name__ == "__main__":
  args = parseArgs()
  data = []
  pattern = Pattern()
  for line in open(args.infile, 'r'):
    strippedLine = line.strip()
    if strippedLine:
      pattern.add_line(strippedLine)
    else:
      data.append(pattern)
      pattern = Pattern()
  data.append(pattern)

  part1(data)