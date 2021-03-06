import random
from itertools import permutations



def parser(filename):
	with open(filename, "r") as file:
		k = file.readlines()
	wizards = k[1].replace(" ", "").replace("\n", "")
	constraint_list = []
	for element in k[3:]:
		constraint_list.append(element.replace(" ", "").replace("\n", ""))
	return (list(wizards), constraint_list)

def constraint_generator(seq):
	constraints = {}
	for i in range(len(seq)):
		for j in range(len(seq)):
			for k in range(len(seq)):
				if k != i and j != k and j != i:
					if (k > i and k > j) or (k < i and k < j):
						if (random.randint(0, 1) == 0):
							constraints[seq[j] + seq[i] + seq[k]] = 1
						else:
							constraints[seq[i] + seq[j] + seq[k]] = 1
						# constraints.extend([seq[j]+ " "+seq[i]+" "+seq[k], seq[i]+ " "+seq[j]+" "+seq[k]])
					if (i > k and i > j) or (i < k and i < j):
						if (random.randint(0, 1) == 1):
							constraints[seq[j] + seq[k] + seq[i]] = 1
						else:
							constraints[seq[k] + seq[j] + seq[i]] = 1
						# constraints.extend([seq[j]+ " "+seq[k]+" "+seq[i], seq[k]+ " "+seq[j]+" "+seq[i]])
					if (j > k and j > i) or (j < k and j < i):
						if (random.randint(0, 1) == 1):
							constraints[seq[i] + seq[k] + seq[j]] = 1
						else:
							constraints[seq[k] + seq[i] + seq[j]] = 1


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
			i = random.randint(0, len(seq) - 1)
			j = random.randint(0, len(seq) - 1)
			k = random.randint(0, len(seq) - 1)

			if k != i and j != k and j != i:
				heur = heuristicSparse(len(constraints), len(seq),
									   constraintUsage[seq[j]],
									   constraintUsage[seq[i]],
									   constraintUsage[seq[k]])
				if (k > i and k > j) or (k < i and k < j):  # make a heuristic on k
					if (random.randint(0, 1) == 1):
						choices.append((heur, [seq[i], seq[j], seq[k]]))
					else:
						choices.append((heur, [seq[j], seq[i], seq[k]]))

				if (i > k and i > j) or (i < k and i < j):  # make a heuristic on i
					if (random.randint(0, 1) == 1):
						choices.append((heur, [seq[k], seq[j], seq[i]]))
					else:
						choices.append((heur, [seq[j], seq[k], seq[i]]))
				if (j > k and j > i) or (j < k and j < i):  # make a heuristic on j
					if (random.randint(0, 1) == 1):
						choices.append((heur, [seq[k], seq[i], seq[j]]))
					else:
						choices.append((heur, [seq[i], seq[k], seq[j]]))

		best = max(choices, key=lambda x: x[0])
		constraints.append("".join(best[1]))
		constraintUsage[best[1][0]] += 1
		constraintUsage[best[1][1]] += 1
		constraintUsage[best[1][2]] += 1

	constraints = constraints[:len(constraints) - 5]
	constraints = list(set(constraints))

	while len(constraints) < 500:
		choices = []
		while len(choices) < 50:
			i = random.randint(0, len(seq) - 1)
			j = random.randint(0, len(seq) - 1)
			k = random.randint(0, len(seq) - 1)
			if k != i and j != k and j != i:
				heur = heuristicDense(len(constraints), len(seq),
									  constraintUsage[seq[j]],
									  constraintUsage[seq[i]],
									  constraintUsage[seq[k]])
				if (k > i and k > j) or (k < i and k < j):  # make a heuristic on k
					if (random.randint(0, 1) == 1):
						choices.append((heur, [seq[i], seq[j], seq[k]]))
					else:
						choices.append((heur, [seq[j], seq[i], seq[k]]))

				if (i > k and i > j) or (i < k and i < j):  # make a heuristic on i
					if (random.randint(0, 1) == 1):
						choices.append((heur, [seq[k], seq[j], seq[i]]))
					else:
						choices.append((heur, [seq[j], seq[k], seq[i]]))
				if (j > k and j > i) or (j < k and j < i):  # make a heuristic on j
					if (random.randint(0, 1) == 1):
						choices.append((heur, [seq[k], seq[i], seq[j]]))
					else:
						choices.append((heur, [seq[i], seq[k], seq[j]]))

		best = max(choices, key=lambda x: x[0])
		constraints.append("".join(best[1]))
		constraintUsage[best[1][0]] += 1
		constraintUsage[best[1][1]] += 1
	print(constraintUsage)
	return constraints


def heuristicSparse(numConstraints, totalWizards, x, y, z):
	toret = -abs((numConstraints / totalWizards) - x)

	return toret


def heuristicDense(numConstraints, totalWizards, x, y, z):
	toret = abs((numConstraints / totalWizards) - x) + abs((numConstraints / totalWizards) - y)
	return toret


def write_output(seq, filename):
	line0 = str(len(seq))
	line1 = " ".join(list(seq))
	constraints = better_constraints(seq)
	line2 = str(len(constraints))
	lines3 = []
	for constraint in constraints:
		lines3.append(" ".join(list(constraint)))
	with open(filename, "w+") as file:
		file.write(line0 + "\n")
		file.write(line1 + "\n")
		file.write(line2 + "\n")
		file.writelines([x + "\n" for x in lines3])
	return "DONE"
