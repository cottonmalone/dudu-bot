
class ArrayQueue:
	def __init__(self):
		self.data = []
		self.sz = 0

	def enqueue(self, person):
		self.sz += 1
		self.data.insert(0, person)

	def availableSpace(self):
		return self.sz < 1

	def dequeue(self):
		self.sz -= 1
		return self.data.pop()

	def size(self):
		return self.sz

	def isEmpty(self):
		return self.sz == 0

	def getQueue(self):
		return self.data

	def contains(self, person):
		return self.indexOf(person) >= 0

	def indexOf(self, person):
		s = self.size()
		i = 0
		while i < s:
			if self.data[i].id == person.id:
				return i
			i += 1
		return -1