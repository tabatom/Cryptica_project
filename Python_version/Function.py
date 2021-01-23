import numpy as np

# N.B.: conventions to identify floor, rocks and walls:
#		1,2,3,4	are the special rocks
#		0		is the floor
#		7		are the walls
#		6		are the rocks that can be moved but that do not require a special ending position


# boolean move to left: returning TRUE if something has changed (if nothing changed, the move can be skipped)
def move_left(matrix):

	# this boolean flags if the move has been done; if not, the move return false and in the main the code will skip the sequence of moves because, throughout the call to "move" function, no real move has been done
	moved = False
	
	# start by moving the first colomn on the left, thus next columns are already updated when moving
	# towards them, in the sense that if there would be "floor" on the right (because of a movement
	# of a preceding piece that was there) thus they can move.
	for row in np.arange(5):
		for col in np.arange(7):
			if (matrix[row][col] != 0 and matrix[row][col] != 7 and matrix[row][col-1] == 0):
				matrix[row][col-1] = matrix[row][col]
				# placing "floor" after the move
				matrix[row][col] = 0
				moved = True
	return moved;


# boolean move to right: returning TRUE if something has changed (if nothing changed, the move can be skipped)
def move_right(matrix):

	# this boolean flags if the move has been done; if not, the move return false and in the main the code will skip the sequence of moves because, throughout the call to "move" function, no real move has been done
	moved = False
	
	# start by moving the first colomn on the left, thus next columns are already updated when moving
	# towards them, in the sense that if there would be "floor" on the right (because of a movement
	# of a preceding piece that was there) thus they can move.
	for row in np.arange(5):
		for col in np.arange(5,-1,-1):		# col starts from 5 because: the indeces in arrays are lowered by 1 w.r.t. the position, so the last colomn has index = 6; we want to avoid verifying the rightest elements because for sure they can't move right
			if (matrix[row][col] != 0 and matrix[row][col] != 7 and matrix[row][col+1] == 0):
				matrix[row][col+1] = matrix[row][col]
				# placing "floor" after the move
				matrix[row][col] = 0
				moved = True
	return moved;


# boolean move to up: returning TRUE if something has changed (if nothing changed, the move can be skipped)
def move_up(matrix):

	# this boolean flags if the move has been done; if not, the move return false and in the main the code will skip the sequence of moves because, throughout the call to "move" function, no real move has been done
	moved = False;

	# start by moving the first colomn on the left, thus next columns are already updated when moving
	# towards them, in the sense that if there would be "floor" on the right (because of a movement
	# of a preceding piece that was there) thus they can move.
	for row in np.arange(1,5):
		for col in np.arange(7):
			if (matrix[row][col] != 0 and matrix[row][col] != 7 and matrix[row-1][col] == 0):
				matrix[row-1][col] = matrix[row][col]
				# placing "floor" after the move
				matrix[row][col] = 0
				moved = True

	return moved;


# boolean move to down: returning TRUE if something has changed (if nothing changed, the move can be skipped)
def move_down(matrix):

	# this boolean flags if the move has been done; if not, the move return false and in the main the code will skip the sequence of moves because, throughout the call to "move" function, no real move has been done
	moved = False;

	# start by moving the first colomn on the left, thus next columns are already updated when moving
	# towards them, in the sense that if there would be "floor" on the right (because of a movement
	# of a preceding piece that was there) thus they can move.
	for row in np.arange(3,-1,-1):
		for col in np.arange(0,7):
			if (matrix[row][col] != 0 and matrix[row][col] != 7 and matrix[row+1][col] == 0):
				matrix[row+1][col] = matrix[row][col]
				# placing "floor" after the move
				matrix[row][col] = 0
				moved = True

	return moved


# defining the matrix reader function
def read_matrix(ifile_):

	matrix = np.ones(shape=(5,7))
	ii = 0
	for line in ifile_:
		matrix[ii] = line.split()
		ii += 1
	return matrix


# function to translate the current number into a readable move string
def dump_number_to_moves_string(cod_move, moves):
	while(moves > 0):
		move = (3 * pow(4, moves-1))
		move = move & cod_move

		move >>= 2*(moves-1)
		
		switcher = {
			0: 'L',
			1: 'R',
			2: 'D',
			3: 'U'
		}

		print(switcher.get(move, "?"), end='')
		moves = moves - 1
	
	print("")
	return


# function to translate the current number into a readable move string
#	N.B.: the number is intended to be coded as the reverse string of moves
def dump_reverse_number_to_moves_string(cod_move, moves_to_show):

	while(moves_to_show > 0):

		move = 3 & cod_move;
		
		switcher = {
			0: 'L',
			1: 'R',
			2: 'D',
			3: 'U'
		}
		
		print(switcher.get(move, "?"), end='')
		
		cod_move = cod_move >> 2
		moves_to_show = moves_to_show - 1
	
	print("")
	return


# function to manually copying the matrix (element by element, to avoid pointers issues)
def check_result(_target_, _matrix_):
	for row in np.arange(0,5):
		for col in np.arange(0,7):
			if (_target_[row][col] != 0):
				if (_target_[row][col] != _matrix_[row][col]): return False
	return True


# function to print file error
def print_file_error():
	print("There is no input file specified: please, use the following syntax:\n \">>>./Cryptica input FILENAME moves NUM_MOVES\".\n\nBe sure that the file is in the correct folder.")
	return


#function to print moves error
def print_num_moves_error():
	print("Missing number of moves required: please, use the following syntax:\n\n>>>./Cryptica input FILENAME moves NUM_MOVES\".")
	return
