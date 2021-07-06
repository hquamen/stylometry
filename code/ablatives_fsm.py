# Finding ablative absolutes in Paradise Lost
#	MORE SOPHISTICATED VERSION
#
#	the pattern is "with noun having been verbed"
#	"with [noun] [participle]"
#
#	often with:
#		when, as, after, since, because, although
#		by, with, from, than, on, in, at
#
#	So break things into Jonsonian groups and then
#	look for some pattern like "with"? followed by N.+ followed by V.+
#
#	LOOKING FOR:
#	IW	with, without (as prepositions)
#	N or P ==> either a noun or a pronoun
#	VVD	past tense of lexical verb (e.g. gave, worked)
#


import os
import re

# pl_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/paradise_lost_POS/'
pl_directory = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/areopagitica/'

# The terms 'perfect sentence' and 'imperfect sentence'
# come from Ben Jonson's _English Grammar_ (1648).
# See pp. 74-77.
perfect_pauses = ['._.', ':_:', '?_?', '!_!']
imperfect_pauses = [';_;', ',_,']
all_pauses = perfect_pauses + imperfect_pauses

# These are the POS for pronouns in the subjective case
SUBJECTIVE_PRONOUNS = ['PNQS', 'PPHS1', 'PPHS2', 'PPIS1', 'PPIS2']

MULT_SPACE = re.compile(r'\s{2,}')

def is_albative(tokens):
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
	text = orig_text.replace('\n', ' ')
	text = MULT_SPACE.sub(' ', text).strip()
	tokens = text.split()
	return [t.strip() for t in tokens if len(t.strip()) > 0]


pl_texts = [f for f in os.listdir(pl_directory) if f.endswith('.txt')]
pl_texts.sort()
for book_file in pl_texts:

	print("\n---------- Book {}\n".format(book_file))
	
	with open(pl_directory + book_file) as f:
		text = f.read()

	tokens = tokenize(text)
	sentences = jonson_split(tokens)

	for sentence in sentences:
		if is_albative(sentence):
			print(sentence)



