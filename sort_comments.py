# Imports
import re
import shlex
import time
import csv

# Algorithm parameters
MIN_SIZE_WORD = 3 # Size minimal of the comments to process
TRESHOLD_FREQUENCY = 50 # Minimum appearance frequency of the comments to process

csv_data = 'test_4700_lcp_json.csv'
output_dictionnary = './dictionnary_4700_lcp.csv'

# Check if a character 's' is a number
# Return a boolean
def is_number(s):
	try:
	    float(s)
	    return True
	except ValueError:
	    return False

# Measure execution time
start = time.time()

# First part : sort the comments by only keeping the ones of size > MIN_SIZE_WORD
comment_array = [] # First array : it contains all the comments of more than MIN_SIZE_WORD characters
lines = '' # Used to concatenate csv lines
with open(csv_data, 'r') as csv:
	for line in csv:
		lines = lines + line
		line_split_1 = re.split(';', line)
		line_split_2 = shlex.split(line_split_1[-1])
		for i in range(len(line_split_2)):
			if len(line_split_2[i]) >= MIN_SIZE_WORD:
				comment_array.append(line_split_2[i])

# Second part : sort the comments by only keeping the ones which doesn't have any number string from the previously sorted array
without_num_array = [] # Second array : it contains all the comments from the comment_array which are exclusively with letters
for comment in comment_array:
	TAG = False
	for i in range(len(comment)):
		if is_number(comment[i]) == True:
			TAG = True
	if TAG == False:
		without_num_array.append(comment)

# Third part : finally exclude multiple value from the previously sorted array
final_array = [] # Third array : it contains all the comments from the without_num_array and doesn't have any redundancy
for word in without_num_array:
	if (word in final_array) == False:
		final_array.append(word)

time_bis = time.time() - start
print('Exec. time before writing = %f sec' % time_bis)

# Final step : write the comments which are left into a txt file
final_array.sort()
fields = ['Comment', 'Occurences']
with open(output_dictionnary, 'w', newline='') as file:
	for word in final_array:
		if without_num_array.count(word) >= TRESHOLD_FREQUENCY:
			file.write(word)
			file.write(';')
			file.write(str(without_num_array.count(word)))
			file.write(';\n')

# Final execution time measurement
time_bis = time.time() - start
print('Exec. time = %f sec' % time_bis)
