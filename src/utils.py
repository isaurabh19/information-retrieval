import os
import sys
import logging

BASE_DIR = os.path.dirname(os.getcwd())
CACM_DIR = os.path.join(BASE_DIR, 'data', 'cacm')
CORPUS_DIR = os.path.join(BASE_DIR, 'data', 'corpus')
INDEX_DIR = os.path.join(BASE_DIR, 'data', 'index')

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

