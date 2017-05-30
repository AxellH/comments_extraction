import json
import re
import csv

ids = [] # If a line contains 'id' it is put into this array
ids_mdl = [] # Final array for mdl ID
ids_version = [] # Final array for version ID
mdl = [] # If a line contains 'modelComment' it is put into this array
mdl_comment = [] # Final array for model comment

lines = '' # File lines concatenation

NUM_ATTRIBUTES = 7 # [mdl ID, mdl comment, var name, var comment, piece name, piece comment, mdl com + var com + piece com]
MAX_CONCAT = 100000 # Number of lines such as the one just on top of it

# Function used to manage and to replace special caracters + handle upper case transformation
def replace_it(matrix, counter, idx):
	Matrix[counter][idx] = Matrix[counter][idx].replace('\\n', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('\\\\n', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('-', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('_', '')
	Matrix[counter][idx] = Matrix[counter][idx].replace('<', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('>', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('(', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace(')', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('.', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace(':', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace(';', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace(',', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('\'', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('"', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('/', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('\\', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('Ã©', 'é')
	Matrix[counter][idx] = Matrix[counter][idx].replace('=', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('+', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('  ', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('   ', ' ')
	return Matrix[counter][idx].upper()

# Id and model comments extraction
data_file = open('test_1000_lcp.json') # Open the json file
for line in data_file: # Travel across it
	lines = lines + line # Lines concatenations
	if '_id' in line: # Identification of the 'id' piece of information
		ids.append(line)
	elif 'modelComment' in line: # Identification of the 'model commentary' piece of information
		mdl.append(line)

# Mdl comments extraction - proper
for i in range(len(mdl)): # Travel across the mdl commentaries extracted
	mdl_split = re.split('"', mdl[i]) # Extract each part between quotes of the modelComment line
	mdl_comment.append(mdl_split[3]) # The fourth part is the modelComment needed
	mdl_comment[i] = mdl_comment[i].replace('\\n', ' ') # Make it proper

# Models ID extraction
id_nb = 0 # Used to detect the number of id in a model Json
lines_split = re.split('\n\n', lines) # Divide document by models
array_cmt = [] # Array used to ignore model multiple versions (just keep the first one)
for i in range(len(lines_split)): # Travel across the differents models
	lines_split_bis = re.split('"', lines_split[i])
	id_cmp = id_nb
	for j in range(len(lines_split_bis)):
		if '_id' in lines_split_bis[j]:
			if id_nb == id_cmp: # It corresponds to the first commentary met (the model one)
				ids_mdl.append(lines_split_bis[3]) # So the model ID is computed only if it corresponds to the first "_id" met into the model scope
			else:
				array_cmt.append(i) # Else the commentary corresponds to the version one, it is necessary to keep only the first
			id_nb = id_nb + 1

# Duplicated commentaries due to several versions have to be deleted
multiple_versions_mdl_idx = [] # Array used to get the index of models including several versions
for i in range(len(array_cmt)):
	for j in range(len(array_cmt)):
		if i != j:
			if array_cmt[i] == array_cmt[j]: # If there is a duplicate of a comment, that's meaning there are several model versions
				multiple_versions_mdl_idx.append(i) # So it is exclude

for i in range(len(multiple_versions_mdl_idx)): # Travel across the commentaries to exclude
	if i%2 == 1:
		mdl_comment.remove(mdl_comment[multiple_versions_mdl_idx[i]]) # We only keep the first version commentary

# Tmp arrays declaration (used to fill the final 2D array)
a1 = []
a2 = []
a4 = []
a5 = []

# Every fields we need are getting back
for i in range(len(lines_split)):
	a = re.split(']', lines_split[i])
	if a != ['']:
		a1.append(a[1])
		a2.append(a[2])
		a4.append(a[4])
		a5.append(a[5])

cpt = 0 # Used to travel accross the result matrix
Matrix = [['' for x in range(NUM_ATTRIBUTES)] for y in range(MAX_CONCAT)] # Creation of our CSV 2D array

# Fill the final 2D array with extracted information
for z in range(len(ids_mdl)):
	a1_bis = re.split('"', a1[z])
	a2_bis = re.split('"', a2[z])
	a4_bis = re.split('"', a4[z])
	a5_bis = re.split('"', a5[z])
	for i in range(2, len(a2_bis)):
		if i%2 == 1:
			if len(a5_bis) > 3: # Check if the variantName isn't empty
				# Feed the final 2D array
				Matrix[cpt][0] = ids_mdl[z]
				Matrix[cpt][1] = mdl_comment[z]
				Matrix[cpt][1] = replace_it(Matrix, cpt, 1)
				Matrix[cpt][2] = a5_bis[3]
				Matrix[cpt][3] = a4_bis[3]
				Matrix[cpt][3] = replace_it(Matrix, cpt, 3)
				Matrix[cpt][4] = a2_bis[i]
				Matrix[cpt][4] = replace_it(Matrix, cpt, 4)
				Matrix[cpt][5] = a1_bis[i]
				Matrix[cpt][5] = replace_it(Matrix, cpt, 5)
				Matrix[cpt][6] = Matrix[cpt][1] + ' ' + Matrix[cpt][3] + ' ' + Matrix[cpt][5]
				Matrix[cpt][6] = Matrix[cpt][6].replace('  ', ' ')
				Matrix[cpt][6] = Matrix[cpt][6].replace('  ', ' ')
				cpt = cpt + 1

# CSV columns name
fields = ['Model ID', 'Model Comment', 'Variant Name', 'Variant Comment', 'Piece Name', 'Piece Comment', 'Concatenation']
count = 0

# Write the final 2D array obtained into a CSV file
with open('./test_1000_lcp.csv', 'w', newline='') as csv_file:
	writer = csv.writer(csv_file, delimiter = ';')
	writer.writerows([fields])
	for i in range(len(Matrix)):
		count_cmp = count
		for j in range(len(Matrix[i])):
			if Matrix[i][j] == '':
				count = count + 1
			elif Matrix[i][j] == ' ':
				count = count + 1
			elif Matrix[i][j] == '  ':
				count = count + 1
		if (count == count_cmp): # We only write the line if it hasn't got any empty field
			writer.writerows([Matrix[i]])
	csv_file.close() # Properly close the final csv file
