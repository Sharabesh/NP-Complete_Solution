import os
import string
from itertools import permutations


def abeAlphabet(numSize, totalAlphabetLength):
    alphabet = string.ascii_lowercase
    permuteThis = ""
    for i in range(numSize):
        permuteThis = permuteThis + alphabet[i]
    perms = [''.join(p) for p in permutations(permuteThis)]
    return perms[:totalAlphabetLength]

def validate(inputs, outputs):
    # reads the input file of contraints
    with open(inputs, "r") as file:
        k = file.readlines()
        numWiz = int(k[0].split(" ")[0])
        numConstraints = int(k[1].split(" ")[0])

    # reads the output that we get from running out algorithm
    with open(outputs, "r") as file:
        wiz = file.readlines()

    # reads through all our orderings of wizards
    wiz = wiz[0].split(" ")

    # checks to see if it satisfies all contraints
    for j in range(2, numConstraints + 2):
        count = 0
        inMiddle = False

        # the current constraint that we are trying to satisfy
        currConstraint = k[j].split(" ")[:3]

        #parses for the each wizard in the ordering
        first = currConstraint[0]
        second = currConstraint[1]
        third = currConstraint[2]

        # makes sure each wizard in our ordering satisfyings the constraint
        print(wiz)
        print(first, second, third)

        for name in wiz:
            if name == first or name == second:
                count += 1
            if name == third and (count == 0 or count == 2):
                inMiddle = True
                count += 1
        print("count", count)
        if count != 3:
            print("didn't find all three wizards")
            print(first, second, third)
            return
        elif not inMiddle:
            print("ordering is wrong here")
            print(first, second, third)
            return False

    print("all good -Abe")
    return True


def validate_all(input_dir):
    input_files = [x for x in os.listdir(input_dir) if "output" not in x]
    vals = []
    for elem in input_files:
        last_dig = elem[-4]
        file_num = elem[5:7]
        corresponding = "output{0}_{1}.out".format(file_num, last_dig)
        if not validate(input_dir + elem, "outputs/" + corresponding):
            print(elem + "NOT VALID")
            vals.append(False)
        else:
            vals.append(True)
    return all(vals)
