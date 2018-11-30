import os
import utils
import logging
import argparse
from bs4 import BeautifulSoup as bs


class Parser(object):
    """Parses html documents and generates a cleaned file after
    1. Stemming
    2. Case folding
    3. Stopping
    """
    def parse(self):
        print(utils.CACM_DIR)
        files = os.listdir(utils.CACM_DIR)
        files = list(map(lambda x: os.path.join(utils.CACM_DIR, x), files))

        for file in files:
            self._parse(file)

    def _parse(self, fpath):
        with open(fpath, 'r') as fp:
            soup = bs(fp.read(), "html.parser")
            content = soup.find('pre').get_text()
            print(len(content))

def check_args(args):
    """Check if arguments are valid
    
    Arguments:
        args (Namespace)
    
    Returns:
        Boolean
    """
    if args.stopping and (args.stopwordsfile == ""):
        print("If using stopwords add file containing stopwords")
        return False
    return True

if __name__ == "__main__":
    utils.check_dirs()
    parser = argparse.ArgumentParser(
        description="Parse arguments for parser")
    
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-case', '--casefolding', action='store_true')
    parser.add_argument('-stem', '--stemming', action='store_true')
    parser.add_argument('-stop', '--stopping', action='store_true')
    parser.add_argument('-stopf', '--stopwordsfile', default="", type=str)

    args = parser.parse_args()
    print(args)

    obj = Parser()
    obj.parse()