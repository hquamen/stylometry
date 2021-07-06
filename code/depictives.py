# Finding depictive adjectives in Paradise Lost
#	MORE SOPHISTICATED VERSION
#
#	the pattern is "verb [not infinitive] + JJ* + [^Noun]"
#
#	often with:
#		when, as, after, since, because, although
#		by, with, from, than, on, in, at
#

#	IN PROGRESS --  JUST BARELY STARTED





import os
import re  # not really used right now.
import string

pl_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/paradise_lost_POS/'
# pl_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/areopagitica/'

# The terms 'perfect sentence' and 'imperfect sentence'
# come from Ben Jonson's _English Grammar_ (1648).
# See pp. 74-77.
perfect_pauses = ['._.', ':_:', '?_?', '!_!']
imperfect_pauses = [';_;', ',_,']
all_pauses = perfect_pauses + imperfect_pauses

MULT_SPACE = re.compile(r'\s{2,}')
DEPICTIVE = re.compile(r'_V.{2}\s\w+_JJ')

def is_depictive(tokens):
	# problem: this needs to be in a limited window, not just a verb
	#	plus an adjective later plus a punct.
	# state = None
	# for i in range(len(tokens)):
	# 	word, pos = tokens[i].split('_')
	# 	if pos[0] == 'V' and not pos.endswith("I"):
	# 		state = 'VERB'
	# 	if pos[0] == 'J':
	# 		if state == 'VERB':
	# 			state = 'ADJ'
	# 	if pos[0] in string.punctuation:
	# 		if state == 'ADJ':
	# 			state = 'DEPICTIVE'
	# return state == "DEPICTIVE"
	
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
	text = orig_text.replace('\n', ' ')
	text = MULT_SPACE.sub(' ', text).strip()
	tokens = text.split()
	return [t.strip() for t in tokens if len(t.strip()) > 0]

def get_sentence(tokens):
	words = [t.split("_")[0] for t in tokens]
	return " ".join(words)

pl_texts = [f for f in os.listdir(pl_directory) if f.endswith('.txt')]
pl_texts.sort()
for book_file in pl_texts:

	print("\n---------- Book {}\n".format(book_file))
	
	with open(pl_directory + book_file) as f:
		text = f.read()

	tokens = tokenize(text)
	sentences = jonson_split(tokens)

	for sentence in sentences:
		if is_depictive(sentence):
			print(get_sentence(sentence))
			print()




