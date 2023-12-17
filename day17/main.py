import argparse
import sys
import re
import heapq

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def get_possible_directions(node):
  """Not the way they came from and not three in a row"""
  possible_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

  if node.parent:
    direction = node.direction_from_parent()
    not_allowed = (direction[0] * -1, direction[1] * -1)
    possible_directions.remove(not_allowed)
  
    if node.calc_in_a_row_greater_than(3, direction):
      print(f"Removing {direction} from {node} {node.parent} {node.parent.parent} {node.parent.parent.parent}")
      possible_directions.remove(direction)

  return possible_directions

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def calc_in_a_row_greater_than(self, number, direction):
       print(f"{self} <{number} {direction}")
       if number <= 0:
          return True
       if direction == self.direction_from_parent():
          return self.parent.calc_in_a_row_greater_than(number - 1, direction)
       return False
              
    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f
  
    def direction_from_parent(self):
       if not self.parent:
          return (0,0)
       return (self.position[0] - self.parent.position[0], self.position[1] - self.parent.position[1])

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        print(f"Open: {open_list}")
        print(f"Closed: {closed_list}")
        
        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in get_possible_directions(current_node): # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + int(maze[child.position[0]][child.position[1]])
            child.h = 0 # ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
    return None

class Grid():
  def __init__(self):
    self.lines = []
    self.maxY = 0
    self.maxX = 0

  def add_line(self, line, y):
    self.lines.append(line)
    self.maxX = len(line) - 1
    self.maxY = y
  
  def __repr__(self):
    retStr = ""
    for line in self.lines:
      retStr += line + "\n"
    return retStr
    
  def part1(self):
    print(self)
#    path = astar(self.lines, (0, 0), (self.maxY, self.maxX))
    path = astar(self.lines, (0, 0), (0,8))

    # path = astar(self.lines, (11,7), (self.maxY, self.maxX))
    total = 0
    for node in path[1:]:
      weight = int(self.lines[node[0]][node[1]])
      total += weight
      print(f"{node} {weight} , {total}")

if __name__ == "__main__":
  args = parseArgs()
  grid = Grid()

  for y, line in enumerate(open(args.infile, 'r')):
    grid.add_line(line.strip(), y)
  grid.part1()
  #grid.part2()