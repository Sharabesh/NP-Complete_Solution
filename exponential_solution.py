import itertools 
import random
import numpy as np 
from math import e


def parser(filename):
	with open(filename,"r") as file:
		k = file.readlines()
	wizards = k[1].replace(" ","").replace("\n","")
	constraint_list = [] 
	for element in k[3:]:
		constraint_list.append(element.replace(" ","").replace("\n",""))
	return (list(wizards),constraint_list)



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














