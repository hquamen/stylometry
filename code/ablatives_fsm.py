############################################################
#
# Harvey Quamen
# University of Albeta
#
# Finding ablative absolutes in Paradise Lost
#	with a Finite State Machine
#
#	the pattern is "with noun having been verbed"
#	"with [noun] [participle]"
#
#	often introduced with:
#		when, as, after, since, because, although
#		by, with, from, than, on, in, at
#
#	So first break tokens into Jonsonian "sentences" and then
#	look for some pattern like "with"? followed by N.+ followed by V.+
#
#	LOOKING FOR:
#	IW	with, without (as prepositions)
#	N or P ==> either a noun or a pronoun
#	VVD	past tense of lexical verb (e.g. gave, worked)
#
############################################################

import os
import re

# regular expression for removing multiple spaces
MULT_SPACE = re.compile(r'\s{2,}')


# text_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/paradise_lost_POS/'
text_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/areopagitica/'

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

# These are the POS for pronouns in the subjective case
SUBJECTIVE_PRONOUNS = ['PNQS', 'PPHS1', 'PPHS2', 'PPIS1', 'PPIS2']


def is_albative(tokens):
	"""Use a Finite State Machine to look for patterns
	of [with] + [noun|pronoun] + [verb]"""
	state = None
	for i in range(len(tokens)):
		word, pos = tokens[i].split('_')
		if pos == 'IW':
			state = 'WITH'
		if pos[0] == 'N':
			if state == 'WITH':
				state = 'NOUN'
		if pos[0] == 'P':
			if pos not in SUBJECTIVE_PRONOUNS:
				if state == 'WITH':
					state = 'NOUN'
		if pos[0] == 'V':
			if state == "NOUN" and tokens[i + 1] in all_pauses:
				state = 'ABLATIVE'
	return state == "ABLATIVE"


def jonson_split(tokens):
	"""Split sequences of tokens into 'Jonsonian' sentences."""
	sentences = []
	current_sentence = []
	for token in tokens:
		current_sentence.append(token)
		if token in all_pauses:
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


texts = [f for f in os.listdir(text_directory) if f.endswith('.txt')]
texts.sort()
for book_file in texts:

	print("\n---------- Book {}\n".format(book_file))
	
	with open(text_directory + book_file) as f:
		text = f.read()

	tokens = tokenize(text)
	sentences = jonson_split(tokens)

	for sentence in sentences:
		if is_albative(sentence):
			print(sentence)



