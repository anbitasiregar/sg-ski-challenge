# Anbita Siregar (anbitasiregar@gmail.com)
# Singapore Ski problem
# Uses 2-d dynamic programming to find the longest decreasing subsequence of map

mountain_map = []   # store 2d map 
longest_path = []   # store longest path for each cell
final_longest_path = 0
ski_paths = []   # store what the actual longest paths are
steepness = []   # store steepness of each path in case there's a tie

f = open("sgskitestcase", "r")

for line in f:
	new_row = [int(x) for x in line.split(" ") if x != "\n"]   # get new row from txt file
	if len(new_row) == 2:   # not part of the grid -- just how many rows/cols
		continue

	mountain_map += [new_row]   # add new_row to 2d grid
	longest_path += [[0] * len(new_row)]   # initialize longest_path


# finds longest path for node in row_num, col_num
def ski_down(row_num, col_num):
	current_node = mountain_map[row_num][col_num]

	if longest_path[row_num][col_num] == 0:
		longest = 0

		for adj_row in [-1, 1]:   # get north, south node from current_node if there is one (corner case)
			new_row_num = row_num + adj_row
			if new_row_num < 0 or new_row_num >= len(mountain_map[0]):
				continue

			adj_node = mountain_map[new_row_num][col_num]
			if adj_node < current_node:
				current_path = ski_down(new_row_num, col_num)
				if current_path > longest:   # if recursive call is > longest, we have a new longest_path
					longest = current_path


		for adj_col in [-1, 1]:   # get east, west node from current_node if there is one (corner case)
			new_col_num = col_num + adj_col
			if new_col_num < 0 or new_col_num >= len(mountain_map[0]):
				continue

			adj_node = mountain_map[row_num][new_col_num]
			if adj_node < current_node:
				current_path = ski_down(row_num, new_col_num)
				if current_path > longest:   # if recursive call is > longest, we have a new longest_path
					longest = current_path

		longest_path[row_num][col_num] = longest + 1   # add one because we're adding current_node to longest path

	return longest_path[row_num][col_num]


def reverse_path(row_num, col_num, current_longest_length):
	if current_longest_length == 0:   # base case: we've hit the last node
		return [mountain_map[row_num][col_num]]

	current_node = mountain_map[row_num][col_num]

	for adj_row in [-1, 1]:
		new_row_num = row_num + adj_row
		if new_row_num < 0 or new_row_num >= len(mountain_map[0]):
			continue

		adj_node = mountain_map[new_row_num][col_num]
		adj_length = longest_path[new_row_num][col_num]

		if adj_length == current_longest_length:   # check if node is next in path
			new_ski_path = reverse_path(new_row_num, col_num, current_longest_length - 1)
			return [current_node] + new_ski_path   # add current node to path result of recursive call

	for adj_col in [-1, 1]:   # get east, west node from current_node if there is one (corner case)
		new_col_num = col_num + adj_col
		if new_col_num < 0 or new_col_num >= len(mountain_map[0]):
			continue

		adj_node = mountain_map[row_num][new_col_num]
		adj_length = longest_path[row_num][new_col_num]

		if adj_length == current_longest_length:   # check if node is next in path
			new_ski_path = reverse_path(row_num, new_col_num, current_longest_length - 1)
			return [current_node] + new_ski_path   # add current node to path result of recursive call


# main function

# get longest path for each node, check if that path is the longest
for row_num in range(len(mountain_map)):
	for col_num in range(len(mountain_map[0])):
		current_node = mountain_map[row_num][col_num]
		current_longest_path = ski_down(row_num, col_num)
		if current_longest_path > final_longest_path:
			final_longest_path = current_longest_path


# Once we know the maximum longest_path, reverse to find actual path
for row_num in range(len(mountain_map)):
	for col_num in range(len(mountain_map[0])):
		current_node = mountain_map[row_num][col_num]
		if longest_path[row_num][col_num] == final_longest_path:   # start of one of longest paths
			new_ski_path = reverse_path(row_num, col_num, final_longest_path - 1)
			ski_paths += [new_ski_path]
			steepness += [current_node]

print final_longest_path
if len(ski_paths) > 1:   # need a tie-breaker, ski path with highest initial steepness
	max_steepness = max(steepness)
	index = steepness.index(max_steepness)
	print ski_paths[index][0] - ski_paths[index][-1]
else:
	print ski_paths[0][0] - ski_paths[0][-1]





