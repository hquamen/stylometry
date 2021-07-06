# Verb locator
##############################################################
#
#	This code looks through a directory of POS marked files
#	and finds sentences where the POS is in the "target zone."
#
##############################################################

import os
import re

BLANK = re.compile(r'^\s*$')
COMMENT = re.compile(r'^\s*#')
SENTENCE_REGEX = re.compile(r'(\._\.)|(!_!)|(:_:)')
QUESTION_MARK_REGEX = re.compile(r'\?_\?')
CAP_LETTER_REGEX = re.compile(r'^[A-Z]')
MULT_SPACE = re.compile(r'\s{2,}')
NOT_PUNCTUATION = re.compile(r'[A-Za-z]')
REMOVE_POS = re.compile(r'_\S+')

TARGET_LOW = 98
TARGET_HIGH = 100

DEBUG = False
STATUS_REPORT = True

APPROVED_SENTENCE_LENGTH = 10
SKIP_POS_ENDING_WITH = "I"

POS_TAG_TO_FIND = "V"

# PROSE DOCS
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/'
# TEXT = '17c Prose'

# POETRY DOCS
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/poetry/'
# TEXT = '17c Poetry'

# MILTON PARADISE LOST
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/paradise_lost_POS/'
# TEXT = 'Paradise Lost'

# MILTON PROSE
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/'
# TEXT = 'Milton Prose'

# MILTON POETRY
# path = ''
# TEXT = 'Milton Poetry'

# MILTON AREOPAGITICA
path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/areopagitica/'
TEXT = 'Areopagitica'


# TEST
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/delme_tests/'
# TEXT = 'Test'

files = [f for f in os.listdir(path) if f.endswith('.txt')]
files.sort()


#
#	FUNCTIONS
#


def clean_tokens(tokens):
	"""Return a list of word tokens with punctuation tokens removed."""
	return [w for w in tokens if NOT_PUNCTUATION.search(w)]

def find_matches(sentences):
	"""Given a list of sentences, this function prints the sentences that
	have a verb located between TARGET_LOW and TARGET_HIGH."""
	for sentence_number, sentence in enumerate(sentences):
		locations = locate_pos_in_sentence(sentence)
		matching_sentence = False
		matches = []
		for location in locations:
			if location >= TARGET_LOW and location <= TARGET_HIGH:
				matching_sentence = True
				# Add rounded % to list; we'll join() later, so stringify it
				matches.append(str(round(location,2)))
		if matching_sentence:
			print('\n{}:{}\n{}'.format(file, sentence_number + 1, ' '.join(sentence)) )
			print(REMOVE_POS.sub("", " ".join(sentence)))
			print(', '.join(matches))
			print()

def locate_pos_in_sentence(tokens, pos_tag = 'V'):
	"""This function calculates the location(s) of any POS in one tokenized sentence."""
	locations = []
	words = clean_tokens(tokens)
	sentence_length = len(words)
	# ignore the sentence if it's zero or one word long;
	# return an empty list, which extend() will ignore.
	if sentence_length < APPROVED_SENTENCE_LENGTH:
		return []
	for word_num, token in enumerate(words):
		try:
			word, pos = token.split('_')
		except:
			print(words, token)
			exit()				# somebody is barfing in PL
		if pos.startswith(POS_TAG_TO_FIND):
			if pos.endswith(SKIP_POS_ENDING_WITH):
				continue
			# append to list as a percentage
			tokens_in_front = word_num
			tokens_behind = sentence_length - word_num - 1
			if DEBUG:
				print("------- DEBUG {} in front; {} behind.".format(tokens_in_front, tokens_behind))
			if tokens_behind < 0:
				print(tokens)
				exit()
			if tokens_in_front + tokens_behind == 0:
				print(words)
				exit()
			locations.append(tokens_in_front / (tokens_in_front + tokens_behind) * 100)
	locations.sort()
	return locations


def parse_sentences(tokens):
	"""Given a list of tokens, this function parses them into sentences. 
	This function allows us to change the grammatical rules for various time periods."""
	sentences = []
	current_sentence = []
	while len(tokens) > 0:
		token = tokens.pop(0)
		# are we at a sentence boundary?
		if SENTENCE_REGEX.search(token):
			current_sentence.append(token)
			sentences.append(current_sentence)
			current_sentence = []
			continue
		if QUESTION_MARK_REGEX.search(token):
			try:
				if CAP_LETTER_REGEX.search(tokens[0]):
					# have new sentence
					current_sentence.append(token)
					sentences.append(current_sentence)
					current_sentence = []
					continue
			except:
				pass
		current_sentence.append(token)
	# if we have anything left over, push it
	if len(current_sentence) > 0:
		sentences.append(current_sentence)
	return sentences

def per_mille(raw_count):
	"""Convert counts to number of occurrences per 1000 (per mille)."""
	return [val * 1000 / document_word_count for val in raw_count]

def tokenize(text):
	"""Tokenize a string text; split on spaces."""
	text = text.replace('\n', ' ')
	text = MULT_SPACE.sub(' ', text).strip()
	tokens = text.split()
	return [t.strip() for t in tokens if len(t.strip()) > 0]

def word_count(tokens):
	"""Counts non-punctuation tokens; works for whole docs or just sentences."""
	return len(clean_tokens(tokens))


#
#	PROCESS THE FILES IN path VARIABLE
#

corpus_word_count = 0
sentences = []

for file in files:
	if not file.endswith('.txt'):
		continue
	print('\n----------- LOOKING AT {} ----------------\n'.format(file))
	with open(path + file) as f:
		lines = f.readlines()
	clean_lines = [line for line in lines if not BLANK.match(line) and not COMMENT.match(line)]
	text = ' '.join(clean_lines)
	tokens = tokenize(text)
	sentences = []

	if DEBUG:
		print('______________')
		print(tokens)
		print('______________')


	document_word_count = word_count(tokens)
	corpus_word_count += document_word_count
	sentences = parse_sentences(tokens)
	if STATUS_REPORT:
		print("Document Word count: {}".format(document_word_count))
		print("Corpus Word count: {}".format(corpus_word_count))
		print("Sentence count: {}".format(len(sentences)))
		avg = document_word_count / len(sentences)
		print('\tAverage Sentence length: {}'.format(avg))

	# print("Loop finished: {} sentences in corpus.".format(len(sentences)))
	find_matches(sentences)


