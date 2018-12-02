from bs4 import BeautifulSoup as bs
from collections import defaultdict
import utils
import os

def parse_cacm_queries():
    queries = []
    with open(utils.GEN_QUERIES, "r") as fp:
        soup = bs(fp.read(), 'html.parser')
        res = soup.find_all('doc')
        qmap = defaultdict(str)
        for x in res:
            s = x.text
            text = s.split()
            qid = text[0]
            queries.append(" ".join(text[1:]))

    print("No of queries {}".format(len(queries)))
    with open(os.path.join(utils.BASE_DIR, "data", "cacm.parsed.query.txt"), "w") as fp:
        fp.write('\n'.join(queries))



parse_cacm_queries()