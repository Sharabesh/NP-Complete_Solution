import itertools 
import random
import numpy as np 
from math import e
import string
import os

def parser(filename):
	with open(filename,"r") as file:
		k = file.readlines()
	wizards = k[1].replace(" ","").replace("\n","")
	constraint_list = [] 
	for element in k[3:]:
		constraint_list.append(element.replace(" ","").replace("\n",""))
	return (list(wizards),constraint_list)

def new_parser(filename):
	# Convert wizards into single char representations
	total_mapping = string.ascii_lowercase + string.ascii_uppercase
	forward_mapping = {}
	backwards_mapping = {}

	with open(filename,"r") as file:
		k = file.readlines()
	num_wizards = k[0].replace("\n","")
	num_constraints = k[1].replace("\n","")
	constraints_list = [] 
	# Gather all the data 
	wiz_set = set()
	for element in k[2:]:
		constraints_list.append(element.replace("\n","").strip())
		for item in element.replace("\n","").split():
			wiz_set.add(item)

	# Convert all the data to single character representations
	i = 0
	for element in wiz_set:
		target_char = total_mapping[i]
		forward_mapping[element] = target_char
		backwards_mapping[target_char] = element
		i+=1 

	new_wiz_set = []
	for element in wiz_set:
		new_wiz_set.append(forward_mapping[element])
	new_constraints_lst = []
	for constraint in constraints_list:
		curr_constraints = ""
		elements = constraint.split()
		for wizard in elements:
			curr_constraints += forward_mapping[wizard]
		new_constraints_lst.append(curr_constraints)


	return ("".join(new_wiz_set),new_constraints_lst,backwards_mapping)


def supervisor(output_file):
	output = []
	files = [x for x in os.listdir(".") if x!= output_file]
	for input_file in files:
		wiz,constraints,backwards_mapping = new_parser(input_file)
		return_val = markov_solver(constraints,wiz)
		actual_ordering = ""
		for element in return_val:
			actual_ordering += backwards_mapping[element] + " "
		with open(output_file,"wa") as file:
			file.write(actual_ordering.strip() + "\n\n\n")
		output.append(actual_ordering.strip() + "\n\n\n\n")
	with open(output_file,"w+") as file:
		file.writelines(output)

def wizards(array_Wiz, arrayCon):
	valid = []
	# array_Wiz = array_Wiz[::-1]
	count = 0
	allCombos = itertools.permutations(array_Wiz,len(array_Wiz))
	for item in allCombos:
		print("Item is: ","".join(item))
		if fulfils_all_constraints("".join(item),arrayCon):
			joinedItem = "".join(item)
			print("VALID: ",joinedItem)
			count += 1
			valid.append(joinedItem)
	print(count)
	print(valid)
	print("constraints",arrayCon, len(arrayCon))
	return "DONE"



def fulfils_all_constraints(ordering,constraints):

	return all([fulfils(constraint,ordering) for constraint in constraints])


def fulfils(constraint,ordering):
	# print("Constraint is: ",constraint)
	# print("Ordering is: ",ordering)
	# print(constraint)
	dependency = ordering.index(constraint[-1])
	first_val = ordering.index(constraint[0])
	second_val = ordering.index(constraint[1])
	return not (first_val<= dependency <= second_val)



def constraint_generator(seq):
	constraints = {}
	for i in range(len(seq)):
		for j in range(len(seq)):
			for k in range(len(seq)):
				if k != i and j != k and j != i:
					if (k > i and k > j) or (k < i and k < j):
						if (random.randint(0,1) == 0):
							constraints[seq[j]+ seq[i]+seq[k]] = 1
						else:
							constraints[seq[i]+ seq[j]+seq[k]] = 1
						# constraints.extend([seq[j]+ " "+seq[i]+" "+seq[k], seq[i]+ " "+seq[j]+" "+seq[k]])
					if (i > k and i > j) or (i < k and i < j):
						if (random.randint(0,1) == 1): 
							constraints[seq[j]+seq[k]+seq[i]] = 1
						else:
							constraints[seq[k]+seq[j]+seq[i]] = 1
						# constraints.extend([seq[j]+ " "+seq[k]+" "+seq[i], seq[k]+ " "+seq[j]+" "+seq[i]])
					if (j > k and j > i) or (j < k and j < i):
						if (random.randint(0,1) == 1): 
							constraints[seq[i]+ seq[k]+seq[j]] = 1
						else:
							constraints[seq[k]+ seq[i]+seq[j]] = 1


						# constraints.extend([seq[i]+ " "+seq[k]+" "+seq[j], seq[k]+ " "+seq[i]+" "+seq[j]])
	return list(constraints.keys())

def better_constraints(seq):
	print("start")
	constraintUsage = {}
	for item in seq:
		constraintUsage[item] = 0
	constraints = []

	while len(constraints) < 500:
		choices = []
		while len(choices) < 50:
			i = random.randint(0, len(seq)-1)
			j = random.randint(0, len(seq)-1)
			k = random.randint(0, len(seq)-1)

			if k != i and j != k and j != i:
				heur = heuristicSparse(len(constraints), len(seq), 
					constraintUsage[seq[j]], 
					constraintUsage[seq[i]], 
					constraintUsage[seq[k]])
				if (k > i and k > j) or (k < i and k < j):   #make a heuristic on k
					if (random.randint(0,1) == 1): 
						choices.append((heur, [seq[i],seq[j],seq[k]]))
					else:
						choices.append((heur, [seq[j],seq[i],seq[k]]))

				if (i > k and i > j) or (i < k and i < j):   #make a heuristic on i
					if (random.randint(0,1) == 1): 
						choices.append((heur, [seq[k],seq[j],seq[i]]))
					else:
						choices.append((heur, [seq[j],seq[k],seq[i]]))
				if (j > k and j > i) or (j < k and j < i):   #make a heuristic on j 
					if (random.randint(0,1) == 1): 
						choices.append((heur, [seq[k],seq[i],seq[j]]))
					else:
						choices.append((heur, [seq[i],seq[k],seq[j]]))

		best = max(choices, key=lambda x: x[0])
		constraints.append("".join(best[1]))
		constraintUsage[best[1][0]] += 1
		constraintUsage[best[1][1]] += 1
		constraintUsage[best[1][2]] += 1

	constraints = constraints[:len(constraints)-5]
	constraints = list(set(constraints))


	while len(constraints) < 500:
		choices = []
		while len(choices) < 50:
			i = random.randint(0, len(seq)-1)
			j = random.randint(0, len(seq)-1)
			k = random.randint(0, len(seq)-1)
			if k != i and j != k and j != i:
				heur = heuristicDense(len(constraints), len(seq), 
					constraintUsage[seq[j]], 
					constraintUsage[seq[i]], 
					constraintUsage[seq[k]])
				if (k > i and k > j) or (k < i and k < j):   #make a heuristic on k
					if (random.randint(0,1) == 1): 
						choices.append((heur, [seq[i],seq[j],seq[k]]))
					else:
						choices.append((heur, [seq[j],seq[i],seq[k]]))

				if (i > k and i > j) or (i < k and i < j):   #make a heuristic on i
					if (random.randint(0,1) == 1): 
						choices.append((heur, [seq[k],seq[j],seq[i]]))
					else:
						choices.append((heur, [seq[j],seq[k],seq[i]]))
				if (j > k and j > i) or (j < k and j < i):   #make a heuristic on j 
					if (random.randint(0,1) == 1): 
						choices.append((heur, [seq[k],seq[i],seq[j]]))
					else:
						choices.append((heur, [seq[i],seq[k],seq[j]]))

		best = max(choices, key=lambda x: x[0])
		constraints.append("".join(best[1]))
		constraintUsage[best[1][0]] += 1
		constraintUsage[best[1][1]] += 1
	print(constraintUsage)
	return constraints



def heuristicSparse(numConstraints, totalWizards, x, y, z):
	toret =  -abs((numConstraints/totalWizards)-x) 
	-abs((numConstraints/totalWizards)-y)
	-abs((numConstraints/totalWizards)-z)
	return toret

def heuristicDense(numConstraints, totalWizards, x, y, z):
	toret =  abs((numConstraints/totalWizards)-x) + abs((numConstraints/totalWizards)-y)
	return toret


def write_output(seq,filename):
	line0 = str(len(seq))
	line1 = " ".join(list(seq))
	constraints = better_constraints(seq)
	line2 = str(len(constraints))
	lines3 = [] 
	for constraint in constraints:
		lines3.append(" ".join(list(constraint)))
	with open(filename,"w+") as file:
		file.write(line0 + "\n")
		file.write(line1 + "\n")
		file.write(line2 + "\n")
		file.writelines([x + "\n" for x in lines3])
	return "DONE" 


def markov_solver(constraints,wizards):
	num_constraints = len(list(set(constraints)))
	constraints = list(set(constraints))
	# Swap state
	
	constraints_violated_current = num_constraints - np.count_nonzero([fulfils(x,wizards) for x in constraints])

	new_state = list(wizards)

	beta =  1.5 # Update beta's 

	while constraints_violated_current > 0:
		
		new_state = list(wizards)

		for i in range(1):	# Big jumps at the beginning 
			start_swap = random.randint(0,len(wizards)-1)
			end_swap = random.randint(0,len(wizards)-1)
			new_state[start_swap],new_state[end_swap] = new_state[end_swap],new_state[start_swap]

		print(wizards, "".join(new_state))
		constraints_violated_new = num_constraints - np.count_nonzero([fulfils(x,"".join(new_state)) for x in constraints])

		# New additions
		if constraints_violated_new < 10:
			beta = 5

		elif constraints_violated_new <= 20:
			beta = 2.5

		elif constraints_violated_new <= 30:
			beta = 2.0


		# End new additions

		try:
			probability_transfer = e ** (beta*(constraints_violated_current - constraints_violated_new))
		except ZeroDivisionError:
			return "".join(new_state)
		selection = random.random() 
		print(constraints_violated_current) # Weight the constraints somehow
		if selection < probability_transfer:
			wizards = "".join(new_state)
			constraints_violated_current = constraints_violated_new

	return "".join(new_state)
	
def markov_walk(constraints,wizards):
	num_constraints = len(list(set(constraints)))
	constraints = list(set(constraints))
	# Swap state
	
	constraints_violated_current = num_constraints - np.count_nonzero([fulfils(x,wizards) for x in constraints])

	new_state = list(wizards)
	for k in range(100):
		
		new_state = list(wizards)

		for i in range(1):	
			start_swap = random.randint(0,len(wizards)-1)
			end_swap = random.randint(0,len(wizards)-1)
			new_state[start_swap],new_state[end_swap] = new_state[end_swap],new_state[start_swap]

		print(wizards, "".join(new_state))
		constraints_violated_new = num_constraints - np.count_nonzero([fulfils(x,"".join(new_state)) for x in constraints])
		try:
			probability_transfer = constraints_violated_current/constraints_violated_new
		except ZeroDivisionError:
			return "".join(new_state)
		selection = random.random() 
		print(constraints_violated_current)
		if True:
			wizards = "".join(new_state)
			constraints_violated_current = constraints_violated_new

	return "".join(new_state)














