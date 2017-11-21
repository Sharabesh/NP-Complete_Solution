import itertools
import random
import numpy as np
from math import e
import string
import os
import concurrent.futures


def supervisor():  # Designed to run within an input directory

	output = []
	files = sorted([x for x in os.listdir(".") if "output" not in x])
	for input_file in files:
		wiz, constraints = new_parser(input_file)
		return_val = markov_solver(constraints, wiz)
		if "staff" in input_file:
			num = input_file.split("_")[1].split(".")[0]
			output_file = "../../staff_{0}.out".format(num)
		else:
			output_file = "../../outputs/output{0}_{1}.out".format(input_file[5:7], input_file[-4])
		with open(output_file, "a") as file:
			file.write(return_val.strip())
		output.append(return_val.strip())
		os.system("say {0}".format(input_file))
	return output


""" Speed up the process with multithreading"""


def supervisor_multithreaded():
	executor = concurrent.futures.ProcessPoolExecutor(10)
	files = sorted([x for x in os.listdir(".") if "output" not in x])
	for input_file in files:
		executor.submit(inner_helper, (input_file))


""" A helper method for multithreading """


def inner_helper(input_file):
	wiz, constraints = new_parser(input_file)
	return_val = markov_solver(constraints, wiz)
	output_file = "../../outputs/output{0}_{1}.out".format(input_file[5:7], input_file[-4])
	with open(output_file, "a") as file:
		file.write(return_val.strip())
	os.system("say {0}".format(input_file))
	return return_val


def new_parser(filename):
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


	return (list(wiz_set), constraints_list)


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


def markov_solver(constraints, wizards):
	num_constraints = len(list(set(constraints)))
	constraints = list(set(constraints))
	# Swap state

	constraints_violated_current = num_constraints - np.count_nonzero([fulfils(x, wizards) for x in constraints])

	# Make a copy of the values so you can return to previous state
	new_state = list(wizards)

	beta = 1.5  # Update beta's

	while constraints_violated_current > 0:

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
			beta = 3
		if constraints_violated_new <= 20:
			beta = 2.5

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


""" Testing Stuff"""


def fulfils_k_constraints(ordering, constraints, num):
	total_mapping = string.ascii_lowercase + string.ascii_uppercase
	i = 0
	wiz_set = ordering.split()
	# Generate single character representations

	fulfillment = np.count_nonzero([fulfils(constraint, ordering) for constraint in constraints])
	return (len(constraints) - fulfillment) <= num


""" Main job is to match the outputs up with whatever was generated by the program"""


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


"""BAD EXPONENTIAL STUFF DOWN HERE"""


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
