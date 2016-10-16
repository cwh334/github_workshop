import network
import random,time,os
import bot

name = input ("Please enter your name: ")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
# hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)

""" Added code starts here to create a list of coordinates """
coordinates = []
for r in range(size):
	for c in range(size):
		coordinates.append([r, c])
# lists of found ship locations and nearby locations
ship_loc = []
near_loc = []
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
	# Added code to update the list of nearby locations
		near_loc.append(ans)
	# Your turn to hit
	# You will get back either ' ', 'x', 'M'		

	largest_prob = [-2, -2]
	random.shuffle(coordinates)
	for coordinate in coordinates:
		# Elimination
		condition = True
		# If no ship location is found yet, only compare the once near hinted nearby locations
		if len(ship_loc) == 0:
			for loc in near_loc:
				if abs(coordinate[0] - loc[0]) > 1 or abs(coordinate[1] - loc[1]) > 1:
					condition = False
		# If one ship location is found, compare only the four locations next to it
		elif len(ship_loc) == 1:
			for loc in ship_loc:
				if abs(loc[0] - coordinate[0]) + abs(loc[1] - coordinate[1]) > 1:
					condition = False
		# If more than 2 locations are found, compare only the two locations on the sides
		else:
			# horizontal
			if ship_loc[0][0] == ship_loc[1][0]:
				if not(coordinate[0] == ship_loc[0][0]) or\
				not(abs(coordinate[1] - ship_loc[0][1]) == 1 or\
					abs(coordinate[1] - ship_loc[-1][1]) == 1):
					condition = False
			# vertical
			else:
				if not(coordinate[1] == ship_loc[0][1]) or\
				not(abs(coordinate[0] - ship_loc[0][0]) == 1 or\
					abs(coordinate[0] - ship_loc[-1][0]) == 1):
					condition = False
		# After elimination, choose (one of) the locations with the most possible combinations			
		if condition == True:
			if bot.count(coordinates, coordinate) > bot.count(coordinates, largest_prob):
				largest_prob = coordinate
	guess = ",".join(list(map(str, largest_prob)))
	ans = network.send(guess)
	# Update lists 
	if ans == "x":
		ship_loc.append(largest_prob)
		ship_down = True
	else:
		coordinates.remove(largest_prob)
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

