###############################################################
#
# Harvey Quamen
# University of Alberta
#
# auto-change punctuation. This reduced 3700+ lines down
# to 14 that needed to be tweaked by hand.
# This still has problems with hyphenated lines, but the
# problem might stem from the 20c edition of Paradise Lost,
# which loved to hyphenate compound nouns, even when not
# necessary. So check for hyphenated words and test this code
# to make sure it treats hyphenations properly.
#
###############################################################

import os
import re
import string

BLANK = re.compile(r'^\s*$')
COMMENT = re.compile(r'^\s*#')
MULT_SPACE = re.compile(r'\s{2,}')

PUNCTUATION = '.,;:?!-—–()'
REPLACEMENTS = {
	' .': '.',
	' ,': ',',
	' ;': ';',
	' ?': '?',
	' !': '!',
	' :': ':',
	' )': ')',
	'( ': '(',
	' - ': '-'
}

# Adjust some spellings that will give us problems; spelling
# checks must be done before tokenization happens.
SPELLING = {
	'som times': 'sometimes',
	'mid air': 'mid-air',
	'Hell-gate': 'Hell Gate',		# Argh. Milton's was better. Who changes this?!
	'Hell-gates': 'Hell Gates',
	'hell-gate': 'Hell Gate',
	"T' whom": 'To whom',			# better POS (thinks t' is "the")
	"t' whom": 'to whom',			# better POS
	"Ith'": "In the",				# better POS (thinks i' is a verb)
	"I' the": 'In the'
}

MILTON = 'autopunk/milton.txt'
MODERN = 'autopunk/modern.txt'

MILTON_DIR = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/rdc/'
MILTON_PREFIX = 'rdc_PL_'
MODERN_DIR = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/old_hq/'
MODERN_PREFIX = 'oldhq_PL_'
OUTPUT_DIR = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/punctuation/hq/'
OUTPUT_PREFIX = 'hq_PL_'

# add apostrophe to alphabet, but leave hyphen as punctuation to be tokenized
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + "'"

def is_word(word):
	for letter in word:
		if letter not in ALPHABET:
			return False
	return True

def fix_spellings(line):
	for wrong, right in SPELLING.items():
		line = line.replace(wrong, right)
	return line

def compose(tokens):
	new_string = ' '.join(tokens)
	for bad, good in REPLACEMENTS.items():
		new_string = new_string.replace(bad, good)
	return new_string.strip()


def reconcile(modern, old):
	new_tokens = []
	# Five cases to handle when reconciling:
	while len(modern) > 0 and len(old) > 0:
		# 1. Both have a word
		if is_word(modern[0]) and is_word(old[0]):
			# pop both; keep modern spelling word
			old.pop(0)
			new_tokens.append(modern.pop(0))
			continue
		# new 2. modern is hyphen and old is word
		if modern[0] == '-' and is_word(old[0]):
			new_tokens.append(modern.pop(0))
			continue
		# 3. modern is punct AND old is word
		if not is_word(modern[0]) and is_word(old[0]):
			# pop modern; ignore it b/c punct; continue
			modern.pop(0)
			continue
		# 4. modern is word and old is punct:
		if is_word(modern[0]) and not is_word(old[0]):
			# pop old and push it to new tokens
			new_tokens.append(old.pop(0))
			continue
		# 5. both are punctuation:
		if not is_word(modern[0]) and not is_word(old[0]):
			# pop both, but keep only the old punctuation
			modern.pop(0)
			new_tokens.append(old.pop(0))
		else:
			# some kind of error; let's find out
			print("Error -- MODERN is:")
			print(modern)
			print("OLD:")
			print(old)
			exit()
	# check to see if we have anything left over:
	if len(modern) > 0:
		# probably left-over punctuation; skip it?
		# new_tokens.extend(modern)
		pass
	elif len(old) > 0:
		new_tokens.extend(old)
	return new_tokens


def tokenize(input_line):
	line = MULT_SPACE.sub(' ', input_line).strip()
	# Fix spelling before tokenization:
	line = fix_spellings(line)
	# print(line)
	tokens = []
	current_token = []
	for letter in line:
		# print('----------', letter)
		if letter in ALPHABET:
			# print("In alphabet, pushing {}".format(letter))
			current_token.append(letter)
			continue
		if letter == ' ':
			# print("Have space:")
			if len(current_token) != 0:
				tokens.append(''.join(current_token))
				current_token = []
				# print("\tPushed tokens.")
			continue
		if letter in PUNCTUATION:
			# print("Letter in punct: {}".format(letter))
			if len(current_token) > 0:
				tokens.append(''.join(current_token))
			tokens.append(''.join(letter))
			# print("Appended {} to tokens.".format(letter))
			current_token = []
	# push remainder as a new token
	tokens.append(''.join(current_token))
	# print(tokens)
	return [t for t in tokens if len(t) > 0]

#############################################################
#
#	FIND FILES
#
#############################################################

milton_files = [f for f in os.listdir(MILTON_DIR) if f.endswith('.txt')]
milton_files.sort()

modern_files = [f for f in os.listdir(MODERN_DIR) if f.endswith('.txt')]
modern_files.sort()

if len(milton_files) != len(modern_files):
	print("Unequal number of .txt files in each directory. Check 'em!")
	exit()

num_files = len(milton_files)

for file_num in range(1, num_files + 1):
	new_lines = []
	book = "{:02d}.txt".format(file_num)

	milton_file = MILTON_DIR + MILTON_PREFIX + book
	if not os.path.isfile(milton_file):
		print("Does not exist: {}".format(milton_file))
		exit()

	modern_file = MODERN_DIR + MODERN_PREFIX + book
	if not os.path.isfile(modern_file):
		print("Does not exist: {}".format(modern_file))
		exit()

	output_file = OUTPUT_DIR + OUTPUT_PREFIX + book
	
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
	#	WRITE!
	#

	for line_num in range(len(milton_lines)):

		mil = tokenize(milton_lines[line_num])
		mod = tokenize(modern_lines[line_num])

		new_tokens = reconcile(modern = mod, old = mil)
		new_lines.append(compose(new_tokens) + "\n")
		# print()
		# print('Milton: {}'.format(milton_lines[line_num]))
		# print('Modern: {}'.format(modern_lines[line_num]))
		# print(' Fixed: {}'.format(sentence))
	
	print("----- Writing Book {}".format(file_num))
	with open(output_file, 'w') as f:
		f.writelines(new_lines)
	
