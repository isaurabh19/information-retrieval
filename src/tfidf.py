# -*- coding: utf-8 -*-
from collections import defaultdict
import utils
import logging
import argparse
import math
import os


class TFiDF(object):
	def __init__(self, args, index, stats, queries):
		self.log = utils.get_logger("TF-IDF")
		self.corpus_stats = stats
		self.stopped_words = utils.read_stopped_words()
		self.queries = queries
		self.inverted_index = index
		self.tfidf_scores = defaultdict(list)
		self.isstopped = args.isstopped

		if args.debug:
			self.log.setLevel(logging.DEBUG)

	def calc_tf_idf(self, query, docid):
		query_score = 0
		query = query.split()
		for word in query:
			if self.isstopped and word in self.stopped_words:
				continue
			try:
				iidx_word = self.inverted_index[word]
				tf = 0
				for x in iidx_word:
					if x[0] == docid:
						tf = x[1]
				idf = math.log(utils.N/len(iidx_word))
				query_score += (tf*idf)
			except KeyError:
				pass

		return (docid, query_score)

	def compute_scores(self):
		self.log.info("Computing TFiDF scores")
		docids = self.corpus_stats.keys()
		for i in range(len(self.queries)):
			qid = "Q{}".format(i)
			self.log.info("Computing score for {}".format(qid))
			self.tfidf_scores[qid] = self._compute_score(docids, self.queries[i])

	def _compute_score(self, docids, query):
		query_scores = map(lambda docid: self.calc_tf_idf(query, docid), docids)
		query_scores = sorted(query_scores, key=lambda x: x[1], reverse=True)[:5]
		return query_scores


def main(args):
	print(args)
	index_file = "stem_{}_stop_{}_inverted_index.txt".format(args.isstemmed, args.isstopped)
	queries = utils.load_queries(utils.PARSED_QUERIES)
	
	if args.isstemmed:
		queries = utils.load_queries(utils.STEM_QUERIES)

	index = utils.load_inverted_index(os.path.join(utils.INDEX_DIR, index_file))
	stats = utils.load_corpus_stats()

	obj = TFiDF(args, index, stats, queries[49:54])
	obj.compute_scores()

	file_name = "stem_{}_stop_{}_tfidf_score.csv".format(args.isstemmed, args.isstopped)
	file_name2 = "stem_{}_stop_{}_tfidf_score.json".format(args.isstemmed, args.isstopped)
	file_path = os.path.join(utils.RESULT_DIR, "tfidf", file_name)
	file_path2 = os.path.join(utils.RESULT_DIR, "tfidf", file_name2)
	utils.write(obj.log, file_path, obj.tfidf_scores, csvf=True)
	utils.write(obj.log, file_path2, obj.tfidf_scores)

if __name__ == '__main__':
	parser = argparse.ArgumentParser("TF-IDF ArgumentParser")
	
	parser.add_argument("-d", "--debug", action="store_true")
	parser.add_argument('-stem', "--isstemmed", action="store_true")
	parser.add_argument('-stop', "--isstopped", action="store_true")
	
	args = parser.parse_args()
	main(args)