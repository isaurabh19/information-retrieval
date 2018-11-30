import argparse
import os

BASE_DIR = os.path.dirname(os.getcwd())


CACM_DIR = os.path.join(BASE_DIR, 'data', 'cacm')
CORPUS_DIR = os.path.join(BASE_DIR, 'data', 'corpus')
RESULT_DIR = os.path.join(BASE_DIR, 'result')
SEP = "_$_"

def check_dirs():
    if not os.path.exists(CORPUS_DIR):
        print("CACM Corpus not found!! Exiting.. Crawl again")
        exit(1)
    if not os.path.exists(CORPUS_DIR):
        os.mkdir(CORPUS_DIR)
    if not os.path.exists(RESULT_DIR):
        os.mkdir(RESULT_DIR)