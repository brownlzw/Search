from collections import deque
from heapq import heappush, heappop

# INTERNAL NOTE: All of this is tested.


class Queue:

	def __init__(self):
		self._items = deque()

	def push(self, item):
		self._items.append(item)

	def pop(self):
		if self.is_empty():
			raise IndexError('Tried to pop from an empty Queue.')
		return self._items.popleft()

	def is_empty(self):
		return self._items == deque()

class Stack(Queue):

	def pop(self):
		if self.is_empty():
			raise IndexError('Tried to pop from an empty Stack.')
		return self._items.pop()

class PriorityQueue:

	def __init__(self, low_priority_first=False):
		self._items = []
		self._priority_multiplier = 1 if low_priority_first else -1

	def push_with_priority(self, item, priority):
		prioritized = (self._priority_multiplier * priority, item)
		heappush(self._items, prioritized)

	def pop(self):
		if self.is_empty():
			raise IndexError('Tried to pop from an empty PriorityQueue')
		return heappop(self._items)[1]

	def is_empty(self):
		return self._items == []