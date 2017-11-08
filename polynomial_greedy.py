# Heuristic --> Rule out exponential algorithms with a decent amount of constraints 


def mapper(constraints, alphabet):

	# Initialization the main mapping
	mapping = {}
	

	hq = 0 
	
	for i in range(-len(alphabet),len(alphabet)):
		mapping[i] = set()

	# Initialize everything together 
	mapping[hq].add([x for x in alphabet])

	# Now do the actual decomp 
	for constraint in constraints:

		ages = finder(mapping,constraint)
		new_val = ages[2]
		ages.pop(2)
		ages = sorted(ages) 

		# Eg positions is now [1,2,2] 
			# This means wiz1 = 1, wiz2 = 2, wiz3 = 2 which is bad
			# This means I have to shift the end value

		if ages[0]<= new_val <= ages[1]:
			mapping[new_val].remove(constraint[-1]) # Remove the depdenency 
			

			# Now put the value in the next available spot 
			mapping[ages[1]].add(constraint[-1])


	# Now we have finished exhausting all the constraints 
	output = [] 
	count = 1
	for key,val in mapping.items():
		for element in val:
			output.append(element,count)
			count += 1
	return output 
		







def finder(mapping,key): # key = "abc" 
	first_letter = key[0]
	second_letter = key[1]
	third_letter = key[2]
	result = [-1,-1,-1]
	for key,val in mapping.items():
		if first_letter in val:
			result[0] = key
		if second_letter in val:
			result[1] = key
		if third_letter in val:
			result[2] = key
	return result 





