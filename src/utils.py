# -*- coding: utf-8 -*-
import os
import sys
import csv
import json
import logging

# value of N for TF-IDF
N = 3204

# value of B for JM-Smoothing
RETRIEVED_DOCS = 100

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULT_DIR = os.path.join(BASE_DIR, 'results')

INDEX_DIR = os.path.join(DATA_DIR, 'index')
CORPUS_DIR = os.path.join(DATA_DIR, 'corpus')
STEM_CORPUS_DIR = os.path.join(DATA_DIR, 'stem_corpus')

STEM_QUERIES = os.path.join(DATA_DIR, "cacm_stem.query.txt")
PARSED_QUERIES = os.path.join(DATA_DIR, "cacm.parsed.query.txt")

def check_dirs():
	if not os.path.exists(CACM_DIR):
			raise FileNotFoundError("RAW HTML documents not found")
	if not os.path.exists(CORPUS_DIR):
			print("Corpus is empty. Creating a new corpus directory")
			os.mkdir(CORPUS_DIR)
	if not os.path.exists(INDEX_DIR):
			os.mkdir(INDEX_DIR)

def get_logger(logger_name):
	# WARNING = '\033[93m'
	# ENDC = '\033[0m'
	log_format = logging.Formatter("\033[93m[%(name)s][%(levelname)s]\033[0m — %(message)s")
	logger = logging.getLogger(logger_name)
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(log_format)
	logger.setLevel(logging.INFO)
	logger.addHandler(console_handler)
	return logger

def write(logger, file_path, data, csvf=False):
	if logger:
		logger.info("Writing: {}".format(file_path))
	with open(file_path, 'w') as fp:
		if csvf:
			writer = csv.writer(fp)
			writer.writerow(["QueryID", "DocID", "Score"])
			for qid, val in data.items():
				for each_val in val:
					writer.writerow([qid, each_val[0], each_val[1]])
		else:
			fp.write(json.dumps(data, indent=2))

def load_queries(queries_path):
	with open(queries_path, 'r') as fp:
		return fp.read().split('\n')

def load_inverted_index(index_path):
	with open(index_path) as fp:
		return json.loads(fp.read())

def load_corpus_stats():
	doc_path = os.path.join(INDEX_DIR, "stem_False_stop_False_corpus_stats.txt")
	with open(doc_path, "r") as fp:
		return json.loads(fp.read())

def load_query_map():
	doc_path = os.path.join(DATA_DIR, "query.parsed.map.txt")
	with open(doc_path, "r") as fp:
		return json.loads(fp.read())