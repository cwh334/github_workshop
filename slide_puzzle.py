import random, os

class Tile:
	def __init__(self, value, r, c):
		self.value = value
		self.r = r
		self.c = c
	def __str__(self):
		return str(self.value)

class Puzzle:
	def __init__(self, size_row = 4, size_col = 4):
		self.size_row = size_row
		self.size_col = size_col
		self.board = []
		value = 1
		for row in range(self.size_row):
			for col in range(self.size_col):
				self.board.append(Tile(value, row, col))
				value += 1
		
		self.board[-1].value = " "
		self.empty = self.board[-1]
		self.neighbors = []
		self.check()
		self.shuffle()
		self.play()

	def __str__(self):
		tmp = ""
		for r in range(self.size_row):
			for c in range(self.size_col):
				tmp += str(self.tile_by_loc(r, c)) + " " * (3 - len(str(self.tile_by_loc(r,c))))
			tmp += "\n"
		return tmp

	def tile_by_loc(self, r, c):
		for tile in self.board:
			if tile.r == r and tile.c == c:
				return tile

	def tile_by_value(self, value):
		for tile in self.board:
			if tile.value == value:
				return tile

	def swap(self, tile):
		self.empty.value = tile.value
		tile.value = " "
		self.empty = tile

	def check(self):
		self.neighbors = []
		for tile in self.board:
			if (tile.r - self.empty.r) ** 2 + (tile.c - self.empty.c) ** 2 == 1:
				self.neighbors.append(tile.value)

	def shuffle(self, rep = 500):
		for i in range(rep):
			rand_nei = random.choice(self.neighbors)
			self.swap(self.tile_by_value(rand_nei))
			self.check()

	def play(self):
		win = False
		while win == False:
			os.system("clear")
			print(self)
			choice = input("Please choose a tile to move: ")
			while not (choice.isdigit() and int(choice) in range(self.size_row * self.size_col)):
				choice = input("Cannot be moved. Please choose another: ")
			if int(choice) in self.neighbors:
				self.swap(self.tile_by_value(int(choice)))
				self.check()
			count = 0
			for tile in self.board:
				if tile.value == tile.r * self.size_col + (tile.c + 1):
					count += 1
			if count == self.size_row * self.size_col - 1:
				win = True
		if win == True:
			print(self)
			print("You win.")


p = Puzzle(5, 5)



