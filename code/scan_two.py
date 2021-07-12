#####################################################
#
# Harvey Quamen
# University of Alberta
#
# This script scans two texts and compares
# them word by word to find divergences in
# the two texts.
#
# How? That's an interesting puzzle.
# I calculate a Jaccard Similarity
# and keep a running tally of how many in a row
# are below a certain threshold. That's a fairly
# good indicator that tells us when the two
# texts diverge from each other.
#####################################################

import re

path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/Areo_exp/'
olde = 'Areopagitica_olde_fixed.txt'
newe = 'Areopagitica_new_fixed.txt'

MULT_SPACE = re.compile(r'\s{2,}')
NON_WORD = re.compile(r'\W+')

THRESHOLD = 0.85	# what's considered a low score?
LIMIT = 5			# how many low scores in a row before stopping?

def tokenize(text):
	text = text.replace('\n', ' ')
	#text = text.replace('-', ' ')	# leave this!
	MULT_SPACE.sub(' ', text)
	text = text.strip()
	return text.split()

with open(path + olde) as f:
	areo_old = f.read()

with open(path + newe) as f:
	areo_new = f.read()

old_tokens = tokenize(areo_old)
old_wordcount = len(old_tokens)

new_tokens = tokenize(areo_new)
new_wordcount = len(new_tokens)

# No sense scanning past the shorest text. How long is it?
words = min([old_wordcount, new_wordcount])


print("Old wordcount: {}; New wordcount: {}".format(len(old_tokens), len(new_tokens)))

low_scores_in_a_row = []

for num in range(words):
	old_set = set(NON_WORD.sub('', old_tokens[num]).lower())
	new_set = set(NON_WORD.sub('', new_tokens[num]).lower())
	jaccard_score = len(old_set.intersection(new_set)) / len(old_set.union(new_set))
	print(num, old_tokens[num], new_tokens[num], round(jaccard_score, 2))
	if jaccard_score > THRESHOLD:
		low_scores_in_a_row = []
	else:
		low_scores_in_a_row.append(jaccard_score)
		if len(low_scores_in_a_row) > LIMIT:
			print("Too many low scores. Texts have diverged. Stopping.")
			exit()


