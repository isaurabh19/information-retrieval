from parser import Parser
from indexer import Indexer
import utils
import sys
import os
import re

wiki_files = os.listdir(utils.CACM_DIR)

def main(c=0, p=1):
    count = 0

    for fname in wiki_files:
        file_path = os.path.join(utils.CACM_DIR, fname)
        with open(file_path, 'r') as frp:
            _, src = frp.read().split(utils.SEP)
            fcontent = Parser(src, c, p).filter_page_source()

            title = fcontent['title'].replace(" ", "_")
            title = title.replace("/","_")
            file_write_path = os.path.join(utils.CORPUS_DIR, title)
            with open("{}.txt".format(file_write_path), "w") as fwp:
                fwp.write(fcontent['content'])
                count += 1 
                print(title, count)

if __name__ == '__main__':
    utils.check_dirs()
    # utils.load_args()
    main(int(sys.argv[1]), int(sys.argv[2]))
    
    # cleanup cache
    re.purge()
    exit(0)