# NOTE TO STUDENT: Please read the handout before continuing.

from tilegameproblem import TileGame
from dgraph import DGraph
from datastructures import Queue, Stack, PriorityQueue
from testsuite import bfs_test, dfs_test, ids_test, bds_test, astar_test


def bfs(problem):
  """
  Implement breadth-first search.
  """
  start = problem.get_start_state()
  q = Queue()
  visited = {}
  cur = start
  q.push(start)
  visited[start] = None
  while not q.is_empty():
    cur = q.pop()
    if problem.is_goal_state(cur):
      break
    for state in problem.get_successors(cur):
      if state not in visited:
        q.push(state)
        visited[state] = cur
  path = []
  while cur is not None:
    path.append(cur)
    cur = visited[cur]
  path.reverse()
  return path


def dfs(problem):
  """
  Implement depth-first search.
  """
  start = problem.get_start_state()
  s = Stack()
  visited = {}
  cur = start
  s.push(start)
  visited[start] = None
  while not s.is_empty():
    cur = s.pop()
    if problem.is_goal_state(cur):
      break
    for state in problem.get_successors(cur):
      if state not in visited:
        s.push(state)
        visited[state] = cur
  path = []
  while cur is not None:
    path.append(cur)
    cur = visited[cur]
  path.reverse()
  return path


def ids(problem):
  """
  Implement iterative deepening search.
  """
  start = problem.get_start_state()
  path = []
  depth = 1
  while True:
    s = Stack()
    visited = {}
    cur = (start, 1)
    s.push(cur)
    visited[start] = None
    while not s.is_empty():
      (cur, d) = s.pop()
      if problem.is_goal_state(cur):
        while cur is not None:
          path.append(cur)
          cur = visited[cur]
        path.reverse()
        return path
      if d != depth:
        for state in problem.get_successors(cur):
          if state not in visited:
            s.push((state, d + 1))
            visited[state] = cur
    depth += 1


def bds(problem, goal):
  """
  Implement bi-directional search.

  The input 'goal' is a goal state (not a search problem, just a state)
  from which to begin the search toward the start state.

  Assume that the input search problem can be thought of as
  an undirected graph. That is, all actions in the search problem
  are reversible.
  """
  start = problem.get_start_state()
  q1 = Queue()
  q2 = Queue()
  map1 = {}
  map2 = {}
  forward = start
  backward = goal
  q1.push(start)
  q2.push(goal)
  map1[start] = None
  map2[goal] = None
  while not (q1.is_empty() or q2.is_empty()):
    forward = q1.pop()
    if forward in map2:
      backward = map2[forward]
      break
    for state in problem.get_successors(forward):
      if state not in map1:
        q1.push(state)
        map1[state] = forward
    backward = q2.pop()
    if backward in map1:
      forward = map1[backward]
      break
    for state in problem.get_successors(backward):
      if state not in map2:
        q2.push(state)
        map2[state] = backward
  path = []
  while forward is not None:
    path.append(forward)
    forward = map1[forward]
  path.reverse()
  while backward is not None:
    path.append(backward)
    backward = map2[backward]
  return path


def astar(problem, heur):
  """
  Implement A* search.

  The given heuristic function will take in a state of the search problem
  and produce a real number

  Your implementation should be able to work with any heuristic, heur
  that is for the given search problem (but, of course, without a
  guarantee of optimality if heur is not admissible).
  """
  start = problem.get_start_state()
  pq = PriorityQueue(True)
  visited = {}
  cost = {}
  cur = start
  pq.push_with_priority(start, heur(start))
  visited[start] = None
  cost[start] = 0
  while not pq.is_empty():
    cur = pq.pop()
    cur_cost = cost[cur]
    if problem.is_goal_state(cur):
      break
    for state in problem.get_successors(cur):
      if state not in visited:
        pq.push_with_priority(state, cur_cost + 1 + heur(state))
        visited[state] = cur
        cost[state] = cur_cost + 1
  path = []
  while cur is not None:
    path.append(cur)
    cur = visited[cur]
  path.reverse()
  return path


### SPECIFIC TO THE TILEGAME PROBLEM

def tilegame_heuristic(state):
  """
  Produces a real number for the given tile game state representing
  an estimate of the cost to get to the goal state.
  """
  state_list = TileGame.tuple_to_list(state)
  count = 0
  d = len(state_list)
  for i in range(d):
    for j in range(len(state_list[i])):
      row = (state_list[i][j] - 1) / d
      col = (state_list[i][j] - 1) % d
      count += abs(row - i) + abs(col - j)
  return count / 2


### YOUR SANDBOX ###

def main():
  """
  Do whatever you want in here; this is for you.
  An example below shows how your functions might be used.
  """
  # initialize a random 3x3 TileGame problem
  tg = TileGame(3)
  print TileGame.board_to_pretty_string(tg.get_start_state())
  # compute path
  path = astar(tg, tilegame_heuristic)
  # display path
  TileGame.print_pretty_path(path)


# an example with DGraphs:
small_dgraph = DGraph([[None, None, 1], [1, None, 1], [1, 1, None]], {1})
print ids(small_dgraph)

def tester():
  """
  Checks I/O basics with trivial test cases.
  You will want to call this from main() once you've written your code.

  You will also want to do more thorough testing of your own.
  Like main(), feel free to modify this function in any way you like.
  """
  bfs_test(bfs)
  dfs_test(dfs)
  ids_test(ids)
  bds_test(bds)
  astar_test(astar)


if __name__ == '__main__':
  main()
