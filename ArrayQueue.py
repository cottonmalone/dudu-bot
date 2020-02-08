
class ArrayQueue:
	def __init__(self):
		self.data = []

	def isEmpty(self):
		return self.data == []

	def enqueue(self, person):
		self.data.insert(0, person)

	def dequeue(self):
		return self.data.pop()

	def size(self):
		return len(self.data)

	def contains(self, person):
		s = self.size()
		i = 0
		while i < s:
			if self.data[i].id == person.id:
				return True
			i += 1
		return False

