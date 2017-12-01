import itertools
import random
from math import e
import string
import os
import time
""" Non standard libraries used for multithreading and faster data manipulation"""
import concurrent.futures
import numpy as np



"""
Supervisor multithreaded is designed to run in one of the input directories
 * Staff_inputs 
 * inputs20
 * inputs35
 * inputs50 
 It generates a list of files to process and and then submits them to a ProcessPoolExecutor
 allowing all of these files to generate solutions simultaneously. It also handles file writing 
such that on conclusion of the inputs it identifies the output directories: ../../outputs/<Corrrect filename> 
and writes into that file. 
"""
def supervisor_multithreaded():
	
	executor = concurrent.futures.ProcessPoolExecutor(20)
	files = sorted([x for x in os.listdir(".") if "output" not in x])
	for input_file in files:
		executor.submit(inner_helper, (input_file))


""" A helper method for multithreading """
def inner_helper(input_file):
	wiz, constraints = new_parser(input_file)
	if "staff" in input_file:
		num = input_file.split("_")[1].split(".")[0]
		output_file = "../../outputs/staff_{0}.out".format(num)
	elif "submission" in input_file:
		val = input_file.replace(".in",".out")
		output_file = "../../phase3_outputs/{0}".format(val)
	else:
		output_file = "../../outputs/output{0}_{1}.out".format(input_file[5:7], input_file[-4])
	return_val = markov_solver(constraints, wiz,output_file=output_file)
	with open(output_file, "w+") as file:
		file.write(return_val.strip())
	os.system("say {0}".format(input_file))
	return return_val

"""
New Parser is designed to read a filename and generate a set of constraints and wizards
It also passes any existing solutions in the output file that may have been previously generated into our algorithm 
so that we can start at a pre-existing solution and gradually improve. 
"""
def new_parser(filename,use_original=True):
	# Convert wizards into single char representations

	with open(filename, "r") as file:
		k = file.readlines()

	num_wizards = k[0].replace("\n", "")
	num_constraints = k[1].replace("\n", "")

	constraints_list = []  # A list of tuples of constraints
	# Gather all the data
	wiz_set = set()
	for element in k[2:]:
		target = element.replace("\n", "").strip().split()
		constraints_list.append(tuple(target))
		for item in element.replace("\n", "").split():
			wiz_set.add(item)

	# Convert all the data to single character representations
	output_file = ""
	if "staff" in filename:
		num = filename.split("_")[1].split(".")[0]
		output_file = "../../outputs/staff_{0}.out".format(num)
	elif "submission" in filename:
		output_file = "../../phase3_outputs/{0}".format(filename.replace(".in",".out"))
	else:
		output_file = "../../outputs/output{0}_{1}.out".format(filename[5:7], filename[-4])
	return_val = list(wiz_set)
	if os.path.exists(output_file):
		with open(output_file,"r") as file:
			k = file.read()
		k = k.replace("\n","")
		z = k.split()
		if use_original:
			if set(z) == wiz_set:
				return_val = list(z)

	return (return_val, constraints_list)

""" Fulfils determines if an ordering satisfies a given constraint
This method is used to calculate the number of wizards that are still failing
""" 
def fulfils(constraint, ordering):  # Constraint needs to be a list
	# print("Constraint is: ",constraint)
	# print("Ordering is: ",ordering)
	# print(constraint)

	wiz_mid = ordering.index(constraint[-1])
	wiz_a = ordering.index(constraint[0])
	wiz_b = ordering.index(constraint[1])

	if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
		return False
	else:
		return True


	# return (not (first_val < dependency <= second_val)) and (not (second_val <= dependency <= first_val))

"""
Markov solver is the true solver of the algorithm. It takes
	- Constraints: A list containing tuples of constraints (Eg: [(a, b, c), (d, e, f)])
	- Wizards: The starting position for our algorithm 
	- output_file: A file to write temporary results so we can store intermediate values

This algorithm begins with an ordering of wizards (param: wizards) and then incrementally makes
changes to the ordering. It will always take a better ordering but it may choose a worse ordering defined by the formula
```probability_transfer = e ** (beta * (constraints_violated_current - constraints_violated_new))```
It terminates once it identifies the case of 0 conditions violated. 
"""
def markov_solver(constraints, wizards, output_file=None):
	num_constraints = len(list(set(constraints)))
	constraints = list(set(constraints))
	# Swap state
	curr_min = 100

	constraints_violated_current = num_constraints - np.count_nonzero([fulfils(x, wizards) for x in constraints])

	# Make a copy of the values so you can return to previous state
	new_state = list(wizards)

	beta = 1.5  # Update beta's

	while constraints_violated_current > 0:
		if (time.time() // 1) % 10 == 0:
			print("Staff_{0} Constraints violated {1}".format(output_file,constraints_violated_current)," ".join(wizards))

		# New additions to drop faster
		num_swaps = 1
		if constraints_violated_current <= 10:
			num_swaps = 1
		elif constraints_violated_current <= 20:
			num_swaps = 20
		elif constraints_violated_current <= 30:
			num_swaps = 50

		new_state = list(wizards)  # Potentially redundant but eh?

		for i in range(1):  # Big jumps at the beginning
			start_swap = random.randint(0, len(new_state) - 1)
			end_swap = random.randint(0, len(new_state) - 1)
			new_state[start_swap], new_state[end_swap] = new_state[end_swap], new_state[start_swap]

		constraints_violated_new = num_constraints - np.count_nonzero(
			[fulfils(x, new_state) for x in constraints])
		# New additions

		if constraints_violated_new < 10:
			beta = 5
		elif constraints_violated_new <= 20:
			beta = 6

		elif constraints_violated_new <= 30:
			beta = 2.0

		# End new additions

		try:
			probability_transfer = e ** (beta * (constraints_violated_current - constraints_violated_new))
		except ZeroDivisionError:
			return " ".join(new_state)
		selection = random.random()
		print(constraints_violated_current)  # Weight the constraints somehow
		if selection < probability_transfer:
			wizards = list(new_state)
			constraints_violated_current = constraints_violated_new

	return " ".join(new_state)



"""
The following is code that is not necessary to the function of the algorithm. 
It was used for testing purposes and has been commented as such

"""


"""
Explains whether or not a parameter num constraints are violated by the current ordering

"""
def fulfils_k_constraints(ordering, constraints, num):
	total_mapping = string.ascii_lowercase + string.ascii_uppercase
	i = 0
	wiz_set = ordering.split()
	# Generate single character representations

	fulfillment = np.count_nonzero([fulfils(constraint, ordering) for constraint in constraints])
	return (len(constraints) - fulfillment) <= num


""" 
Main job is to match the outputs up with whatever was generated by the program
"""
def find_matching(output_file, num):
	with open(output_file, "r") as file:
		k = file.readlines()
	k = [x.replace("\n", "") for x in k if x != "\n"]

	mapping = {}

	for item in [x for x in os.listdir(".") if x != output_file]:
		wiz, constraints = new_parser(item)
		mapping[item] = []
		for i in range(len(k)):
			print("K IS: ", k[i])
			print("constraints is: ", constraints)
			try:
				if fulfils_k_constraints(k[i], constraints, num):
					mapping[item].append(i)
			except:
				pass
	return mapping


""""Unnecessary stuff """

""" 
This program was used to determine the continuity of constraint swapping method. 

We sought to determine if there was a gradual improvement brought about
 by making a swap rather than random spikes. 

"""
def markov_walk(constraints, wizards):
	num_constraints = len(list(set(constraints)))
	constraints = list(set(constraints))
	# Swap state

	constraints_violated_current = num_constraints - np.count_nonzero([fulfils(x, wizards) for x in constraints])

	new_state = list(wizards)
	for k in range(100):

		new_state = list(wizards)

		for i in range(1):
			start_swap = random.randint(0, len(wizards) - 1)
			end_swap = random.randint(0, len(wizards) - 1)
			new_state[start_swap], new_state[end_swap] = new_state[end_swap], new_state[start_swap]

		print(wizards, "".join(new_state))
		constraints_violated_new = num_constraints - np.count_nonzero(
			[fulfils(x, "".join(new_state)) for x in constraints])
		try:
			probability_transfer = constraints_violated_current / constraints_violated_new
		except ZeroDivisionError:
			return "".join(new_state)
		selection = random.random()
		print(constraints_violated_current)
		if True:
			wizards = "".join(new_state)
			constraints_violated_current = constraints_violated_new

	return "".join(new_state)


"""
The following is our exponential solver used for testing purposes.
This function iterates through all possible orderings of wizards 
and identify which orderings are valid in all constraints. 
"""


def wizards(array_Wiz, arrayCon):
	valid = []
	# array_Wiz = array_Wiz[::-1]
	count = 0
	allCombos = itertools.permutations(array_Wiz, len(array_Wiz))
	for item in allCombos:
		print("Item is: ", "".join(item))
		if fulfils_all_constraints("".join(item), arrayCon):
			joinedItem = "".join(item)
			print("VALID: ", joinedItem)
			count += 1
			valid.append(joinedItem)
	print(count)
	print(valid)
	print("constraints", arrayCon, len(arrayCon))
	return "DONE"


def fulfils_all_constraints(ordering, constraints):
	return all([fulfils(constraint, ordering) for constraint in constraints])
