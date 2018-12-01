import os
import sys
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CACM_DIR = os.path.join(BASE_DIR, 'data', 'cacm')
INDEX_DIR = os.path.join(BASE_DIR, 'data', 'index')
RESULT_DIR = os.path.join(BASE_DIR, 'results')

CORPUS_DIR = os.path.join(BASE_DIR, 'data', 'corpus')
STEM_CORPUS_DIR = os.path.join(BASE_DIR, 'data', 'stem_corpus')

GEN_QUERIES = os.path.join(BASE_DIR, "data", "cacm.query.txt")
STEM_QUERIES = os.path.join(BASE_DIR, "data", "cacm_stem.query.txt")

PARSED_QUERIES = os.path.join(BASE_DIR, "data", "cacm.parsed.query.txt")

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

def write(logger, file_path, data):
    logger.info("Writing: {}".format(file_path))
    with open(file_path, 'w') as fp:
        fp.write(json.dumps(data, indent=1))