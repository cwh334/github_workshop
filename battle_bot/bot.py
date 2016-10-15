def count_sep(list_pool, coordinate, row, col):
	# Count how many spaces there are consecutively (horizontal or vertical at a time) max 7
	# total spaces - 3 = the number of combinations
	count_a = 1
	count_b = 1
	row_next = coordinate[0] + row
	col_next = coordinate[1] + col
	while count_a != 4:
		if [row_next, col_next] in list_pool:
			count_a += 1
			row_next += row
			col_next += col
		else:
			break
	row_next = coordinate[0] - row
	col_next = coordinate[1] - col	
	while count_b != 4:
		if [row_next, col_next] in list_pool:
			count_b += 1
			row_next -= row
			col_next -= col
		else:
			break
	return(count_a + count_b - 4)

def count(list_pool, coordinate):
	# Add up horizontal and vertical possibilities
	return(count_sep(list_pool, coordinate, 1, 0) + count_sep(list_pool, coordinate, 0, 1))

def arrange(list_pool, result):
	# According to the result of a guess, arrange the coordinates into corresponding lists
	if result == " ":
		list_pool.remove(largest_prob)
	elif result == "x":
		ship_loc.append(list_pool.pop(list_pool.index(largest_prob)))
	else:
		mine_loc.append(list_pool.pop(list_pool.index(largest_prob)))

"""ship_loc = []
mine_loc = []
if ans != None:
	mine_loc.append(ans)

largest_prob = 0
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
			if count(coordinate) > largest_prob:
				largest_prob = coordinate
guess = ",".join(largest_prob)
arrange(network.sent(guess))"""

	

