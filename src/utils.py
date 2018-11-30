import os
import sys

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
