import random, os

class Tile:
	def __init__(self, value, r, c):
		# value shows the sequence in which tiles should be in. 
		# r, c are coordinates of current locations
		self.value = value
		self.r = r
		self.c = c
	def __str__(self):
		return str(self.value)

class Puzzle:
	def __init__(self, size_row = 4, size_col = 4):
		# specify board size
		self.size_row = size_row
		self.size_col = size_col
		# create a list of tiles in the puzzle
		self.board = []
		value = 1
		for row in range(self.size_row):
			for col in range(self.size_col):
				self.board.append(Tile(value, row, col))
				value += 1
		# the last tile should be blank and store into another attribute self.empty
		self.board[-1].value = " "
		self.empty = self.board[-1]
		# a list of values of tiles that can be moved
		self.neighbors = []
		# create initial game board and play
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
		# search for a tile in the list using its location
		for tile in self.board:
			if tile.r == r and tile.c == c:
				return tile

	def tile_by_value(self, value):
		# search for a tile in the list using its value
		for tile in self.board:
			if tile.value == value:
				return tile

	def swap(self, tile):
		# swap a tile with the blanl tile
		self.empty.value = tile.value
		tile.value = " "
		self.empty = tile

	def check(self):
		# create and update the list of values of tiles that can be moved
		self.neighbors = []
		for tile in self.board:
			if (tile.r - self.empty.r) ** 2 + (tile.c - self.empty.c) ** 2 == 1:
				self.neighbors.append(tile.value)

	def shuffle(self, rep = 500):
		# randomly choose tiles to swap with the blank tile to make sure the puzzle is solvable
		# repeat as many times as specified
		for i in range(rep):
			rand_nei = random.choice(self.neighbors)
			self.swap(self.tile_by_value(rand_nei))
			self.check()

	def win(self):
		# winning condition: all the tile values match their correct locations
		count = 0
		for tile in self.board:
			if tile.value == tile.r * self.size_col + (tile.c + 1):
				count += 1
		if count == self.size_row * self.size_col - 1:
			return True
		else:
			return False

	def play(self):
		while not self.win():
			os.system("clear")
			print(self)
			# ask player to choose a tile to move
			# error checking: number, in board range
			choice = input("Please choose a tile to move: ")
			while not (choice.isdigit() and int(choice) in range(self.size_row * self.size_col)):
				choice = input("Cannot be moved. Please choose another: ")
			# if the chosen tile is movable, swap and update the neighbors list
			if int(choice) in self.neighbors:
				self.swap(self.tile_by_value(int(choice)))
				self.check()			
			if self.win():
				os.system("clear")
				print(self)
				print("You win.")