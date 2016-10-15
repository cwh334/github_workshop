import network
import random,time,os
import bot

name = input ("Please enter your name")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
# hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)

""" Added code starts here to create a list of coordinates """
coordinates = []
for r in range(size):
	for c in range(size):
		coordinates.append([r, c])
""" Ends here """

while True:
	# Opponents time to hit (waiting for opponent hit)
	# - either you will lose
	# - or opponent hit empty location or a ship location
	# - or opponent hit a mine 
	# 	- You get additional info about a nearby location to the opponent's ship
	ans = network.receive()

	if ans == 'lost':
		break
	elif ans != None:
		ans = list(map(int,ans.split(',')))
		print (ans[0],ans[1], "is nearby location of the ship")

	# Your turn to hit
	# You will get back either ' ', 'x', 'M'

	ship_loc = []
	mine_loc = []
	if ans != None:
		mine_loc.append(ans)

	largest_prob = [-2, -2]
	random.shuffle(coordinates)
	for coordinate in coordinates:
		condition = True
		for loc in ship_loc:
			if abs(loc[0] - coordinate[0]) + abs(loc[1] - coordinate[1]) > 1:
				condition = False
		for loc in mine_loc:
			if not(abs(coordinate[0] - ans[0]) <= 1 and abs(coordinate[1] - ans[1]) <= 1):
				condition = False
		if condition == True:
			if bot.count(coordinates, coordinate) > bot.count(coordinates, largest_prob):
				largest_prob = coordinate
	guess = ",".join(list(map(str, largest_prob)))
	ans = network.send(guess)
	if ans == " ":
		coordinates.remove(largest_prob)
	elif ans == "x":
		ship_loc.append(coordinates.pop(coordinates.index(largest_prob)))
	else:
		mine_loc.append(coordinates.pop(coordinates.index(largest_prob)))

	# Ends here
	

	if ans == 'win':
		break
	elif ans == 'wrong input':
		print ("Your input was wrong")
	else:
		# assign result to board
		guessList = list(map(int,guess.split(',')))
		dispBoard[guessList[0]][guessList[1]]=ans


# Printing final result
if ans == 'win':
	guessList = list(map(int,guess.split(',')))
	dispBoard[guessList[0]][guessList[1]]='x'
	network.printBoard()
	print ("you have won the game")
else:
	network.printBoard()
	print ("you have lost the game")

