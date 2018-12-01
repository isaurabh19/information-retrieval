from collections import defaultdict
from threading import Thread
from math import log
import re
import os
import utils
import logging
import json
import argparse

class JelinekMercer(object):
    def __init__(self, args, queries):
        self.log = utils.get_logger("JM-Smoothing")
        self.queries = queries
        self.inverted_index = None
        self.corpus_stats = None
        self.jm_scores = defaultdict(list)

        if args.debug:
            self.log.setLevel(logging.DEBUG)

    def read(self, file_name, corpus_file_name):
        with open(os.path.join(utils.INDEX_DIR, file_name)) as fp:
            self.inverted_index = json.loads(fp.read())

        self.log.debug(self.inverted_index.keys())

        with open(os.path.join(utils.INDEX_DIR, corpus_file_name)) as fp:
            self.corpus_stats = json.loads(fp.read())

    def computer_scores(self):
        C = self.compute_corpus_size()
        L = 0.35

        queries = map(self.refine_query, self.queries)
        
        for query in queries:
            self._compute_scores(query, C, L)

    def _compute_scores(self, query, C, L):
        self.log.info("Computing score for::\n {}".format(query))
        terms = query.split()
        iidx = self.get_inverted_indices(terms)
        
        for docid, stats in self.corpus_stats.items():
            D = stats["word_count"]
            query_doc_score = 0

            for term in terms:
                fqid = self.get_term_doc_freq(iidx[term], term, docid)
                cqi = self.get_term_count(iidx[term], term)
                
                A = ((1-L)*(fqid/D))
                B = (L*(cqi/C))

                try:
                    query_doc_score += log(A+B)
                except ValueError:
                    pass
                    # self.log.warning("Zero val for query term {}".format(term))
            self.jm_scores[query].append((docid, query_doc_score))
        self.log.info(max(self.jm_scores[query], key=lambda x: x[1]))


    def refine_query(self, query):
        query = re.sub("[,'\-\"^(){};/<>*!@#$%.+=|?~:]+", " ", query)
        query = ' '.join([w.lower() for w in query.split()])
        return query

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
                iidx[word] = self.inverted_index[word]
            except KeyError:
                pass
                # self.log.warning("Missing key in index: {}".format(word))
        return iidx
        
    def write(self, file_name, data):
        self.log.info("Writing: {}".format(file_name))
        file_path = os.path.join(utils.RESULTS_DIR, file_name)
        with open(file_path, 'w') as fp:
            fp.write(json.dumps(data, indent=1))


def get_queries(queries_path):
    with open(queries_path, 'r') as fp:
        return fp.read().split('\n')

def main(args):

    queries = None
    if args.isquerystemmed:
        queries = get_queries(utils.STEM_QUERIES)
    else:
        queries = get_queries(utils.PARSED_QUERIES)

    # queries = ['What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?']
    obj = JelinekMercer(args, queries)
    obj.log.debug(queries)
    obj.read(args.invertedindex, args.corpusstats)
    obj.computer_scores()

    file_name = "stem_{}_jm_score.txt".format(args.isquerystemmed)
    obj.write(file_name, obj.jm_scores)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser for JM Smoothing")
    parser.add_argument("-stem", "--isquerystemmed", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-ifile", "--invertedindex", type=str)
    parser.add_argument("-cfile", "--corpusstats", type=str)
    args = parser.parse_args()
    print(args)
    main(args)