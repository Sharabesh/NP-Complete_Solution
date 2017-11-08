import itertools 




def wizards(numWiz, numCon, array_Wiz, arrayCon):
	allCombos = itertools.permutations(array_Wiz,len(array_Wiz))
	for item in allCombos:
		if fulfils_all_constraints(item):
			print(item)
	return "DONE"


def fulfils_all_constraints(constraints,ordering):
	return all([fulfils(constraint,ordering) for constraint in constraints])


def fulfils(constraint,ordering):
	dependency = ordering.index(constraint[-1])
	first_val = ordering.index(constraint[0])
	second_val = ordering.index(constraint[1])
	return dependency < first_val or dependency > second_val