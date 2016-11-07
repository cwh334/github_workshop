from random import shuffle

suits = ["s", "h", "d", "c"]
ranks = []
for i in range(1, 14):
	ranks.append(i)

class Card:
# Each card has two attributes: a suit and a rank
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return "*------*\n|{0}{1}    |\n|      |\n|    {0}{1}|\n*------*".format(self.rank,self.suit)
# Compare cards be the rank, disregarding the suit
	def __gt__(self, target):
		if self.rank > target.rank:
			return True
		else:
			return False

	def __lt__(self, target):
		if self.rank < target.rank:
			return True
		else:
			return False
	def __eq__(self, target):
		if self.rank == target.rank:
			return True
		else:
			return False
	def __int__(self):
		return self.rank

class Deck:
	def __init__(self, full = True):
# Default attribute full = True, with identical full deck. If full = False, it will be an empty deck.
# Each deck with 52 cards, identitical unless shuffled.
		self.deck = []
		if full == True:
			for suit in suits:
				for rank in ranks:
					self.deck.append(Card(suit, rank))
	def __str__(self):
		tmp = ""
		for row in range(5):
			for c in self.deck:
				tmp += str(c).split("\n")[row] + " "
			tmp += "\n"
		return tmp
	
	def shuffle(self):
		shuffle(self.deck)

	def distribute(self):
# First shuffle and then distribute into two decks of 26 cards
		a = []
		b = []
		self.shuffle()
		for i in range(len(self.deck)):
			if i % 2 == 0:
				a.append(self.deck[i])
			else:
				b.append(self.deck[i])
		deck_1 = Deck(False)
		deck_2 = Deck(False)
		deck_1.deck = a
		deck_2.deck = b
		return deck_1, deck_2

	def __len__(self):
		return len(self.deck)
# The number of cards in the deck
	def __getitem__(self, index):
		return self.deck[index]
# Get a specific card by index
	def pop(self, index = 0):
# Remove and return the first card (default) in the deck. 
		return self.deck.pop(index)

	def append(self, item):
# Append cards to this deck
		self.deck.append(item)

	def merge(self, list):
# Merge a deck into this existing deck
		self.deck = self.deck + list

# Create a deck for each player
original = Deck()
p1, p2 = original.distribute()

counts = [26, 26]
decks = [p1, p2]
skip = 0
table = []

while len(p1) != 0 and len(p2) != 0:
# Count the number of cards left (unused). 
# When all cards in the player's hand are used, shuffle the cards won from the game into the usable deck.
	for i in range(len(counts)):
		if counts[i] == 0:
			counts[i] = len(decks[i])
			decks[i].shuffle()

	print(str(p1[0]) + str(p2[0]))
# Each players reveals their top card in the deck on the table
	for deck in decks:
		table.append(deck.pop())
# When the condition skip is on, the players are at war.
# The cards will not be compared until the forth one.
	if skip > 0:
		skip -= 1
# If there is a tie. The war condition is on (skip)
# The winner gets all the cards on the table
	else:
		if table[-2] == table[-1]:
			skip = 3
			print("Start of skips")
		elif table[-2] > table[-1]:
			p1.merge(table)
			table = []
		else:			
			p2.merge(table)
			table = []
# Cards used
	for count in counts:
		count -= 1
# Print temporary results after each round
	print(len(p1), len(p2))

# Whne one player loses all the cards, the player loses
if len(p1) == 0:
	print("Player 2 wins.")
elif len(p2) == 0:
	print("Player 1 wins.")
