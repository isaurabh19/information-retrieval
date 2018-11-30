from collections import defaultdict
from math import log
import json
import sys
import os

MU = 1500
BASEDIR = os.getcwd()

class DirichletScore(object):
    def __init__(self, queries):
        self.iidx_dir = os.path.join(BASEDIR, 'resources', 'unigrams.txt')
        self.corpus_dir = os.path.join(BASEDIR, 'resources', 'corpus')
        self.doc_length = defaultdict(int)
        self.query_scores = defaultdict(list)
        self.inverted_index = None
        self.queries = queries
    
    def read_iidx(self):
        """read invereted index into a dictionary
        """
        with open(self.iidx_dir, 'r') as fp:
            self.inverted_index = json.loads(fp.read())

    def precompute_doclength(self):
        """Populate the doc_id vs total lenth dictionary
        """
        files = os.listdir(self.corpus_dir)
        os.chdir(self.corpus_dir)
        for each_file in files:
            with open(each_file, 'r') as fp:
                file_name = os.path.basename(each_file).split(".")[0]
                self.doc_length[file_name] = len(fp.read().split())

    def get_term_count(self, inverted_list, term):
        result = 0
        for x in inverted_list:
            result += x[1]
        return result

    def get_term_doc_freq(self, inverted_list, term, doc):
        for x in inverted_list:
            if x[0] == doc:
                return x[1]
        return 0

    def computer_scores(self):
        """Computer scores for all queries
        """
        for query in self.queries:
            self._computer_scores(query)

    def _computer_scores(self, query=""):
        """Compute Dirichlet scores for a given query for all documents in the
        corpus
        """
        terms = query.split()
        iidx = self.get_inverted_indices(terms)
        scores = []

        C = sum(self.doc_length.values())
        for doc, D in self.doc_length.items():
            score = 0
            for term in terms:
                fqid = self.get_term_doc_freq(iidx[term], term, doc)
                cqi = self.get_term_count(iidx[term], term)
                # FORMULA
                score += log((fqid + MU*(cqi/C))/(D+MU))

            scores.append((doc, score))
        self.query_scores[query] = scores

    def get_inverted_indices(self, query):
        """Given a query, returns a dictionary with inverted index for each term
        in the query
        """
        iidx = defaultdict(list)
        for word in query:
            iidx[word] = self.inverted_index[word]['List']
        return iidx

    def sort(self):
        for query, ls in self.query_scores.items():
            self.query_scores[query] = sorted(ls, key=lambda a: a[1], reverse=True)

    def result(self):
        sysname = "LM Dirichlet"
        os.chdir(os.path.join(BASEDIR, 'result', 'Dirichlet'))
        for query, ls in self.query_scores.items():
            with open('{}.txt'.format(query.replace(' ', '_')), 'w') as fp:
                # print("{}::  {}".format(query, ls[:100]))
                for rank in range(len(ls[:100])):
                    fp.write('{}\tQ0\t{: >60}\t{}\t{}\t{}\n'.format(self.queries.index((query))+1, ls[rank][0], rank+1, ls[rank][1], sysname))


if __name__ == "__main__":
    queries_file = sys.argv[1]
    queries = []
    with open(queries_file, 'r') as fp:
        for line in fp:
            queries.append(line.strip('\n'))
    dscore = DirichletScore(queries)
    dscore.read_iidx()
    dscore.precompute_doclength()
    dscore.computer_scores()
    dscore.sort()
    # dscore.result()