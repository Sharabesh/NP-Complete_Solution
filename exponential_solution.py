import itertools 




def wizards(numWiz, numCon, array_Wiz, arrayCon):
	allCombos = itertools.permutations(array_Wiz,len(array_Wiz))
	for item in allCombos:
		print("Item is: ","".join(item))
		if fulfils_all_constraints("".join(item),arrayCon):
			print("VALID: ",item)
	return "DONE"


def fulfils_all_constraints(ordering,constraints):
	return all([fulfils(constraint,ordering) for constraint in constraints])


def fulfils(constraint,ordering):
	print("Constraint is: ",constraint)
	print("Ordering is: ",ordering)
	dependency = ordering.index(constraint[-1])
	first_val = ordering.index(constraint[0])
	second_val = ordering.index(constraint[1])
	return dependency < first_val or dependency > second_val