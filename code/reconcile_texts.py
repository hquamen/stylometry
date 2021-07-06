# This script scans two texts and compares
# them word by word. It also:
#	1. Keeps new spelling
#	2. Keeps old punctuation
#	3. Tries to reconcile the lists when the tokens mismatch.
#


import re
import string
import textwrap

path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/Areo_exp/'
olde = 'Areopagitica_olde_fixed.txt'
newe = 'Areopagitica_new_fixed.txt'


STATUS_REPORT = True

MULT_SPACE = re.compile(r'\s{2,}')
NON_WORD = re.compile(r'\W+')

# add apostrophe to alphabet, but leave hyphen as punctuation to be tokenized
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + "'"
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
	'2': 'two',
	'3': 'three',
	'4': 'four',
	'5': 'five',
	'&c.': 'etc.',
	'&': 'and',
	"dy'd": 'died',
	'oyle': 'oil',
	'frie': 'fry',
	'som times': 'sometimes',
	'any body': 'anybody',
	'any one': 'anyone',
	'mean while': 'meanwhile',
	'it selfe': 'itselfe',
	'mid air': 'mid-air',
	'Hell-gate': 'Hell Gate',		# Argh. Milton's was better. Who changes this?!
	'Hell-gates': 'Hell Gates',
	'hell-gate': 'Hell Gate',
	"T' whom": 'To whom',			# better POS (thinks t' is "the")
	"t' whom": 'to whom',			# better POS
	"Ith'": "In the",				# better POS (thinks i' is a verb)
	"I' the": 'In the'
}

THRESHOLD = 0.5		# what's considered a low score?
LIMIT = 5			# how many low scores in a row before stopping?
WIDTH = 80

def calculate_jaccard(a, b):
	# Not using this right now!
	old = set(NON_WORD.sub('', a).lower())
	new = set(NON_WORD.sub('', b).lower())
	try:
		answer = len(old.intersection(new)) / len(old.union(new))
	except:
		answer = 0
	return answer

def buildlines(tokens):
	new_string = ' '.join(tokens)
	for bad, good in REPLACEMENTS.items():
		new_string = new_string.replace(bad, good)
	new_string = new_string.strip()
	lines = textwrap.wrap(new_string, WIDTH)
	return '\n'.join(lines)

def fix_spellings(line):
	for wrong, right in SPELLING.items():
		line = line.replace(wrong, right)
	return line

def is_word(word):
	for letter in word:
		if letter not in ALPHABET:
			return False
	return True

def tokenize(orig_text):
	text = orig_text.replace('\n', ' ')
	text = fix_spellings(text)
	text = MULT_SPACE.sub(' ', text).strip()
	
	# print(text)
	tokens = []
	current_token = []
	for letter in text:
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


#########################################################
#
#	LOAD FILES and TOKENIZE
#
#########################################################

with open(path + olde) as f:
	old_text = f.read()

with open(path + newe) as f:
	mod_text = f.read()

old = tokenize(old_text)
old_wordcount = len(old)
# print("OLD: {}".format(old))

modern = tokenize(mod_text)
modern_wordcount = len(modern)
# print("MOD: {}".format(modern))

min_wordcount = min([old_wordcount, modern_wordcount])
max_wordcount = max([old_wordcount, modern_wordcount])

if STATUS_REPORT:
	print("Old wordcount: {}; New wordcount: {}".format(len(old), len(modern)))

#	SET UP FOR LOOP

low_scores_in_a_row = []
reconciled_tokens = []
old_word_num = 0
mod_word_num = 0
out_of_synch = 0

# dunno if this is the proper boolean test here:
while old_word_num < len(old) and mod_word_num < len(modern):

	if out_of_synch > LIMIT:
		print("Hit out-of-synch limit. Stopping.")
		exit()

	# Six cases to handle when reconciling:

	# 1. Both have a word
	if is_word(modern[mod_word_num]) and is_word(old[old_word_num]):
		# check jaccard similarity:
		if calculate_jaccard(modern[mod_word_num], old[old_word_num]) < THRESHOLD:
			print("\nWords out of synch")
			print("\tMod {}: ".format(mod_word_num), end = ', ')
			print(modern[mod_word_num - 5: mod_word_num + 5])
			print("\tOld {}: ".format(old_word_num), end = ', ')
			print(old[old_word_num - 5: old_word_num + 5])
			# increment our out_of_synch counter; push words as normal (for now!)
			out_of_synch += 1
		else:
			out_of_synch = 0
		# advance both pointers; keep modern spelling word
		reconciled_tokens.append(modern[mod_word_num])
		mod_word_num += 1
		old_word_num += 1
		# out_of_synch = 0
		continue
	
	# new 2. modern is hyphen and old is word
	#		NOT SURE WHAT TO DO HERE.
	if modern[mod_word_num] == '-' and is_word(old[old_word_num]):
		reconciled_tokens.append(modern[mod_word_num])
		# for now, advance modern pointer; check this with "Hell-gate" or something
		mod_word_num += 1
		# out_of_synch = 0
		continue
	
	# 3. modern is punctuation AND old is word
	if not is_word(modern[mod_word_num]) and is_word(old[old_word_num]):
		# advance modern pointer; ignore it b/c punct; continue
		mod_word_num += 1
		# out_of_synch = 0
		continue
	
	# 4. modern is word and old is punct:
	if is_word(modern[mod_word_num]) and not is_word(old[old_word_num]):
		# keep old punctuation and advance old pointer
		reconciled_tokens.append(old[old_word_num])
		old_word_num += 1
		# out_of_synch = 0
		continue
	
	# 5. both are punctuation:
	if not is_word(modern[mod_word_num]) and not is_word(old[old_word_num]):
		# advance both, but keep only the old punctuation
		reconciled_tokens.append(old[old_word_num])
		old_word_num += 1
		mod_word_num += 1
		# out_of_synch = 0
		continue

	# 6. We're out of synch; we get here only if all conditionals above are false
	print("\nOut of synch")
	print("Modern: ", mod[mod_word_num:])
	print("Old tx: ", old[old_word_num:])
	out_of_synch += 1

	
print("Loop done.\n")
print(buildlines(reconciled_tokens))



"""# check to see if we have anything left over:
if len(modern) > word_num:
	# probably left-over punctuation; skip it?
	# reconciled_tokens.extend(modern)
	pass
elif len(old) > 0:
	reconciled_tokens.extend(old)"""

