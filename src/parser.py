import os
import re
import utils
import timeit
import logging
import argparse
from bs4 import BeautifulSoup as bs


class Parser(object):
    """Parses html documents and generates a cleaned file after
    1. Stemming
    2. Case folding
    3. Stopping
    """
    def __init__(self, args):
        self.log = utils.get_logger("ParserLog")
        self.log.info(args)

        if args.debug:
            self.log.setLevel(logging.DEBUG)

    def parse(self):
        """Wrapper to parse html files to text files
        """
        self.log.info("Cleaning corpus")
        files = os.listdir(utils.CACM_DIR)
        files = list(map(lambda x: os.path.join(utils.CACM_DIR, x), files))

        for file in files:
            self._parse(file)

    def _parse(self, fpath):
        """Parses the HTML document at input file path into a simple text file
        with content

        Arguments:
            fpath (String) - File Path
        """
        file_name, ext = os.path.basename(fpath).split(".")
        corpus_file_path = os.path.join(utils.CORPUS_DIR, "{}.txt".format(file_name))

        if ext == "html":
            self.log.debug(file_name)
            
            with open(fpath, 'r') as fp:
                soup = bs(fp.read(), "html.parser")
                content = soup.find('pre').get_text()
                content = self.clean(content)

                # concat all terms with a single space character
                content = " ".join(content.split())

                with open(corpus_file_path, 'w') as fwp:
                    fwp.write(content)

    def clean(self, content):
        """Removes special character from the content

        Arguments:
            content (String)
        """
        
        # keeping '
        content = re.sub("[',\"^(){};/<>*!@#$%.+=|-?~:]+", " ", content)
        if args.casefolding:
            content = content.lower()
        return content


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
    
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument('-case', '--casefolding', action='store_true')
    parser.add_argument('-stem', '--stemming', action='store_true')
    parser.add_argument('-stop', '--stopping', action='store_true')
    parser.add_argument('-stopf', '--stopwordsfile', default="", type=str)

    args = parser.parse_args()
    obj = Parser(args)
    obj.parse()