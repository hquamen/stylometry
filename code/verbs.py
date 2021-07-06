# Verb locator
##############################################################
#
#	This code looks through a directory of POS marked files
#	and reads each document, skipping lines with '#' and blank lines.
#	It then parses the text into sentences according to 17c rules.
#	It then calculates where the verbs are in those sentences,
#	and outputs CSV, suitable for graphing.
#
#	NEED:
#		word count w/o punctuation (for the per_mille scale)
#		sentence length w/o punctuation (for per_cent scale)

#	TO DO:
#	make sure this works for both a document and a corpus
#	-- Milton doesn't always split a sentence on '!' either. Check caps.
#
##############################################################

import os
import re
import collections

BLANK = re.compile(r'^\s*$')
COMMENT = re.compile(r'^\s*#')
SENTENCE_REGEX = re.compile(r'(\._\.)|(:_:)')
QUESTION_MARK_REGEX = re.compile(r'\?_\?')
MAYBE_SENTENCE_REGEX = re.compile(r'(\?_\?)|(!_!)')
CAP_LETTER_REGEX = re.compile(r'^[A-Z]')
MULT_SPACE = re.compile(r'\s{2,}')
NOT_PUNCTUATION = re.compile(r'[A-Za-z]')
ETC = re.compile(r'&c\.;')
et_cetera = 'et_RR21 cetera_RR22 ;_;'

#	GLOBALS

BIN_SIZE = 5	# percentage size of the bin; 5% == 20 bins

DEBUG = False
STATUS_REPORT = False

HEADER = ['location','frequency','text']
TEXT = 'Prose'

APPROVED_SENTENCE_LENGTH = 10
SKIP_POS_ENDING_WITH = "I"		# These POS are all infinitives in CLAWS

POS_TAG_TO_FIND = "V"

MINIMUM_WINDOW = 98

pos_counter = collections.Counter()

##############################################################
#
# 	PATHS
#
##############################################################

# PROSE DOCS
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/'
# TEXT = '17c Prose'

# POETRY DOCS
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/poetry/'
# TEXT = '17c Poetry'

# MILTON PARADISE LOST
path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/paradise_lost_POS/'
TEXT = 'Paradise Lost'

# MILTON PROSE
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/'
# TEXT = 'Milton Prose'

# MILTON POETRY
# path = ''
# TEXT = 'Milton Poetry'

# MILTON AREOPAGITICA
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/milton/areopagitica/'
# TEXT = 'Areopagitica'

# KJV GENESIS
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/kjv_bible/'
# TEXT = 'KJV Genesis'

# GENEVA GENESIS
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/geneva/'
# TEXT = 'Geneva Genesis'

# TEST
# path = '/Users/hquamen/Documents/Literary_Style_Project/Milton_Style_article/texts/delme_tests/'
# TEXT = 'Test'


##############################################################
#
#	FUNCTIONS
#
##############################################################



def tokenize(text):
	"""Tokenize a string text; split on spaces."""
	text = text.replace('\n', ' ')
	text = MULT_SPACE.sub(' ', text).strip()
	tokens = text.split()
	return [t.strip() for t in tokens if len(t.strip()) > 0]

def parse_sentences(original_tokens):
	"""Given a text, this function parses the tokenized text into sentences. 
	Using the regexes defined in this file, this function allows us to change 
	the grammatical rules for various time periods."""
	tokens = original_tokens.copy()
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
		if MAYBE_SENTENCE_REGEX.search(token):
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


#
#	HISTOGRAM
#

def make_histogram(locations):
	bins = bin_percentages(locations)
	return per_mille(bins)

def bin_percentages(raw_list):
	"""This function bins raw counts for histogram viz. I just don't do it in R."""
	num_bins = int(100 / BIN_SIZE)
	binned = [0] * num_bins
	for item in raw_list:
		index = int(item // BIN_SIZE)
		if index > 19:
			index = 19
		binned[index] += 1
	return binned

def per_mille(raw_count):
	"""Convert counts to number of occurrences per 1000 (per mille)."""
	return [val * 1000 / corpus_word_count for val in raw_count]


#
#	TOKENIZER / LOCATION
#

def clean_tokens(tokens):
	"""Return a list of word tokens with punctuation tokens removed."""
	# Problem: this might be a list or else a list of lists. Flatten, if so.
	try:
		if isinstance(tokens[0], list):
			flat = [item for sublist in tokens for item in sublist]
			tokens = flat
	except:
		pass
	return [w for w in tokens if NOT_PUNCTUATION.search(w)]

def word_count(tokens):
	"""Counts non-punctuation tokens; works for whole docs or just sentences."""
	print('\t -- in word_count, raw length = {}'.format(len(tokens)))
	return len(clean_tokens(tokens))

def find_pos_locations(tokens, pos_tag = POS_TAG_TO_FIND):
	"""This function calculates the location(s) of any POS in one tokenized sentence."""
	locations = []
	words = clean_tokens(tokens)
	sentence_length = len(words)
	# ignore the sentence if it's too short;
	# return an empty list, which extend() will ignore.
	if sentence_length < APPROVED_SENTENCE_LENGTH:
		# print("Sentence length: {}; skipping.".format(sentence_length))
		return []
	for word_num, token in enumerate(words):
		try:
			word, pos = token.split('_')
		except:
			print(word_num, token, file)
			exit()				# somebody is barfing in PL
		if pos.startswith(pos_tag):
			# count the token; want count of infinitives now
			pos_counter.update([pos])

			# remove infinitive verbs, e.g.; they end with "I"
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



##############################################################
#
#	PROCESS THE FILES IN path VARIABLE
#
##############################################################


#	1. Corpus aggregate variables:
#		if the corpus is only one doc, these are the same,
#		obviously, as the document variables calculated below.

corpus_word_count = 0
all_sentences = []
location_percentages = []

total_periodic_sentences = 0
total_sentences = 0

#	2. Get list of corpus files

files = [f for f in os.listdir(path) if f.endswith('.txt')]
files.sort()


#	3. Process each file:

for file in files:
	if not file.endswith('.txt'):
		continue
	print("Working on {}".format(file))

	# remove later because we're resetting per book
	sentences = []

	with open(path + file) as f:
		lines = f.readlines()
	clean_lines = [line for line in lines if not BLANK.match(line) and not COMMENT.match(line)]
	text = ' '.join(clean_lines)

	# calculate all our variables
	document_tokens = tokenize(text)
	sentences = parse_sentences(document_tokens)		# this is a list of token lists
	all_sentences.extend(sentences)						# every sentence in the corpus
	document_word_count = word_count(document_tokens)	# this document word count
	if document_word_count == 0:
		print("Have zero length word count")
		print(file)
		exit()
	corpus_word_count += document_word_count			# word count in the corpus

	if STATUS_REPORT:
		print('______________')
		print('File: {}; Sentences: {}; Word Count: {}'.format(file, len(sentences), document_word_count))
		print('Aggregate Corpus Stats: Sentences: {}; Words: {}'.format(len(all_sentences), corpus_word_count))

	# We need to loop the sentences out here:
	# for sentence in sentences:
	# 	location_percentages.extend(find_pos_locations(sentence, pos_tag = 'V'))
	sentence_count = 0
	for sentence in sentences:
		locations = find_pos_locations(sentence, pos_tag = 'V')
		for loc in locations:
			if loc > MINIMUM_WINDOW:
				sentence_count += 1
				total_periodic_sentences += 1
				break

	print("Number of sentences: {}".format(len(sentences)))
	print("Number of periodic sentences: {}".format(sentence_count))
	print("Percentage: {}".format( sentence_count * 100 / len(sentences) ))

print("Total periodic sentences: {}".format(total_periodic_sentences))
print("Total sentences: {}".format(len(all_sentences)))
periodic_avg = total_periodic_sentences * 100 / len(all_sentences)
print("Percentage of periodic sentences: {}".format(periodic_avg))

# 4. Calculate binned and normalized histogram values
histogram = make_histogram(location_percentages)

#5. OUTPUT

print("Totals:")
print("Corpus Word Count: {}".format(corpus_word_count))
print()
print()
print(pos_counter)
print(','.join(HEADER))
for index, val in enumerate(histogram):
	print("{},{},{}".format( ((index + 1) * BIN_SIZE), val, TEXT))



