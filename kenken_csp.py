from csp import *   #implemented csp algorithms
from collections import OrderedDict
import sys          #read command line arguments
import time         #time for metrics
import ast
import numpy as np
#import pandas as pd
import os


class myKenken(CSP):

    def __init__(self, input_data):
        self.variables = []             #done
        self.size_of_puzzle = 0         #done
        self.domain = {}                #done
        self.clique = {}                #done
        self.inside_same_clique = {}    #done
        self.neighbors_col_row = {}     #done
        self.clique_number = {}         #done

        #read input file
        file = open(input_data, "r")
        input_data = file.readlines()
        file.close()

        #read size of Kenken puzzle
        line = input_data[0]
        self.size_of_puzzle = int(line.strip('\n'))
        counter_list = []

        #create variables (every cell of Kenken puzzle)
        rest_lines = input_data[1:]
        counter = 0
        for line in rest_lines:
            line = line.strip()
            line = line.split("|")
            math_number = int(line[0])
            math_symbol = line[1]
            self.clique[counter] = [math_number, math_symbol, []]
            tuples = line[2:]
            counter_list.append(counter)
            for tuple in tuples:
                input_tuple = tuple.split(",")
                cur_tuple = (int(input_tuple[0]), int(input_tuple[1]))
                self.clique[counter][2].append(cur_tuple)
                self.clique_number[cur_tuple] = counter
                self.variables.append(cur_tuple)
            counter += 1
        self.variables.extend(counter_list)

        # creating neighbors of same row and column
        for i in range(self.size_of_puzzle):  # row
            for j in range(self.size_of_puzzle):  # col
                #print(i, j)
                self.neighbors_col_row[(i, j)] = self.get_neighbors_constraints(i, j)
                #print(self.neighbors_col_row[(i, j)])
                try:
                    self.neighbors_col_row[(i, j)].append(self.clique_number[(i, j)])
                except:
                    print("'{}', '{}'".format(i, j))
                    print(self.clique_number[(i, j)])
                    sys.exit()
        for i in range(len(self.clique)):
            self.neighbors_col_row[i] = self.clique[i][2]

        # create domain
        for i in range(self.size_of_puzzle):  # row
            for j in range(self.size_of_puzzle):  # col
                tuple = (i, j)
                self.domain[tuple] = []
                for k in range(1, self.size_of_puzzle + 1):
                    self.domain[tuple].append(k)
        # create domain again
        cur_list = []
        value_list = [x for x in range(1, self.size_of_puzzle + 1)]
        for cur_clique in self.clique:
            for i in range(len(self.clique[cur_clique][2])):
                cur_list.extend(value_list)
            possible_combinations = [x for x in itertools.permutations(cur_list, r=len(self.clique[cur_clique][2]))]
            possible_combinations = list(set(possible_combinations))
            possible_combinations = self.get_proper_combinations(possible_combinations, cur_clique)
            #print("clique: ", self.clique[cur_clique], " and proper combinations: ", possible_combinations)
            #print("")
            cur_list = []
            self.domain[cur_clique] = []
            self.domain[cur_clique].extend(possible_combinations)
        #print("")


        # creating dictionary items inside same clique
        for iter in range(counter):
            for i in self.clique[iter][2][0:]:
                for j in self.clique[iter][2][0:]:
                    if i != j:
                        try:
                            self.inside_same_clique[i].append(j)
                        except KeyError:
                            self.inside_same_clique[i] = [j]

        #print(self.variables)
        #print()
        #print(self.size_of_puzzle)
        #print()
        #print(self.domain)
        #print()
        #print(self.clique)
        #print()
        #print(self.inside_same_clique)
        #print()
        #print(self.neighbors_col_row)
        #print()
        #print(self.clique_number)

        CSP.__init__(self, self.variables, self.domain, self.neighbors_col_row, self.get_kenken_constraints_satisfaction)

    def get_proper_combinations(self, possible_combinations, cur_clique):

        proper_combinations = []

        math_number = self.clique[cur_clique][0]
        math_symbol = self.clique[cur_clique][1]
        clique_size = len(self.clique[cur_clique][2])

        temp_var = 0

        if math_symbol == "+":
            for combination in possible_combinations:
                for i in range(clique_size):
                    temp_var += combination[i]
                if temp_var == math_number:
                    proper_combinations.append(combination)
                temp_var = 0
        elif math_symbol == "-":
            for combination in possible_combinations:
                temp_var = combination[0]
                for i in range(1, clique_size):
                    temp_var -= combination[i]
                if abs(temp_var) == math_number:
                    proper_combinations.append(combination)
        elif math_symbol == "*":
            for combination in possible_combinations:
                temp_var = 1
                for i in range(clique_size):
                    temp_var *= combination[i]
                if temp_var == math_number:
                    proper_combinations.append(combination)
        elif math_symbol == "/":
            for combination in possible_combinations:
                temp_var = combination[0]
                for i in range(1, clique_size):
                    temp_var /= combination[i]
                if (temp_var == math_number) or (temp_var == (1/math_number)):
                    proper_combinations.append(combination)

        return proper_combinations

    def get_neighbors_constraints(self, row, col):

        main_tuple = (row, col)
        neighbors_list = []

        # get items of same row
        for j in range(self.size_of_puzzle):
            current_tuple = (row, j)
            if main_tuple != current_tuple:
                neighbors_list.append(current_tuple)

        # get items of sam col
        for i in range(self.size_of_puzzle):
            current_tuple = (i, col)
            if main_tuple != current_tuple:
                neighbors_list.append(current_tuple)

        return neighbors_list

    def get_kenken_constraints_satisfaction(self, var_A, val_a, var_B, val_b):

        #check similarity
        if isinstance(var_A, tuple) and isinstance(var_B, tuple):
            #if self.check_similar_neighbors(var_A, val_a, var_B, val_b) == 0:
                #return False
            #return True
            return val_a != val_b

        cur_clique = []
        cur_clique_valies = []

        # A is a clique
        if isinstance(var_A, int) and isinstance(var_B, tuple):

            #print(var_A, val_a, var_B, val_b)
            cur_clique = self.clique[var_A][2]
            index_var_b = cur_clique.index(var_B)
            #print("index: ", index_var_b)
            #print("cur_clique: ", cur_clique)
            cur_clique_valies = [self.infer_assignment().get(cur_clique[i]) for i in range(len(cur_clique))]
            #print("cur_clique_values: ", cur_clique_valies)
            if val_b != val_a[index_var_b]:
                return False
            for i in range(len(cur_clique)):
                #print("intoooo hereeee")
                if i == index_var_b:
                    continue
                if cur_clique_valies[i] is None:
                    continue
                if cur_clique_valies[i] != val_a[i]:
                    #print("val_a[i]", val_a[i])
                    return False
            #print("aaaaaaaaaaaaaaaaaaa")
            return True
        # B is a clique
        elif isinstance(var_A, tuple) and isinstance(var_B, int):

            #print(var_A, val_a, var_B, val_b)
            cur_clique = self.clique[var_B][2]
            index_var_a = cur_clique.index(var_A)
            #print("index: ", index_var_a)
            #print("cur_clique: ", cur_clique)
            cur_clique_valies = [self.infer_assignment().get(cur_clique[i]) for i in range(len(cur_clique))]
            #print("cur_clique_values: ", cur_clique_valies)
            if val_a != val_b[index_var_a]:
                return False
            for i in range(len(cur_clique)):
                #print("intoooo thereeeeee")
                if i == index_var_a:
                    continue
                if cur_clique_valies[i] is None:
                    continue
                if cur_clique_valies[i] != val_b[i]:
                    return False
            #print("aaaaaaaaaaaaaaaaaaa")
            return True
        else:
            print("---> Wrong arguments at get_kenken_constraints_satisfaction() <---")
            sys.exit()

        return False


    def check_similar_neighbors(self, var_A, val_a, var_B, val_b):

        # check similarity
        if var_B in self.neighbors_col_row[var_A]:
            if val_a == val_b:
                return 0
        return 1

    """
    def do_math_function(self, var_A, val_a, var_B, val_b):

        clique_A_number = self.clique_number[var_A]
        symbol = self.clique[clique_A_number][1]

        result = False

        if symbol == "+":
            print("")
        # clique with only 2 variables
        elif symbol == "-":
            if a > b:
                if (a-b) == self.clique[clique_A_number][0]:
                    result = True
            else:
                if (b-a) == self.clique[clique_A_number][0]:
                    result = True
        elif symbol == "*":
            print("")
        #clique with only 2 variables
        elif symbol == "/":
            if a > b:
                if (a/b) == self.clique[clique_A_number][0]:
                    result = True
            else:
                if (b/a) == self.clique[clique_A_number][0]:
                    result = True

        return result
    """

    def display_result(self, result):

        started_result = {}
        try:
            for i in result:
                if isinstance(i, tuple):
                    #print(result[i])
                    started_result[i] = result[i]
        except TypeError:
            print(result)
            return

        #print("started_result: ", started_result)
        started_result = sorted(started_result.keys())
        #print("started_result: ", started_result)

        counter = 1
        for i in started_result:
            print(result[i], end=' ')
            if counter == self.size_of_puzzle:
                print()
                counter = 0
            counter += 1





if __name__ == '__main__':

    #if len(sys.argv) != 3:
    #    print("Not enough arguments. Run command should be:")
    #    print("--- python kenken_csp.py <algorithm> <input_data_file> ---")
    #    sys.exit()

    algorithm_array = ["BT", "BT+MRV", "FC", "FC+MRV", "MAC"]
    input_data_array = ["./datasets/kenken3.txt", "./datasets/kenken4.txt", "./datasets/kenken5.txt"]
    time_results = [[],[],[],[],[]]
    assignments_number = [[],[],[],[],[]]

    #algorithm = sys.argv[1]
    #input_data_file = sys.argv[2]
    starting_time = time.clock()
    initialize_time = 0
    algorithm_time = 0

    #exists = os.path.isfile(input_data_file)
    #if not exists:
    #    print("File \"\"\"", input_data_file, "\"\"\" doesn't exist. Please try another file.")
    #    sys.exit()

    for algorithm in algorithm_array:
        time_results.append([])
        assignments_number.append([])
        for input_data_file in input_data_array:

            initialize_time = 0
            algorithm_time = 0
            assignments_No = 0

            my_kenken = myKenken(input_data_file)

            if algorithm == "BT":
                starting_algorithm_time = time.clock()
                backtracking_result = backtracking_search(my_kenken)
                algorithm_time = time.clock()
                finish_algorithm_time = algorithm_time - starting_algorithm_time
                #print(backtracking_result)
                my_kenken.display_result(backtracking_result)
                time_results[0].append(finish_algorithm_time)
                assignments_number[0].append(my_kenken.nassigns)

            elif algorithm == "BT+MRV":
                starting_algorithm_time = time.clock()
                backtracking_result = backtracking_search(my_kenken, select_unassigned_variable=mrv)
                algorithm_time = time.clock()
                finish_algorithm_time = algorithm_time - starting_algorithm_time
                my_kenken.display_result(backtracking_result)
                time_results[1].append(finish_algorithm_time)
                assignments_number[1].append(my_kenken.nassigns)

            elif algorithm == "FC":
                starting_algorithm_time = time.clock()
                backtracking_result = backtracking_search(my_kenken, inference=forward_checking)
                algorithm_time = time.clock()
                finish_algorithm_time = algorithm_time - starting_algorithm_time
                my_kenken.display_result(backtracking_result)
                time_results[2].append(finish_algorithm_time)
                assignments_number[2].append(my_kenken.nassigns)

            elif algorithm == "FC+MRV":
                starting_algorithm_time = time.clock()
                backtracking_result = backtracking_search(my_kenken, select_unassigned_variable=mrv,inference=forward_checking)
                algorithm_time = time.clock()
                finish_algorithm_time = algorithm_time - starting_algorithm_time
                my_kenken.display_result(backtracking_result)
                time_results[3].append(finish_algorithm_time)
                assignments_number[3].append(my_kenken.nassigns)

            elif algorithm == "MAC":
                starting_algorithm_time = time.clock()
                backtracking_result = backtracking_search(my_kenken, inference=mac)
                algorithm_time = time.clock()
                finish_algorithm_time = algorithm_time - starting_algorithm_time
                my_kenken.display_result(backtracking_result)
                time_results[4].append(finish_algorithm_time)
                assignments_number[4].append(my_kenken.nassigns)

            elif algorithm == "MINCONF":
                starting_algorithm_time = time.clock()
                backtracking_result = min_conflicts(my_kenken)
                algorithm_time = time.clock()
                finish_algorithm_time = algorithm_time - starting_algorithm_time
                my_kenken.display_result(backtracking_result)
                if backtracking_result is None:
                    assignments_number[5].append("None")
                else:
                    assignments_number[5].append(my_kenken.nassigns)
                time_results[5].append(finish_algorithm_time)


            else:
                print("Wrong algorithm input from command line. Available algorithms are: ")
                print("       i. BT")
                print("      ii. BT+MRV")
                print("     iii. FC")
                print("      iv. FC+MRV")
                print("       v. MAC")
                print("      vi. MINCONF")
                sys.exit()

            print("Algorithm {}: ".format(algorithm))
            print("  Calculation time:   --- {0:.5f} seconds ---" .format(finish_algorithm_time))
            print("  Input Data File:    --- {} file ---".format(input_data_file))
            print("")

    print("Final time results: ")
    for i in range(5):
        for j in range(3):
            print("{0:.5f}".format(time_results[i][j]), end=' ')
        print()

    print("Final Assignments results: ")
    for i in range(5):
        for j in range(3):
            print(format(assignments_number[i][j]), end=' ')
        print()


