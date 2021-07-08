#############################################################
# Finding depictive adjectives in Paradise Lost
#
#	the pattern is "verb [not infinitive] + JJ* + [^Noun]"
#
# See Daniel Shore's Chapter 6 in "Cyberformalism" for more
#	on these. Great example of a grammatical pattern, but it
#	wasn't my main focus. So this is a copy-n-paste modify of
#	the ablative code.
#############################################################


import os
import re
import string

# point to the directory where the texts are:
text_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/paradise_lost_POS/'
# text_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/areopagitica/'


############################################################
#
# Jonson Sentences
#	The terms 'perfect sentence' and 'imperfect sentence'
#	come from Ben Jonson's _English Grammar_ (1648).
#	See pp. 74-77.
#
############################################################

perfect_pauses = ['._.', ':_:', '?_?', '!_!']
imperfect_pauses = [';_;', ',_,']
all_pauses = perfect_pauses + imperfect_pauses

MULT_SPACE = re.compile(r'\s{2,}')

def is_depictive(tokens):
	"""Use a little FSM to find the simple pattern; there
	may be words in the middle, so keeping state is a good
	way to skip optional words."""
	
	have_verb = False
	have_adjective = False

	for i in range(len(tokens)):
		word, pos = tokens[i].split("_")
		if have_adjective:
			if pos.startswith("N"):
				have_adjective = False
				continue
			else:
				# this is our best case
				print(tokens)
				return True
		if pos.startswith("J") and have_verb:
			have_adjective = True
			have_verb = False
			continue
		if pos.startswith("V") and not pos.endswith("I"):
			# print("Checking VERB {} {}".format(word, pos))
			have_verb = True
			continue
		have_verb = False
	return False


def jonson_split(tokens):
	"""Split sequences of tokens into 'Jonsonian' sentences."""
	sentences = []
	current_sentence = []
	for token in tokens:
		current_sentence.append(token)

		# find a better way to split differently:
		if token in perfect_pauses:

			sentences.append(current_sentence)
			current_sentence = []
			continue
	# append what's left over
	if len(current_sentence) > 0:
		sentences.append(current_sentence)
	return sentences

def tokenize(orig_text):
	"""Clean up text and return tokens (includes punctuation tokens)"""
	text = orig_text.replace('\n', ' ')
	text = MULT_SPACE.sub(' ', text).strip()
	tokens = text.split()
	return [t.strip() for t in tokens if len(t.strip()) > 0]

def get_sentence(tokens):
	"""Return a slightly cleaner sentence w/o POS tags."""
	words = [t.split("_")[0] for t in tokens]
	return " ".join(words)

texts = [f for f in os.listdir(text_directory) if f.endswith('.txt')]
texts.sort()
for book_file in texts:

	print("\n---------- Book {}\n".format(book_file))
	
	with open(text_directory + book_file) as f:
		text = f.read()

	tokens = tokenize(text)
	sentences = jonson_split(tokens)

	for sentence in sentences:
		if is_depictive(sentence):
			print(get_sentence(sentence))
			print()

