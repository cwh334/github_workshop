import network
import random,time,os

name = input ("Please enter your name")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
# hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)

while True:
	################################################################################
	# Opponents time to hit (waiting for opponent hit)
	# - either you will lose
	# - or opponent hit empty location or a ship location
	# - or opponent hit a mine 
	# 	- You get additional info about a nearby location to the opponent's ship
	################################################################################
	ans = network.receive()

	if ans == 'lost':
		break
	elif ans != None:
		ans = list(map(int,ans.split(',')))
		print (ans[0],ans[1], "is nearby location of the ship")

	################################################################################
	# Your turn to hit
	# You will get back either ' ', 'x', 'M'
	#
	# need to make your own logic to come up with a string "r,c" to send to opponent
	################################################################################
	guess = input("enter coordinates r,c: ")

	ans = network.send(guess)

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

