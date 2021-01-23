import numpy as np
import sys
import os

from Function import *

print("\nStarting...\n")

directory = "../Levels/"
targets = "_targets"

# collecting all possible info
args = sys.argv

# ---------- INSTANTIATING ALL VARIABLES NEEDED ----------

init_moves = ""			# string of initial moves: crucial to avoid some computations
final_moves = ""		# string of final moves: crucial to avoid some computations
str_move = ""			# string of SOLUTION moves
less_moves = 0			# int that counts how many moves the algorithm can skip
num_moves = 0			# total number of moves
name = ""				# name of the level: tha program already has the folder and the respective target file set
env = np.zeros(shape=(5,7))		# matrix of the initial environment
target = np.zeros(shape=(5,7))		# matrix of the final positions of the "special" rocks
work = np.zeros(shape=(5,7))		# copy of env to be modified at every iteration; at the beginning of every iteration this would be resetted by copying env

# ---------- READING INPUT STRING ----------

cont_info = 0
while (cont_info < len(args)):
    # selecting and opening input file
    if (args[cont_info] == "input"):
        
        # opening environment file
        name = args[cont_info+1]
        
        try:
            ifile_env = open(directory + name)
        except:
            print("\nError during environment file opening...\n")
            sys.exit()

        # opening target file
        try:
            ifile_target = open(directory + name + targets)
        except:
            print("\nError during target file opening...\n")
            sys.exit()

        # building environmnet matrix from file
        env = np.array(read_matrix(ifile_env))

        # closing file after read it
        ifile_env.close()


        # building target matrix from file
        target = read_matrix(ifile_target)

        # closing file after read it
        ifile_target.close()

        # copying matrix (to keep the original one)
        work = env.copy()


        print("Files opened...\n")


    if (args[cont_info] == "moves"):
        # getting number of moves
        num_moves = int(args[cont_info+1])


    # collecting starting moves
    if (args[cont_info] == "start"):
        init_moves = args[cont_info+1]
        less_moves += len(init_moves)

    # collecting final moves
    if (args[cont_info] == "final"):
        final_moves = args[cont_info+1]
        less_moves += len(final_moves)

    cont_info += 1

print("Number of moves is:", num_moves, end="\n\n")

print("Ended initialization...\n")

# ---------- ENDED INITIALIZZATION ----------

# ---------- CHECKING ERRORS OR NOT INITIALIZED THINGS ----------

if (name == ""):
    print_file_error()
    sys.exit()

if (num_moves == 0):
    print_num_moves_error()
    sys.exit()

# ---------- TRANSLATING INITIAL AND FINAL MOVES INTO NUMBERS ----------

# N.B.: moves will be read in reverse order, so here one have to initialize them in reverse so that
#		then they will be read in the correct order

tail_moves_bits = 0
app = 0

index_move = num_moves - 1

# adding initial moves
if (len(init_moves) != 0):
    for c in init_moves:
        
        #if c=='L':
        #    tail_moves_bits += 0
        if c=='R':
            tail_moves_bits += 1 * pow(4, index_move)
        elif c=='D':
            tail_moves_bits += 2 * pow(4, index_move)
        elif c=='U':
            tail_moves_bits += 3 * pow(4, index_move)

        index_move -= 1

# moving index_move to the "first final move position"
#	the "-1" is due to the fact that index_move is updated also
#	during the insert of last initial move
index_move -= num_moves - less_moves;

# Printing moves till now (initial moves)
print("Dumping the translated code for initial moves:")
dump_number_to_moves_string(tail_moves_bits, num_moves);


# adding reverse final moves
if (len(final_moves) != 0):
    for c in final_moves:
        #if c=='L':
        #    tail_moves_bits += 0;
        if c=='R':
            tail_moves_bits += 1 * pow(4, index_move)
        elif c=='D':
            tail_moves_bits += 2 * pow(4, index_move)
        elif c=='U':
            tail_moves_bits += 3 * pow(4, index_move)

        index_move -= 1

# ---------- CHECKING tail_moves_bits IS CORRECT ----------

# to verify the string is correct
print("\nChecking initial and final moves:\n")
dump_number_to_moves_string(tail_moves_bits, num_moves)

# ---------- PREPARING TO WORK ----------

# numbers of string of moves to try (given initial and final moves)
lim_move = pow(4, (num_moves-less_moves))

# debugging info
print("\n\tOperating on:\n\t\t", lim_move, " move codes\n")

# this is the counter to "trace" the moves
move_generator = 0

# this is the "move variable" that can be modified in the loop
code_move = 0;

# left shift to be applied on each generated code_move to correctly sum it with tail_moves_bytes
init_len = len(init_moves)
fin_len = len(final_moves)

# looking for the minima of different moves needed to solve the level (if 1 rock is away from his position of 3 "left moves" then in the string there must be at least 3 "L")
numL, numR, numU, numD = 0, 0, 0, 0

for row in np.arange(0,5):
    for col in np.arange(0,7):
        if (target[row][col] != 0):	# in target matrix all elements are 0 but the final positions of the rocks
            t = target[row][col]
            tnumL, tnumR, tnumU, tnumD = 0, 0, 0, 0

            for row_ in np.arange(0,5):
                for col_ in np.arange(0,7):
                    # looking for the element that has to go in that position
                    if (t == env[row_][col_]):
                        # saving the minimum number of moves in the "respective" direction
                        if (row_-row < 0): 
                            tnumD = row-row_
                        else:
                            tnumU = row_-row

                        if (col_-col < 0):
                            tnumR = col-col_
                        else:
                            tnumL = col_-col


            # saving only the maxima number of minimum moves
            if (tnumD > numD):	numD = tnumD
            if (tnumU > numU):	numU = tnumU
            if (tnumR > numR):	numR = tnumR
            if (tnumL > numL):	numL = tnumL

# debugging
print("Expected number of moves is:\n"+"\nR:", numR, "\nL:", numL, "\nU:", numU, "\nD:", numD)

cont_move = 0

# mask to catch the first moves and check some patterns in them
mask1 = 3 * pow(4, num_moves - 1)			# mask to count the moves
mask2 = 63 * pow(4, num_moves - 1 - 2)		# mask to check following combinations of moves: UDU, DUD, RLR, LRL
mask3 = 1023 * pow(4, num_moves - 1 - 4)	# mask to check: UUUUU, DDDDD
mask4 = 16383 * pow(4, num_moves - 1 - 6)	# mask to check: RRRRRRR, LLLLLLL
check1 = 0
check2 = 0
check3 = 0
check4 = 0


# ---------- STARTING TO GENERATE MOVES AND TO TRYING THEM ----------

print_flag = 0

while (move_generator < lim_move):
    # to see the proceding of the process
    if (move_generator > lim_move/4 and move_generator < lim_move/2 and print_flag == 0):
        print("Verified about 1/4 of the strings...")
        print_flag += 1
    elif ((move_generator > lim_move/2) and print_flag == 1):
        print("Verified about 2/4 of the strings...")
        print_flag += 1
    elif ((move_generator > 3*lim_move/4) and print_flag == 2):
        print("Verified about 3/4 of the strings...")
        print_flag += 1

    #copy_matrix(env, work);

    work = env.copy()
    
    # creating move (left moving "move_generator" such that it is "in the centre" w.r.t. tails)
    code_move = (int(move_generator) << 2*fin_len) + tail_moves_bits

    # praparing to loop over "code_move"
    cont_move = 0

    # Resetting masks
    mask1 = 3 * pow(4, num_moves - 1)			# mask to count the moves
    mask2 = 63 * pow(4, num_moves - 1 - 2)		# mask to check following combinations of moves: UDU, DUD, RLR, LRL
    mask3 = 1023 * pow(4, num_moves - 1 - 4)	# mask to check: UUUUU, DDDDD
    mask4 = 16383 * pow(4, num_moves - 1 - 6)	# mask to check: RRRRRRR, LLLLLLL


    # bool to skip test in case the move string is not ok
    testing = True

    # checking if there are at least the needed moves as explained before
    countR, countL, countU, countD = 0, 0, 0, 0

    while ((testing) and (cont_move < num_moves)):
        # first masking: counting moves
        check1 = mask1 & code_move
        check1 >>= 2*(num_moves - cont_move - 1)

        if check1 == 0:
            countL += 1
        elif check1 == 1:
            countR += 1
        elif check1 == 2:
            countD += 1
        elif check1 == 3:
            countU += 1

        # second masking (to do only if there are at least 3 moves (6 bits) )
        if (cont_move < num_moves - 2):
            check2 = mask2 & code_move
            check2 >>= 2*(num_moves - cont_move - 1 - 2)

            # LRL = 0b000100 = 4			skipping from LRL... to LRR...
            # RLR = 0b010001 = 17			skipping from RLR... to RLD...
            # DUD = 0b101110 = 46			skipping from DUD... to DUU...
            # UDU = 0b111011 = 59			skipping from UDU... to UUL... (automatic due to the order L,R,D,U)

            # If a pattern is found, then change last move and restart
            #	Example: ...RLR...  -->  ...RLD...
            #	In this way the program skips all the moves starting wrong
            #	N.B.: the variable to be changed is move_generator
            #			and it has to be done in the proper way
            
            if check2 in (4, 17, 46, 59):
                move_generator += 1 * pow(4, num_moves - 1 - fin_len - cont_move - 2)
                testing = False
                # print("Skipping at mask2")


        # third masking (to do only if there are at least 5 moves (10 bits) )
        if (testing and cont_move < num_moves - 4):
            check3 = mask3 & code_move
            check3 >>= 2*(num_moves - cont_move - 1 - 4)

            # DDDDD = 0b1010101010 = 682		skipping from DDDDD... to DDDDU...
            # UUUUU = 0b1111111111 = 1023		skipping from ...UUUUU... to ..XLLLLL... (automatic due to the order L,R,D,U)
            #											X = successive move before the UUUUU pattern

            # If a pattern is found, then change last move and restart
            #	Example: ...DDDDD...  -->  ...DDDDU...
            
            if check3 in (682, 1023):
                move_generator += 1 * pow(4, num_moves - 1 - fin_len - cont_move - 4)
                testing = False
                # print("Skipping at mask3")


        # fourth masking (to do only if there are at least 7 moves (14 bits) )
        if (testing and cont_move < num_moves - 6):
            check4 = mask4 & code_move
            check4 >>= 2*(num_moves - cont_move - 1 - 6)

            # LLLLLLL = 0b00000000000000 = 0		skipping from LLLLLLL... to LLLLLLR...
            # RRRRRRR = 0b01010101010101 = 5461		skipping from RRRRRRR... to RRRRRRU... (automatic due to the order L,R,D,U)

            # If a pattern is found, then change last move and restart
            #	Example: ...LLLLLLL...  -->  ...LLLLLLR...
            
            if check4 in (0,5461):
                move_generator += 1 * pow(4, num_moves - 1 - fin_len - cont_move - 6)
                testing = False
                # print("Skipping at mask4")


        # updating masks and cont_move at end of loop
        mask1 >>= 2
        mask2 >>= 2
        mask3 >>= 2
        mask4 >>= 2
        cont_move += 1

    # if there are not enough moves in a specific direction then the program does not try that string
    if (testing and ((countR < numR) or (countL < numL) or (countU < numU) or (countD < numD))):
        testing = False
        move_generator += 1
        # print("Skipping because of not enough moves")
        continue

    # if testing is true then I can test the code_move
    if (testing):
        mask1 = 3 * pow(4, num_moves - 1)			# mask to execute the moves
        # code_move = (move_generator << 2*fin_len) + tail_moves_bits
        test_move = 0

        while (testing and test_move < num_moves):
            # no_test
            check1 = mask1 & code_move
            check1 >>= 2*(num_moves - test_move - 1)

            if check1 == 0:
                testing = move_left(work)
            elif check1 == 1:
                testing = move_right(work)
            elif check1 == 2:
                testing = move_down(work)
            elif check1 == 3:
                testing = move_up(work)

            if (not testing):
                # mettere update mosse in modo tale da saltare alle prossime
                move_generator += 1 * pow(4, num_moves - 1 - fin_len - test_move)
                # print1 = 1
                # dump_number_to_moves_string(code_move, num_moves)
                # cout << test_move

            mask1 >>= 2
            test_move += 1

    # function that checks if all elements of the matrices are equal
    if (testing and check_result(target,work)):
        mask1 = 3 * pow(4, num_moves - 1)
        # code_move = (move_generator << 2*fin_len) + tail_moves_bits
        cont_move = 0

        while (cont_move < num_moves):
            check1 = mask1 & code_move
            check1 >>= 2*(num_moves - cont_move - 1)

            # N.B.: here one can create the final string by adding initial move string, masking only "move_generator", then add final_move string
            if check1 == 0:
                str_move = str_move + "L"
            elif check1 == 1:
                str_move = str_move + "R"
            elif check1 == 2:
                str_move = str_move + "D"
            elif check1 == 3:
                str_move = str_move + "U"

            mask1 >>= 2
            cont_move += 1

        print("\nThe solution is:", str_move)

        # alarm for finishing
        os.system("paplay /usr/share/sounds/sound-icons/trumpet-12.wav");
        
        sys.exit()
    else:
        move_generator += 1

os.system("paplay /usr/share/sounds/sound-icons/xylofon.wav");

print("\nDone.")
