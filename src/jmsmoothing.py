# -*- coding: utf-8 -*-
from collections import defaultdict
import utils
import logging
import argparse
import math
import os


class JelinekMercer(object):
	def __init__(self, args, index, stats, queries):
		self.log = utils.get_logger("JM-Smoothing")
		self.queries = queries
		self.stopped_words = utils.read_stopped_words()
		self.inverted_index = index
		self.corpus_stats = stats
		self.jm_scores = defaultdict(list)
		self.isstopped = args.isstopped

		if args.debug:
			self.log.setLevel(logging.DEBUG)

	def compute_scores(self):
		C = self.compute_corpus_size()
		L = 0.35

		# already doing it in cacm_query_parser
		# model should not be doing that, it is a part of user interface
		# queries = map(self.refine_query, self.queries)
		id = 0
		for query in self.queries:
			self._compute_scores(id, query, C, L)
			id += 1

		self.sort()

	def _compute_scores(self, id, query, C, L):
		self.log.info("Q{}: {}".format(id, query))
		terms = query.split()
		iidx = self.get_inverted_indices(terms)
		
		for docid, stats in self.corpus_stats.items():
			D = stats["word_count"]
			query_doc_score = 0

			for term in terms:
				if self.isstopped and term in self.stopped_words:
					continue
				fqid = self.get_term_doc_freq(iidx[term], term, docid)
				cqi = self.get_term_count(iidx[term], term)
				
				A = ((1-L)*(fqid/D))
				B = (L*(cqi/C))

				try:
					query_doc_score += math.log(A+B)
				except ValueError:
					pass
					# self.log.warning("Zero val for query term {}".format(term))

			qid = "Q{}".format(id)
			self.jm_scores[qid].append((docid, query_doc_score))
		
		self.log.info("TOP Scorer: {}".format(max(self.jm_scores[qid], key=lambda x: x[1])))

	def get_term_doc_freq(self, inverted_list, term, docid):
		for x in inverted_list:
			if x[0] == docid:
				return x[1]
		return 0

	def get_term_count(self, inverted_list, term):
		result = 0
		for x in inverted_list:
			result += x[1]
		return result

	def compute_corpus_size(self):
		corpus_size = 0
		for _, stats in self.corpus_stats.items():
			corpus_size += stats["word_count"]
		return corpus_size

	def get_inverted_indices(self, terms):
		"""Given a list of casefolded query term, returns a dictionary with inverted index for each term
		in the query
		"""
		iidx = defaultdict(list)
		for word in terms:
			try:
				# import pdb; pdb.set_trace()
				iidx[word] = self.inverted_index[word]
			except KeyError:
				pass
				# self.log.warning("Missing key in index: {}".format(word))
		return iidx

	def sort(self):
		for query, ls in self.jm_scores.items():
			self.jm_scores[query] = sorted(ls, key=lambda a: a[1], reverse=True)[:5]


def main(args):
	print(args)
	queries = None
	index_file = "stem_{}_stop_{}_inverted_index.txt".format(args.isstemmed, args.isstopped)
	queries = utils.load_queries(utils.PARSED_QUERIES)
	
	if args.isstemmed:
		queries = utils.load_queries(utils.STEM_QUERIES)

	index = utils.load_inverted_index(os.path.join(utils.INDEX_DIR, index_file))
	stats = utils.load_corpus_stats()

	obj = JelinekMercer(args, index, stats, queries[49:54])
	obj.compute_scores()

	file_name = "stem_{}_stop_{}_jm_score.csv".format(args.isstemmed, args.isstopped)
	file_path = os.path.join(utils.RESULT_DIR, "jm", file_name)
	utils.write(obj.log, file_path, obj.jm_scores, csvf=True)
	
	file_name2 = "stem_{}_stop_{}_jm_score.json".format(args.isstemmed, args.isstopped)
	file_path2 = os.path.join(utils.RESULT_DIR, "jm", file_name2)
	utils.write(obj.log, file_path2, obj.jm_scores)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parser for JM Smoothing")
	
	parser.add_argument("-d", "--debug", action="store_true")
	parser.add_argument("-stem", "--isstemmed", action="store_true")
	parser.add_argument("-stop", "--isstopped", action="store_true")

	args = parser.parse_args()
	main(args)