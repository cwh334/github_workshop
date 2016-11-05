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
		return ("*" + "-" * 5 + "*" + "\n" \
		+ "|" + "{0}{1}" + " " * (6 - len(str({self.rank}))) + "|" + "\n" \
		+ ("|" + " " * 5 + "|" + "\n") * 2 \
		+ "|" + " " * (6 - len(str({self.rank}))) + "{0}{1}" + "|" + "\n" \
		+ "*" + "-" * 5 + "*" + "\n").format(self.suit, self.rank)
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

class Deck:
# Each deck with 52 cards, identitical unless shuffled
	def __init__(self, full = True):
		self.deck = []
		if full == True:
			for suit in suits:
				for rank in ranks:
					self.deck.append(Card(suit, rank))
	def __str__(self):
		tmp = ""
		for card in self.deck:
			tmp += str(card)
		return tmp
	
	def shuffle(self):
		shuffle(self.deck)

	def distribute(self):
		a = []
		b = []
		self.shuffle()
		for i in range(len(self.deck)):
			if i % 2 == 0:
				a.append(self.deck[i])
				print (self.deck[i])
			else:
				b.append(self.deck[i])
		deck_1 = Deck(False)
		deck_2 = Deck(False)
		self.deck_1 = a
		self.deck_2 = b
		return deck_1, deck_2

d = Deck()
a, b = d.distribute()
print(b)
print(len(b.deck))

