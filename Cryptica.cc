#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <math.h>
#include <vector>
#include <bits/stdc++.h>

#include "functions.h"

using namespace std;

int main(int argc, char* argv[])
{
	cout << "\nStarting...\n" << endl;

	string directory = "Levels/";
	string targets = "_targets";

	// collecting all possible info
	vector<string> args;
	args.resize(argc);
	for ( int iarg = 1; iarg < argc; ++iarg ) args[iarg] = argv[iarg];
	
	
// ---------- INSTANTIATING ALL VARIABLES NEEDED ----------

	string init_moves = "";			// string of initial moves: crucial to avoid some computations
	string final_moves = "";		// string of final moves: crucial to avoid some computations
	string str_move = "";			// string of SOLUTION moves
	int less_moves = 0;			// int that counts how many moves the algorithm can skip
	int num_moves = 0;			// total number of moves
	string name = "";				// name of the level: tha program already has the folder and the respective target file set
	int env[5][7];				// matrix of the initial environment
	int target[5][7];				// matrix of the final positions of the "special" rocks
	int work[5][7];				// copy of env to be modified at every iteration; at the beginning of every iteration this would be resetted by copying env
	
// ---------- READING INPUT STRING ----------
	
	int cont_info = 0;
	while (cont_info < argc)
	{
		// selecting and opening input file
		if (args[cont_info] == "input")
		{
			// opening environment file
			name = args[cont_info+1];
			ifstream file_env( directory + name );
	
			// check if file is open
			if (not( file_env.is_open()))
			{
				cout << "\nError during environment file opening...\n" << endl;
				return 1;
			}
			
			// opening target file	
			ifstream file_target( directory + name + targets );

			// check if file is open
			if (not( file_target.is_open()))
			{
				cout << "\nError during target file opening...\n" << endl;
				return 1;
			}
			
			// building environmnet matrix from file
			int** env_app = read_matrix(file_env);

			// copying matrix to avoid using dynamic allocated memory
			for (int row = 0; row < 5; row++)
			{		
				for (int col = 0; col < 7; col++)
				{
					env[row][col] = env_app[row][col];
				}
			}

			// deallocating allocated memory
			delete_matrix(env_app);

			// closing file after read it
			file_env.close();
			
			
			// building target matrix from file
			int** target_app = read_matrix(file_target);
	
			// copying matrix to avoid using dynamic allocated memory
			for (int row = 0; row < 5; row++)
			{		
				for (int col = 0; col < 7; col++)
				{
					target[row][col] = target_app[row][col];
				}
			}
	
			// deallocating allocated memory
			delete_matrix(target_app);
	
			// closing file after read it
			file_target.close();


			// copying matrix (to keep the original one)
			for (int row = 0; row < 5; row++)
			{		
				for (int col = 0; col < 7; col++)
				{
					work[row][col] = env[row][col];
				}
			}
	
			cout << "Files opened...\n" << endl;
		}
		
		if (args[cont_info] == "moves")
		{
			// getting number of moves
			const string n = args[cont_info+1];
			stringstream sstr;
			sstr.str(n);
			sstr >> num_moves;
			sstr.clear();
		}
		
		// collecting starting moves
		if (args[cont_info] == "start")
		{
			init_moves = args[cont_info+1];
			less_moves += init_moves.length();
		}
		
		// collecting final moves
		if (args[cont_info] == "final")
		{
			final_moves = args[cont_info+1];
			less_moves += final_moves.length();
		}
		
		cont_info++;
	}

	cout << "Number of moves is: " << num_moves << endl << endl;

	cout << "Ended initialization...\n" << endl;

// ---------- ENDED INITIALIZZATION ----------

// ---------- CHECKING ERRORS OR NOT INITIALIZED THINGS ----------

	if (name == "")
	{
		print_file_error();
		return 1;
	}

	if (num_moves == 0)
	{
		print_num_moves_error();
		return 1;
	}

// ---------- TRANSLATING INITIAL AND FINAL MOVES INTO NUMBERS ----------

// N.B.: moves will be read in reverse order, so here one have to initialize them in reverse so that
//		then they will be read in the correct order

	// long long tail_moves_bits = 0;
	unsigned long long tail_moves_bits = 0;
	unsigned long long app = 0;
	
	int index_move = num_moves - 1;

	// adding initial moves
	if (init_moves.length() != 0)
	{
		for (char &c : init_moves)
		{
			switch(c)
			{
				case('L'):
				//tail_moves_bits += 0;
				//countL++;
				break;
				
				case('R'):
				tail_moves_bits += 1 * pow(4, index_move);
				//countR++;
				break;
				
				case('D'):
				tail_moves_bits += 2 * pow(4, index_move);
				//countD++;
				break;
				
				case('U'):
				tail_moves_bits += 3 * pow(4, index_move);
				//countU++;
				break;
			}
			
			index_move--;
		}
	}

	// moving index_move to the "first final move position"
	//	the "-1" is due to the fact that index_move is updated also
	//	during the insert of last initial move
	index_move -= num_moves - less_moves;

	// debugging
	cout << "Checking initial moves:" << endl;
	dump_number_to_moves_string(tail_moves_bits, num_moves);

	// adding reverse final moves
	if (final_moves.length() != 0)
	{
		for (char &c : final_moves)
		{
			switch(c)
			{
				case('L'):
				//tail_moves_bits += 0;
				//countL++;
				break;
				
				case('R'):
				tail_moves_bits += 1 * pow(4, index_move);
				//countR++;
				break;
				
				case('D'):
				tail_moves_bits += 2 * pow(4, index_move);
				//countD++;
				break;
				
				case('U'):
				tail_moves_bits += 3 * pow(4, index_move);
				//countU++;
				break;
			}
			index_move--;
		}
	}
	

// ---------- CHECKING tail_moves_bits IS CORRECT ----------

	// to verify the string is correct
	cout << "\nChecking initial and final moves:\n";
	dump_number_to_moves_string(tail_moves_bits, num_moves);
	cout << "\n" << endl;

// ---------- PREPARING TO WORK ----------

	// numbers of string of moves to try (given initial and final moves)
	unsigned long long lim_move = pow(4, (num_moves-less_moves));
	
	// debugging info
	cout << "\n\tOperating on:\n\t\t" << lim_move << " move codes" << "\n" << endl;
	
	// this is the counter to "trace" the moves
	unsigned long long move_generator = 0;
	
	// this is the "move variable" that can be modified in the loop
	unsigned long long code_move = 0;
	
	// left shift to be applied on each generated code_move to correctly sum it with tail_moves_bytes
	int init_len = init_moves.length();
	int fin_len = final_moves.length();
	
	// looking for the minima of different moves needed to solve the level (if 1 rock is away from his position of 3 "left moves" then in the string there must be at least 3 "L")
	int numL = 0, numR = 0, numU = 0, numD = 0;
	
	for (int row = 0; row < 5; row++)
	{
		for (int col = 0; col < 7; col++)
		{
			if (target[row][col] != 0)	// in target matrix all elements are 0 but the final positions of the rocks
			{
				int t = target[row][col];
				int tnumL = 0, tnumR = 0, tnumU = 0, tnumD = 0;
				
				for (int row_ = 0; row_ < 5; row_++)
				{
					for (int col_ = 0; col_ < 7; col_++)
					{
						// looking for the element that has to go in that position
						if (t == env[row_][col_])
						{
							// saving the minimum number of moves in the "respective" direction
							if (row_-row < 0)
							{
								tnumD = row-row_;
							}
							else
							{
								tnumU = row_-row;
							}
						
							if (col_-col < 0)
							{
								tnumR = col-col_;
							}
							else
							{
								tnumL = col_-col;
							}
						}
					}
				}
				
				// saving only the maxima number of minimum moves
				if (tnumD > numD)	numD = tnumD;
				if (tnumU > numU)	numU = tnumU;
				if (tnumR > numR)	numR = tnumR;
				if (tnumL > numL)	numL = tnumL;
			}
		}
	}
	
	// debugging
	cout << "Expected number of moves is:\n" << "\nR: " << numR << "\nL: " << numL << "\nU: " << numU << "\nD: " << numD << endl;
	
	int cont_move = 0;
		
	// mask to catch the first moves and check some patterns in them
	unsigned long long mask1 = 3 * pow(4, num_moves - 1);			// mask to count the moves
	unsigned long long mask2 = 63 * pow(4, num_moves - 1 - 2); 		// mask to check following combinations of moves: UDU, DUD, RLR, LRL
	unsigned long long mask3 = 1023 * pow(4, num_moves - 1 - 4);	// mask to check: UUUUU, DDDDD
	unsigned long long mask4 = 16383 * pow(4, num_moves - 1 - 6);	// mask to check: RRRRRRR, LLLLLLL
	unsigned long long check1;
	unsigned long long check2;
	unsigned long long check3;
	unsigned long long check4;



// ---------- STARTING TO GENERATE MOVES AND TO TRYING THEM ----------

	short print = 0;

	while(move_generator < lim_move)
	{
		// to see the proceding of the process
		if (move_generator > lim_move/4 and move_generator < lim_move/2 and print == 0)
		{
			cout << "Verified about 1/4 of the strings..." << endl;
			print++;
		}
		else if ((move_generator > lim_move/2) and print == 1)
		{
			cout << "Verified about 2/4 of the strings..." << endl;
			print++;
		}
		else if ((move_generator > 3*lim_move/4) and print == 2)
		{
			cout << "Verified about 3/4 of the strings..." << endl;
			print++;
		}

		copy_matrix(env, work);
		
		// creating move (left moving "move_generator" such that it is "in the centre" w.r.t. tails)
		code_move = (move_generator << 2*fin_len) + tail_moves_bits;
		
		// praparing to loop over "code_move"
		cont_move = 0;
		
		// Resetting masks
		mask1 = 3 * pow(4, num_moves - 1);			// mask to count the moves
		mask2 = 63 * pow(4, num_moves - 1 - 2); 	// mask to check following combinations of moves: UDU, DUD, RLR, LRL
		mask3 = 1023 * pow(4, num_moves - 1 - 4);	// mask to check: UUUUU, DDDDD
		mask4 = 16383 * pow(4, num_moves - 1 - 6);	// mask to check: RRRRRRR, LLLLLLL
		
	// debugging
	//	cout << "------------------------------------------" << endl;
	//	dump_number_to_moves_string(tail_moves_bits, num_moves);
	//	dump_number_to_moves_string(code_move, num_moves);
		

		// bool to skip test in case the move string is not ok
		bool testing = true;
		
		// checking if there are at least the needed moves as explained before
		int countR = 0, countL = 0, countU = 0, countD = 0;
		
		while ((testing) and (cont_move < num_moves))
		{
			// first masking: counting moves
			check1 = mask1 & code_move;
			check1 >>= 2*(num_moves - cont_move - 1);
			
			switch(check1)
			{
				case(0):
				countL++;
				break;
				
				case(1):
				countR++;
				break;
				
				case(2):
				countD++;
				break;
				
				case(3):
				countU++;
				break;
			}

		
			// second masking (to do only if there are at least 3 moves (6 bits) )
			//if (testing and cont_move < num_moves - 2)
			if (cont_move < num_moves - 2)
			{
				check2 = mask2 & code_move;
				check2 >>= 2*(num_moves - cont_move - 1 - 2);

				// LRL = 0b000100 = 4		skipping from LRL... to LRR...
				// RLR = 0b010001 = 17		skipping from RLR... to RLD...
				// DUD = 0b101110 = 46		skipping from DUD... to DUU...
				// UDU = 0b111011 = 59		skipping from UDU... to UUL... (automatic due to the order L,R,D,U)

				// If a pattern is found, then change last move and restart
				//	Example: ...RLR...  -->  ...RLD...
				//	In this way the program skips all the moves starting wrong
				//	N.B.: the variable to be changed is move_generator
				//			and it has to be done in the proper way
				
				if (check2==4 or check2==17 or check2==46 or check2==59)
				{
					move_generator += 1 * pow(4, num_moves - 1 - fin_len - cont_move - 2);
					testing = false;
					//cout << "Skipping at mask2" << endl;
					// skipping every successive evaluation
					//continue;
				}
			}

			
			// third masking (to do only if there are at least 5 moves (10 bits) )
			if (testing and cont_move < num_moves - 4)
			{
				check3 = mask3 & code_move;
				check3 >>= 2*(num_moves - cont_move - 1 - 4);
				
				// DDDDD = 0b1010101010 = 682		skipping from DDDDD... to DDDDU...
				// UUUUU = 0b1111111111 = 1023		skipping from ...UUUUU... to ..XLLLLL... (automatic due to the order L,R,D,U)
				//											X = successive move before the UUUUU pattern
				
				// If a pattern is found, then change last move and restart
				//	Example: ...DDDDD...  -->  ...DDDDU...
				
				if (check3==682 or check3==1023)
				{
					move_generator += 1 * pow(4, num_moves - 1 - fin_len - cont_move - 4);
					testing = false;
					//cout << "Skipping at mask3" << endl;
					// skipping every successive evaluation
					//continue;
				}
			}
	
			// fourth masking (to do only if there are at least 7 moves (14 bits) )
			if (testing and cont_move < num_moves - 6)
			{
				check4 = mask4 & code_move;
				check4 >>= 2*(num_moves - cont_move - 1 - 6);
				
				// LLLLLLL = 0b00000000000000 = 0		skipping from LLLLLLL... to LLLLLLR...
				// RRRRRRR = 0b01010101010101 = 5461	skipping from RRRRRRR... to RRRRRRU... (automatic due to the order L,R,D,U)
				
				// If a pattern is found, then change last move and restart
				//	Example: ...LLLLLLL...  -->  ...LLLLLLR...
				
				if (check4==0 or check4==5461)
				{
					move_generator += 1 * pow(4, num_moves - 1 - fin_len - cont_move - 6);
					testing = false;
					//cout << "Skipping at mask4 " << check4 << endl;
					// skipping every successive evaluation
					//continue;
				}
			}
	
	// debugging
	//		if (testing)	cout << "Testing mask4: " << testing << endl;

			// updating masks and cont_move at end of loop
			mask1 >>= 2;
			mask2 >>= 2;
			mask3 >>= 2;
			mask4 >>= 2;
			cont_move++;
		}
		
	// debugging
	//	cout << code_move << endl;

		// if there are not enough moves in a specific direction then the program does not try that string
		if (testing and ((countR < numR) or (countL < numL) or (countU < numU) or (countD < numD)))
		{
			testing = false;
			move_generator++;
			// cout << "Skipping because of not enough moves" << endl;
			continue;
		}

		// if testing is true then I can test the code_move
		if (testing)
		{
			mask1 = 3 * pow(4, num_moves - 1);			// mask to execute the moves
			//code_move = (move_generator << 2*fin_len) + tail_moves_bits;
			int test_move = 0;
			
	// debugging
	//		cout << "While testing: " << code_move << endl;
			
			while (testing and test_move < num_moves)	//no_test
			{
				check1 = mask1 & code_move;
				check1 >>= 2*(num_moves - test_move - 1);
				
				switch(check1)
				{
					case(0):
					testing = move_left(work);
					break;
					
					case(1):
					testing = move_right(work);
					break;
					
					case(2):
					testing = move_down(work);
					break;
					
					case(3):
					testing = move_up(work);
					break;
				}
				
				if (not testing)
				{
					// mettere update mosse in modo tale da saltare alle prossime
					move_generator += 1 * pow(4, num_moves - 1 - fin_len - test_move);
					//print1 = 1;
					//dump_number_to_moves_string(code_move, num_moves);
					//cout << test_move;
				}
				
				mask1 >>= 2;
				test_move++;
			}
		}


		// function that checks if all elements of the matrices are equal
		if (testing and check_result(target,work))
		{
			mask1 = 3 * pow(4, num_moves - 1);
			//code_move = (move_generator << 2*fin_len) + tail_moves_bits;
			cont_move = 0;
		
			while (cont_move < num_moves)
			{
				check1 = mask1 & code_move;
				check1 >>= 2*(num_moves - cont_move - 1);
			
				// N.B.: here one can create the final string by adding initial move string, masking only "move_generator", then add final_move string
				switch(check1)
				{
					case(0):
					str_move = str_move + "L";
					//countL++;
					break;
				
					case(1):
					str_move = str_move + "R";
					//countR++;
					break;
				
					case(2):
					str_move = str_move + "D";
					//countD++;
					break;
				
					case(3):
					str_move = str_move + "U";
					//countU++;
					break;
				}
			
				mask1 >>= 2;
				cont_move++;
			}
			
			cout << "\nThe solution is: " << str_move << endl;
			
			// alarm for finishing
			system("paplay /usr/share/sounds/sound-icons/trumpet-12.wav");
			
			return 0;
		}
		else
		{
			move_generator++;
		}
		
	// debugging
	//	cout << testing << "\n\n\n\n";
	//	if (testing)
	//	{
	//		dump_matrix(work);
	//		cout << "\n\n\n";
	//	}
	}
	
	system("paplay /usr/share/sounds/sound-icons/xylofon.wav");
	
	cout << "\nDone." << endl;
	
	return 0;
}
