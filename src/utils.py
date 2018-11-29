import argparse
import os

BASE_DIR = os.path.dirname(os.getcwd())


CACM_DIR = os.path.join(BASE_DIR, 'data', 'cacm')
CORPUS_DIR = os.path.join(BASE_DIR, 'data', 'corpus')
RESULT_DIR = os.path.join(BASE_DIR, 'result')
SEP = "_$_"
args = None

def check_dirs():
    if not os.path.exists(CACM_DIR):
        print("Wiki directory not found!! Exiting.. Crawl again")
        exit(1)
    if not os.path.exists(CORPUS_DIR):
        os.mkdir(CORPUS_DIR)
    if not os.path.exists(RESULT_DIR):
        os.mkdir(RESULT_DIR)

def load_args():
    '''Parse the arguments with argparse utility
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    global args
    args = parser.parse_args()

def log(*arguments):
    '''Logger in debugging mode
    if option '-d' or '--debug' is given
    import debugging outputs will be printed
    '''
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    if args.debug:
        print("{}[dbg]{} {}".format(WARNING, ENDC, arguments))