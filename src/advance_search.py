from collections import defaultdict
import utils
import logging
import argparse
import math
import os

class AdvanceSearch(object):
	def __init__(self, args):
		self.log = utils.get_logger("AdvanceSearch")
		self.query = args.query
		self.args = args

	def load_inverted_index(self, file_path):
		with open(file_path, "r") as fp:
			self.inverted_index = json.loads(fp.read())

	def load_positional_index(self, file_path):
		with open(file_path, "r") as fp:
			self.positional_index = json.loads(fp.read())

	def preprocess_pos_index(self):
		for qid, data in self.positional_index.items():
			for docid, ls in data.items():
				for i in range(1, len(ls)):
					ls[i] = ls[i]+ls[i-1]

	def get_term_indexes(self, terms, data):
		res = defaultdict(load_positional_index)
		for term in terms:
			res[term] = self.data[term]
		return res

	def get_docs(self, index):
		return set([x[0] for x in index])

	def get_common_docs(self, terms, term_indexes):
		A = self.get_docs(term_indexes[terms[0]])
		for term in terms[1:]:
			B = self.get_docs(term_indexes[term])
			A = A.intersection(B)
		return A

	def get_term_postions_in_doc(self, docid, terms, term_positions):
		res = defaultdict(list)
		for term in terms:
			res[term] = term_positions[term][docid]
		return res

	def get_exact_docs(self, common_docs, terms, term_positions):
		for docid in common_docs:
			positions = self.get_term_postions_in_doc(docid, terms, term_positions)
			# for pos in positions[terms[0]]:
			# 	for i in range(1, len(terms)):
			# 		if positions[terms[i]]

	def exact_search(self):
		terms = self.query.split()
		term_indexes = self.get_term_indexes(terms, self.inverted_index)
		term_positions = self.get_term_indexes(terms, self.positional_index)
		common_docs = self.get_common_docs(terms, term_indexes)
		if len(common_docs) > 0:
			res = self.get_exact_docs(common_docs, terms, term_positions)
			self.log.info("{}".format(res))


def main(args):
	print(args)

	obj = AdvanceSearch(args)

if __name__ == '__main__':
	parser = argparse.ArgumentParser("TF-IDF ArgumentParser")
	

	parser.add_argument("-d", "--debug", action="store_true")
	parser.add_argument('-e', "--exactmatch", action="store_true")
	parser.add_argument('-b', "--bestmatch", action="store_true")
	parser.add_argument('-n', "--proximitymatch", deafult="", type=int)
	parser.add_argument('-q', "--query", deafult="", type=str)

	args = parser.parse_args()
	main(args)