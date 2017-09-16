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
	map = {}
	cur = start
	q.push(start)
	map[start] = None
	while not q.is_empty():
		cur = q.pop()
		if problem.is_goal_state(cur):
			break;
		for state in problem.get_successors(cur):
			if state not in map:
				q.push(state)
				map[state] = cur
	list = []
	while cur != None:
		list.append(cur)
		cur = map[cur]
	return list[::-1]


def dfs(problem):
	"""
	Implement depth-first search.
	"""
	start = problem.get_start_state()
	s = Stack()
	map = {}
	cur = start
	s.push(start)
	map[start] = None
	while not s.is_empty():
		cur = s.pop()
		if problem.is_goal_state(cur):
			break;
		for state in problem.get_successors(cur):
			if state not in map:
				s.push(state)
				map[state] = cur
	list = []
	while cur != None:
		list.append(cur)
		cur = map[cur]
	return list[::-1]

def ids(problem):
	"""
	Implement iterative deepening search.
	"""
	start = problem.get_start_state()
	frontier = []
	map = {}
	end = start
	frontier.append(start)
	map[start] = None
	found = False
	while not found:
		newFrontier = []
		for cur in frontier:
			print cur
			if problem.is_goal_state(cur):
				found = True
				end = cur
				break;
			for state in problem.get_successors(cur):
				if state not in map:
					newFrontier.append(state)
					map[state] = cur
			if not found:
				frontier = newFrontier
	print "=" * 10
	list = []
	while end != None:
		list.append(end)
		end = map[end]
	return list[::-1]

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
			break;
		for state in problem.get_successors(forward):
			if state not in map1:
				q1.push(state)
				map1[state] = forward
		backward = q2.pop()
		if backward in map1:
			forward = map1[backward]
			break;
		for state in problem.get_successors(backward):
			if state not in map2:
				q2.push(state)
				map2[state] = backward
	list = []
	while forward != None:
		list.append(forward)
		forward = map1[forward]
	list = list[::-1]
	while backward != None:
		list.append(backward)
		backward = map2[backward]
	return list

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
	map = {}
	cost = {}
	cur = start
	pq.push_with_priority(start, tilegame_heuristic(start))
	map[start] = None
	cost[start] = 0
	while not pq.is_empty():
		cur = pq.pop()
		curCost = cost[cur]
		if problem.is_goal_state(cur):
			break;
		for state in problem.get_successors(cur):
			if state not in map:
				pq.push_with_priority(state, curCost + 1 + tilegame_heuristic(state))
				map[state] = cur
				cost[state] = curCost + 1
	list = []
	while cur != None:
		list.append(cur)
		cur = map[cur]
	return list[::-1]


### SPECIFIC TO THE TILEGAME PROBLEM

def tilegame_heuristic(state):
	"""
	Produces a real number for the given tile game state representing
	an estimate of the cost to get to the goal state.
	"""
	list = TileGame.tuple_to_list(state)
	count = 0
	d = len(list)
	for i in range(d):
		for j in range(len(list[i])):
			row = (list[i][j] - 1) / d
			col = (list[i][j] - 1) % d
			count += abs(row - i) + abs(col - j)
	return count / 2

### YOUR SANDBOX ###

def main():
	"""
	Do whatever you want in here; this is for you.
	An example below shows how your functions might be used.
	"""
	# initialize a random 3x3 TileGame problem
	tg = TileGame(2)
	print TileGame.board_to_pretty_string(tg.get_start_state())
	#compute path
	path = astar(tg, tg.goal_state)
	# display path
	TileGame.print_pretty_path(path)

	# an example with DGraphs:
	# small_dgraph = DGraph([[None, None, 1], [1, None, 1], [1, 1, None]], {1})
	# print ids(small_dgraph)

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
