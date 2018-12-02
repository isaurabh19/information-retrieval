from collections import defaultdict
from matplotlib import pyplot as plt
import argparse
import logging
import utils
import json
import os


class Query(object):
	def __init__(self, qid, retrieved_docs, B):
		self.qid = qid
		self.retrieved_docs = retrieved_docs
		self.rel_docs = None
		self.precision_values = []
		self.recall_values = []
		self.A = None
		self.B = B
		self.p5 = None
		self.p20 = None
		self.precision = None
		self.recall = None


class Evaluation(object):
	def __init__(self, args, rel_docs):
		self.log = utils.get_logger("Evaluation")
		self.model = args.model
		self.ranks_file_name = args.file
		self.rel_docs = rel_docs
		self.queries = defaultdict(Query)

		if args.debug:
			self.log.setLevel(logging.DEBUG)

	def filter_queries(self):
		self.log.info("Filtering non relevant queries")
		query_ids = set(self.rel_docs.keys())
		all_query_ids = set(self.queries.keys())

		remove_qids = all_query_ids - query_ids
		for qid in remove_qids:
			del self.queries[qid]

	def populate_query_data(self):
		self.log.info("Populating Query Data")
		query_ids = set(self.rel_docs.keys())
		for qid in query_ids:
			qobj = self.queries[qid]
			qobj.rel_docs = self.rel_docs[qid]
			qobj.A = len(self.rel_docs[qid])
			self.calc_precision_recall(qobj)

	def create_queries(self):
		with open(os.path.join(utils.RESULT_DIR, self.ranks_file_name), "r") as fp:
			content = json.loads(fp.read())
			for qid, vals in content.items():
				docs = [x[0] for x in vals]
				self.queries[qid] = Query(qid, docs, len(docs))

	def calc_map_mrr(self):
		"""Calculate MAP and MRR values
		"""
		self.log.info("Calculate MAP and MRR")
		def calc_ap_rr(qobj):
			"""Calculate AP and RR values given a query object

			Returns:
				(float, float) - (AP, RR)
			"""
			retrieved_docs = qobj.retrieved_docs
			precision_values = qobj.precision_values
			rel_docs = qobj.rel_docs

			rr = 0
			rr_flag = True
			pre_vals = []
			for docid, p in zip(retrieved_docs, precision_values):
				if docid in rel_docs:
					if rr_flag:
						rr = float(1/p)
						rr_flag = False
					pre_vals.append(p)

			ap = sum(pre_vals)/len(pre_vals)

			self.log.debug("{}-AP={}".format(qobj.qid, ap))
			return ap, rr

		all_aps_rrs = list(map(calc_ap_rr, self.queries.values()))

		mrr_val = map_val = 0
		for val in all_aps_rrs:
			map_val += val[0]
			mrr_val += val[1]

		map_val /= len(all_aps_rrs)
		mrr_val /= len(all_aps_rrs)

		self.log.info("MAP={}, MRR={}".format(map_val, mrr_val))

		return map_val, mrr_val

	def calc_p_at_k(self):
		self.log.info("Populating P@K, Final Precision and Recall values")
		qids = self.queries.keys()
		for qid, qobj in self.queries.items():
			self.queries[qid].p5 = self.queries[qid].precision_values[4]
			self.queries[qid].p20 = self.queries[qid].precision_values[19]
			# self.queries[qid].precision = self.queries[qid].precision_values[-1:][0]
			# self.queries[qid].recall = self.queries[qid].recall_values[-1:][0]

	def calc_precision_recall(self, query):
		"""
		"""
		self.log.info("Calculate all Precision/Recall for {}".format(query.qid))
		rank = 0
		for i in range(query.B):
			if query.retrieved_docs[i] in query.rel_docs:
				rank += 1
			query.precision_values.append(rank/(i+1))
			query.recall_values.append(rank/query.A)

	def get_stats(self, map_val, mrr_val):
		def get_query_stats(qobj):
			packet = {
				"QID": qobj.qid,
				"P@5": qobj.p5,
				"P@20": qobj.p20,
				"Precision": qobj.precision_values,
				"Recall": qobj.recall_values
			}

			return packet

		qids = self.queries.keys()
		result = {
			"MAP": map_val,
			"MRR": mrr_val,
			"Stats": list(map(lambda qid: get_query_stats(self.queries[qid]), qids))
		}

		return result

	def gen_pr_graph(self):
		for _, qobj in self.queries.items():
			self._create_graph(qobj)

	def _create_graph(self, qobj):
		y = qobj.recall_values
		x = qobj.precision_values

		plt.xlabel("Precision")
		plt.ylabel("Recall")
		plt.plot(x, y)
		plt.title("PR Trend for {}".format(qobj.qid))
		img_path = os.path.join(utils.RESULT_DIR, "plots", "eval_{}_{}.png".format(self.model, qobj.qid))
		plt.savefig(img_path)
		plt.clf()

def load_rel_docs():
	with open(os.path.join(utils.BASE_DIR, "data", "cacm.parsed.rel.txt"), "r") as fp:
		content = json.loads(fp.read())
		return content

def main(args):
	print(args)
	rel_docs = load_rel_docs()
	obj = Evaluation(args, rel_docs)
	obj.create_queries()

	obj.log.debug("Initiated Queries = {}".format(len(obj.queries)))
	obj.filter_queries()
	obj.log.debug("Relevance Feedback Queries = {}".format(len(obj.queries)))
	obj.populate_query_data()

	map_val, mrr_val = obj.calc_map_mrr()
	obj.calc_p_at_k()

	# file_path = os.path.join(utils.RESULT_DIR, "eval_{}.txt".format(obj.model))
	# utils.write(obj.log, file_path, obj.get_stats(map_val, mrr_val))
	obj.gen_pr_graph()

if __name__ == '__main__':
	parser = argparse.ArgumentParser("Argument Parser for Evaluation")

	parser.add_argument("-d", "--debug", action="store_true")
	parser.add_argument("-m", "--model", default="jm", type=str)
	parser.add_argument("-f", "--file", default="stem_False_stop_False_jm_score.txt", type=str)

	args = parser.parse_args()
	main(args)