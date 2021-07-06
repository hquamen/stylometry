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

PRONOUNS = ["APPGE", "DA", "DA1", "DA2", "DAR", "DAT", "DB", "DB2", "DD", "DD1", "DD2", "DDQ", "DDQGE", "DDQV", "ND1", "NN", "NN1", "NN2", "NNA", "NNB", "NNL1", "NNL2", "NNO", "NNO2", "NNT1", "NNT2", "NNU", "NNU1", "NNU2", "NP", "NP1", "NP2", "NPD1", "NPD2", "NPM1", "NPM2", "PN", "PN1", "PNQO", "PNX1", "PPH1", "PPHO1", "PPHO2", "PPIO1", "PPIO2", "PPX1", "PPX2", "PPY"]
VERBS = ["JJ", "JJR", "JJT", "JK", "VH0", "VHD", "VHN", "VVD", "VVG", "VVN", "VVNK"]
PUNCT = [".", ',', ':', ';', '!', '?']

def is_ablative(tokens):
	# looking for a four-unit sequence of tokens:
	#	punct + [pronoun] + [verb] + punct
	token_count = len(tokens)
	# print("{} tokens:".format(token_count))
	# print(tokens)
	if token_count < 4:
		return False

	for i in range(token_count - 3):
		one_word, one_pos = tokens[i].split("_")
		two_word, two_pos = tokens[i + 1].split("_")
		three_word, three_pos = tokens[i + 2].split("_")
		four_word, four_pos = tokens[i + 3].split("_")
		# print("\n----- POS: {} | {} | {} | {}".format(one_pos, two_pos, three_pos, four_pos))
		if one_pos in PUNCT:
			if two_pos in PRONOUNS:
				if three_pos in VERBS:
					if four_pos in PUNCT:
						# print("have ablative")
						return True
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
		if is_ablative(sentence):
			print("-" * 25)
			print(sentence)
			print(get_sentence(sentence))
			print()

# text = "Deity_NN1 supreme_JJ ,_, us_PPIO2 dispossessed_VVD ,_,"
# tokens = tokenize(text)
# is_ablative(tokens)


