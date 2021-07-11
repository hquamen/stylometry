######################################################
#
# Harvey Quamen
# University of Albeta
#
# Compare punctuation in lines across two docs; although
# there's a THRESHOLD here it's not used. The two lines
# fail if there's not an exact match of punctuation tokens.
#
######################################################

import os
import re
import string

BLANK = re.compile(r'^\s*$')
COMMENT = re.compile(r'^\s*#')
PUNCTUATION = '.,;?!-—–()'

THRESHOLD = 0.9

# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/'
# document_one = 'doc_1.txt'
# document_two = 'doc_2.txt'

main_path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/'
first_dir = 'rdc/'
second_dir = 'hq/'

def calculate_ratio(one, two):
	"""Calculate the raw similarity of two sets; not Jaccard distance, as I thought."""
	a = [letter for letter in set(one) if letter in string.ascii_lowercase]
	b = [letter for letter in set(two) if letter in string.ascii_lowercase]
	return len(a) / len(b)

def retrieve_punctuation(line):
	punct = [char for char in line if char in PUNCTUATION]
	return punct

#
#	Get list of files -- one book per file
#

first_files = [f for f in os.listdir(main_path + first_dir) if f.endswith('.txt')]
first_files.sort()

second_files = [f for f in os.listdir(main_path + second_dir) if f.endswith('.txt')]
second_files.sort()

#
#	Process each PL book in parallel

num_errors = 0

for book in range(12):

	print("\n\n----------------------------- CHECKING BOOK {}".format(book + 1))
	
	with open(main_path + first_dir + first_files[book]) as f:
		doc1 = [l.strip().lower() for l in f.readlines() if not BLANK.search(l) and not COMMENT.search(l)]

	with open(main_path + second_dir + second_files[book]) as f:
		doc2 = [l.strip().lower() for l in f.readlines() if not BLANK.search(l) and not COMMENT.search(l)]

	max_lines = len(doc2)

	for line_num in range(max_lines):
		punct1 = retrieve_punctuation(doc1[line_num])
		punct2 = retrieve_punctuation(doc2[line_num])
		if punct1 != punct2:
			print('\n---- Punctuation mismatch: Line {}'.format(line_num))
			print(first_dir, ":", doc1[line_num])
			print(second_dir, ":", doc2[line_num])
			num_errors += 1



print("Total number of punctuation mismatches: {}".format(num_errors))