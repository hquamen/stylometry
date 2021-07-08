#########################################################
#
#	Harvey Quamen
#	University of Alberta
#
# A script to verify correct capitalization.
# In Milton, this is important because if he uses
# a capital letter after ? then it's a new sentence;
# if lowercase after ? then it's the same sentence.
#
# This script compares a directory of modern spelling texts
# versus a directory of 17th-century spelling texts. If the
# two disagree, the script says so.
#
#########################################################

import os
import re

BLANK = re.compile(r'^\s*$')
COMMENT = re.compile(r'^\s*#')

#
#	I'm reconciling two texts: one is the modern spelling and one is the
#	17th century spelling from Richard Cunningham's project.
#
MILTON_DIR = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/rdc/'
MILTON_PREFIX = 'rdc_PL_'
MODERN_DIR = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/hq/'
MODERN_PREFIX = 'hq_PL_'

QUESTION = '?'
EXCLAMATION = '!'

def get_next_letter(line, location):
	for letter in line[location:]:
		if letter.isalpha():
			return letter
	return None

milton_files = [f for f in os.listdir(MILTON_DIR) if f.endswith('.txt')]
milton_files.sort()

modern_files = [f for f in os.listdir(MODERN_DIR) if f.endswith('.txt')]
modern_files.sort()

if len(milton_files) != len(modern_files):
	print("Unequal number of .txt files in each directory. Check 'em!")
	exit()

num_files = len(milton_files)

for file_num in range(1, num_files + 1):
	print("\n------------------ Checking Book {} ---------".format(file_num))

	book = "{:02d}.txt".format(file_num)

	milton_file = MILTON_DIR + MILTON_PREFIX + book
	if not os.path.isfile(milton_file):
		print("Does not exist: {}".format(milton_file))
		exit()

	modern_file = MODERN_DIR + MODERN_PREFIX + book
	if not os.path.isfile(modern_file):
		print("Does not exist: {}".format(modern_file))
		exit()
	
	with open(milton_file) as f:
		milton_lines = [line.strip() for line in f.readlines() if not BLANK.match(line) \
			and not COMMENT.match(line)]

	with open(modern_file) as f:
		modern_lines = [line.strip() for line in f.readlines() if not BLANK.match(line) \
			and not COMMENT.match(line)]

	if len(milton_lines) != len(modern_lines):
		print("Unequal # of Lines in book {}.".format(file_num))
		exit()

	#
	#	CHECK PUNCTUATION + CAPITALIZATION
	#

	for line_num in range(len(milton_lines)):

		for punct in [QUESTION, EXCLAMATION]:
			modern_letter = None
			milton_letter = None
			try:
				location = modern_lines[line_num].index(punct)
				modern_letter = get_next_letter(modern_lines[line_num], location)
				if modern_letter is None:
					continue
			except:
				continue

			try:
				milt_location = milton_lines[line_num].index(punct)
				milton_letter = get_next_letter(milton_lines[line_num], milt_location)
				if milton_letter is None:
					continue
			except:
				continue
			
			if modern_letter != milton_letter:
				print()
				print("Mod: {}; Milton: {}".format(modern_letter, milton_letter))
				print("Capitalization error: Book {}; Line {}".format(file_num, line_num))
				print("Mod: {}".format(modern_lines[line_num]))
				print("Mil: {}".format(milton_lines[line_num]))


