size = 8

coordinates = []
for r in range(size):
	for c in range(size):
		coordinates.append([r, c])


probability = {}

def count_comb(coordinate, row, col):
	# Count how many spaces there are consecutively (horizontal or vertical at a time) max 7
	# total spaces - 3 = the number of combinations
	count_a = 1
	count_b = 1
	row_next = coordinate[0] + row
	col_next = coordinate[1] + col
	while count_a != 4:
		print(count_a, count_b, row_next, col_next)
		if [row_next, col_next] in coordinates:
			count_a += 1
			row_next += row
			col_next += col
		else:
			break
	row_next = coordinate[0] - row
	col_next = coordinate[1] - col	
	while count_b != 4:
		print(count_a, count_b, row_next, col_next)
		if [row_next, col_next] in coordinates:
			count_b += 1
			row_next -= row
			col_next -= col
		else:
			break
	print("count", count_a, count_b)
	return(count_a + count_b - 4)

def create_dict(dictionary, coordinate):
	dictionary[str(coordinate[0]) + "," + str(coordinate[1])] = count_comb(coordinate, 1, 0)
	print(dictionary)
	dictionary[str(coordinate[0]) + "," + str(coordinate[1])] += count_comb(coordinate, 0, 1)
	print(dictionary)

	return(dictionary)
for c in coordinates:
	print(create_dict(probability, c))
