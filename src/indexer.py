from collections import defaultdict
import os
import json
import utils
import logging
import argparse


class Indexer(object):
	def __init__(self, corpus_path, args):
		self.corpus_name = corpus_path
		self.log = utils.get_logger("IndexerLog")
		self.inverted_index = defaultdict(list)
		self.positional_index = defaultdict(dict)
		self.corpus = defaultdict(str)

		if args.debug:
			self.log.setLevel(logging.DEBUG)

	def read(self):
		"""Read the corpus directory into memory
		"""
		files = os.listdir(self.corpus_name)
		files = list(map(lambda x: os.path.join(utils.CORPUS_DIR, x), files))

		for file in files:
			with open(file, 'r') as fp:
				content = fp.read()
				docid, _ = os.path.basename(file).split(".")
				self.corpus[docid] = content.split()

	def index(self):
		"""Wrapper to create inverted index
		"""
		self.log.info("Creating Inverted Index")
		for docid, content in self.corpus.items():
			self._index(docid, content)

		self.log.debug("{}".format(self.inverted_index.keys()))

	def _index(self, docid, content):
		"""Indexer
		
		Arguments:
			docid (String)
			content (String)
		"""
		self.log.debug("{}, Words: {}".format(docid, len(content)))
		
		vocab = set(content)
		term_freq = list(map(lambda x: content.count(x), vocab))

		for word, freq in zip(vocab, term_freq):
			self.inverted_index[word].append((docid, freq))

	def create_positional_index(self):
		"""Wrapper to create positional index
		"""
		self.log.info("Creating Positional Indexes")

		for docid, content in self.corpus.items():
			vocab = set(content)
			words = content
			self._create_positional_index(docid, vocab, words)

	def _create_positional_index(self, docid, vocab, words):
		# word_indexes = range(len(words))
		for w in vocab:
			j = 0
			pos_index = []
			start_index = words.index(w)
			for i in range(start_index, len(words)):
				if words[i] == w:
					if j == 0:
						pos_index.append(i)
					else:
						pos_index.append(i-pos_index[j-1])
					j += 1

			if len(pos_index) > 0:
				self.positional_index[w][docid] = pos_index

	def write(self, file_name, data):
		self.log.info("Writing: {}".format(file_name))
		file_path = os.path.join(utils.INDEX_DIR, file_name)
		with open(file_path, 'w') as fp:
			fp.write(json.dumps(data, indent=1))

def main(args):
	obj = None

	# if args.corpus != "":
	# 	obj = Indexer(str(args.corpus), args)
	# else:
	obj = Indexer(utils.CORPUS_DIR, args)
	obj.read()
	
	# create inverted indexes
	obj.index()
	file_name = "{}_inverted_index.txt".format(os.path.basename(obj.corpus_name).split(".")[0])
	obj.write(file_name, obj.inverted_index)
	
	# create positional indexes
	file_name = "{}_positional_index.txt".format(os.path.basename(obj.corpus_name).split(".")[0])
	obj.create_positional_index()
	obj.write(file_name, obj.positional_index)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="Parse arguments for Indexer")
	
	parser.add_argument('-d', '--debug', action="store_true")
	parser.add_argument('-corpus', '--corpus-directory', default="", type=str)

	main(parser.parse_args())