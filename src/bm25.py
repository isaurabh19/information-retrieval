# -*- coding: utf-8 -*-
from collections import defaultdict
import utils
import logging
import argparse
import math
import os


class BM25(object):
	def __init__(self, args, index, stats, queries):
		self.log = utils.get_logger("BM25")
		self.inverted_index = index
		self.stopped_words = utils.read_stopped_words()
		self.corpus_stats = stats
		self.queries = queries
		self.bm25_scores = defaultdict(list)
		self.isstopped = args.isstopped

		if args.debug:
			self.log.setLevel(logging.DEBUG)

	def _compute_term_score(self, term, docid, avdl, qfi):
		try:
			iidx = self.inverted_index[term]
			ni = len(iidx)
			fi = 0
			for x in iidx:
				if x[0] == docid:
					fi = x[1]
		except KeyError:
			ni = 0
			fi = 0

		N = utils.N
		k1 = 1.2
		k2 = 100
		b = 0.75
		R = 0.0
		r = 0.0
		dl = self.corpus_stats[docid]["word_count"]
		K = k1*((1-b) + (b*(dl/avdl)))

		A = ((r + 0.5)/(R - r + 0.5))/((ni - r + 0.5)/(N - ni - R + r + 0.5))
		logA = math.log(A)
		B = ((k1 + 1)*fi)/(K + fi)
		C = ((k2 + 1)*qfi)/(k2 + qfi)

		score = logA*B*C
		return score

	def _compute_score(self, docids, query, avdl):
		scores = []
		terms = query.split()

		for docid in docids:
			score = 0
			for term in terms:
				if self.isstopped and term in self.stopped_words:
					continue
				score += self._compute_term_score(term, docid, avdl, query.count(term))
			scores.append((docid, score))

		scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
		return scores

	def compute_scores(self):
		self.log.info("Computing BM25 scores")

		avdl = self.precompute_avdl()
		docids = self.corpus_stats.keys()
		for i in range(len(self.queries)):
			qid = "Q{}".format(i)
			self.log.info("Computing score for {}".format(qid))
			self.bm25_scores[qid] = self._compute_score(docids, self.queries[i], avdl)

	def precompute_avdl(self):
		corpus_size = 0
		for _, data in self.corpus_stats.items():
			corpus_size += data["word_count"]

		return corpus_size/len(self.corpus_stats)


def main(args):
	print(args)
	index_file = "stem_{}_stop_{}_inverted_index.txt".format(args.isstemmed, args.isstopped)
	queries = utils.load_queries(utils.PARSED_QUERIES)

	if args.isstemmed:
		queries = utils.load_queries(utils.STEM_QUERIES)

	index = utils.load_inverted_index(os.path.join(utils.INDEX_DIR, index_file))
	stats = utils.load_corpus_stats()

	obj = BM25(args, index, stats, queries[49:54])
	obj.compute_scores()

	file_name = "stem_{}_stop_{}_bm25_score.csv".format(args.isstemmed, args.isstopped)
	file_path = os.path.join(utils.RESULT_DIR, "bm25", file_name)
	utils.write(obj.log, file_path, obj.bm25_scores, csvf=True)
	file_name2 = "stem_{}_stop_{}_bm25_score.json".format(args.isstemmed, args.isstopped)
	file_path2 = os.path.join(utils.RESULT_DIR, "bm25", file_name2)
	utils.write(obj.log, file_path2, obj.bm25_scores)

if __name__ == '__main__':
	parser = argparse.ArgumentParser("BM25 ArgumentParser")
	
	parser.add_argument("-d", "--debug", action="store_true")
	parser.add_argument('-stem', "--isstemmed", action="store_true")
	parser.add_argument('-stop', "--isstopped", action="store_true")
	
	args = parser.parse_args()
	main(args)