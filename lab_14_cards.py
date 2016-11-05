from random import shuffle
from os import system

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
# Each deck with 52 cards, identitical unless shuffled.
# Default attribute full = True, with identical full deck. If full = False, it will be an empty deck.
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
		deck_1.deck = a
		deck_2.deck = b
		return deck_1, deck_2

	def __len__(self):
		return len(self.deck)

	def __getitem__(self, index):
		return self.deck[index]

	def pop(self, index = 0):
		return self.deck.pop(index)

	def append(self, item):
		self.deck.append(item)

# Create a deck for each player
original = Deck()
p1, p2 = original.distribute()

count = 26

while len(p1) != 0 and len(p2) != 0:
	print(p1[0], p2[0])
	if count == 0:
		p1.shuffle()
		p2.shuffle()
		count = 26
	if p1[0] == p2[0]:
		if count < 4:
			p1.shuffle()
			p2.shuffle()
			count = 26
		war_card = 4
		step = 4
		while p1[war_card] == p2[war_card]:
			if len(p1) < 4
			if count < 4:
				p1.shuffle()
				p2.shuffle()
				count = 26
			war_card += step
			count -= 4
		for i in range(war_card + 1):
			if p1[war_card] > p2[war_card]:
				p1.append(p1.pop())
				p1.append(p2.pop())
			else:
				p2.append(p1.pop())
				p2.append(p2.pop())
				
	else:
		if p1[0] > p2[0]:
			p1.append(p1.pop())
			p1.append(p2.pop())
		if p1[0] < p2[0]:
			p2.append(p1.pop())
			p2.append(p2.pop())
		count -= 1

if len(p1) == 0:
	print("Player 2 wins.")
elif len(p2) == 0:
	print("Player 1 wins.")






