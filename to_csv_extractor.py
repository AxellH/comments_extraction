# Imports
import json
import re
import csv
import time
import demjson

# Function used to manage and to replace special caracters + handle upper case transformation
def replace_it(counter, idx):
	Matrix[counter][idx] = Matrix[counter][idx].replace('\n', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('\\n', ' ')
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
	Matrix[counter][idx] = Matrix[counter][idx].replace('Ã‰', 'é')
	Matrix[counter][idx] = Matrix[counter][idx].replace('=', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('+', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('  ', ' ')
	Matrix[counter][idx] = Matrix[counter][idx].replace('   ', ' ')
	return Matrix[counter][idx].upper()

# Final data array parameters (size)
MAX_CONCAT = 100000
NUM_ATTRIBUTES = 7

# I/O data files
json_data = 'test_4700_lcp.json'
csv_data = './test_4700_lcp_json.csv'

# Time the begining of the program execution
start = time.time()

# Handle the json file structure (to be processable)
with open(json_data) as json_file:
	lines = ''
	for line in json_file:
		line = line.replace('ObjectId(', '')
		line = line.replace(')', '')
		if '/*' not in line:
			lines = lines + line

# Separate each json model
div_json = re.split('\n\n', lines)

# Data arrays declaration
data = []
mdl_id = []
mdl_com = []
var_name = []
var_com = []
piece_name = []
piece_com = []

# Fill the data arrays
for i in range(len(div_json)):
	data.append(json.loads(div_json[i]))
	varName = data[i]['versions'][0]['fileMetadata']['variantNames']
	varCom = data[i]['versions'][0]['fileMetadata']['variantComments']
	pieceName = data[i]['versions'][0]['fileMetadata']['pieceNames']
	pieceCom = data[i]['versions'][0]['fileMetadata']['pieceComments']
	if len(varName) != 0 and len(varCom) != 0 and len(pieceName) != 0 and len(pieceCom) != 0: # Check if no field is empty
		mdl_id.append(data[i]['_id'])
		mdl_com.append(data[i]['versions'][0]['fileMetadata']['modelComment'])
		varName = data[i]['versions'][0]['fileMetadata']['variantNames']
		var_name.append(varName[0])
		varCom = data[i]['versions'][0]['fileMetadata']['variantComments']
		var_com.append(varCom[0])
		piece_name.append(pieceName)
		piece_com.append(pieceCom)

# Creation of our CSV 2D array
Matrix = [['' for x in range(NUM_ATTRIBUTES)] for y in range(MAX_CONCAT)]
matrix_cpt = 0 # Used to travel across the Matrix lines

# Fill the final 2D array
for i in range(len(mdl_id)):
	for j in range(len(piece_name[i])):
		Matrix[matrix_cpt][0] = mdl_id[i]
		Matrix[matrix_cpt][1] = mdl_com[i]
		Matrix[matrix_cpt][1] = replace_it(matrix_cpt, 1)
		Matrix[matrix_cpt][2] = var_name[i]
		Matrix[matrix_cpt][2] = replace_it(matrix_cpt, 2)
		Matrix[matrix_cpt][3] = var_com[i]
		Matrix[matrix_cpt][3] = replace_it(matrix_cpt, 3)
		Matrix[matrix_cpt][4] = piece_name[i][j]
		Matrix[matrix_cpt][4] = replace_it(matrix_cpt, 4)
		Matrix[matrix_cpt][5] = piece_com[i][j]
		Matrix[matrix_cpt][5] = replace_it(matrix_cpt, 5)
		Matrix[matrix_cpt][6] = str(Matrix[matrix_cpt][1]) + ' ' + str(Matrix[matrix_cpt][3]) + ' ' + str(Matrix[matrix_cpt][5])
		Matrix[matrix_cpt][6] = replace_it(matrix_cpt, 6)
		Matrix[matrix_cpt][6] = Matrix[matrix_cpt][6].replace('  ', ' ')
		Matrix[matrix_cpt][6] = Matrix[matrix_cpt][6].replace('  ', ' ')
		matrix_cpt = matrix_cpt + 1

# CSV columns name
fields = ['Model ID', 'Model Comment', 'Variant Name', 'Variant Comment', 'Piece Name', 'Piece Comment', 'Concatenation']

# Write the final 2D array obtained into a CSV file
with open(csv_data, 'w', newline='') as csv_file:
	writer = csv.writer(csv_file, delimiter = ';')
	writer.writerows([fields])
	for i in range(len(Matrix)):
		count = 0
		if '' in Matrix[i] or ' ' in Matrix[i] or '  ' in Matrix[i]:
			count = count + 1
		if count == 0: # We only write the line if it hasn't got any empty field
			writer.writerows([Matrix[i]])
	csv_file.close() # Properly close the final csv file

print('Execution time = %f sec.' % (time.time() - start))
