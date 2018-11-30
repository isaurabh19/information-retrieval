import collections
import utils
import json
import os
import re


IGNORE = set(["", "'", "&"])

class Indexer(object):
    """Parent Class to tokenize corpus data into tokens and generate inverted
    indexes
    """
    def __init__(self):
        self.inverted_index = collections.defaultdict(list)
        self.final_iidx = collections.defaultdict(list)
        self.doc_words = collections.defaultdict(int)
        self.term_freq = collections.defaultdict(int)
        self.pos_index = collections.defaultdict(list)
        self.doc_freq = None

    def read(self, count):
        files = os.listdir(utils.CORPUS_DIR)
        for fname in files:
            with open(os.path.join(utils.CORPUS_DIR, fname), 'rb') as frp:
                docID = os.path.basename(frp.name).split(".")[0]
                text = frp.read().decode('utf-8')
                if text[:2] == "b\'":
                    text = text[2:]
                words = self.clean_words(text.split(" "))
                self.tokenize(count, docID, words, text)

    def tokenize(self, count, docID, words, content):
        if count == 1:
            self.count_term_freq(docID, words)
        
        words_set = set()
        
        # [2-1]
        if count == 1:
            words_set = set(words)
        else:
            for i in range(len(words)-count):
                wrd = words[i]
                if count != 1 and wrd not in IGNORE:
                    words_set.add(' '.join(words[i:i+count]))

        for wrd in words_set:
            term_freq = content.count(wrd)
            self.inverted_index[wrd].append((docID, term_freq))
            
            # [4-1]
            self.term_freq[wrd] += term_freq
            
        # [2-3] number of terms in each document
        self.doc_words[docID] = len(set(content))

    def clean_words(self, words):
        return [x for x in words if x not in IGNORE]

    # [2-4] Positional Index
    def count_term_freq(self, docID, words):
        """Count word occurrences and encode them using d-gaps for the given document
        """
        utils.log("Pos: ", docID, len(words))
        pos_index = []

        for w in set(words):
            pos_index = []
            for i in range(len(words)):
                if w == words[i]:
                    pos_index.append(i)

            for i in range(1, len(pos_index)):
                pos_index[i] = pos_index[i] - pos_index[i-1]
            self.pos_index[w].append({"docID": docID, "index": pos_index})

    def stats(self):
        """
        1- For each inverted index in Task 2a, generate a term frequency table comprising of two columns: 
            term and term frequency (for the corpus).
            Sort the table from most to least frequent.
        2- For each inverted index in Task 2a, generate a document frequency table comprising of three columns: 
            term, docIDs, and document frequency. Sort lexicographically based on term.
            Note: For tasks 3-1 and 3-2, you will generate six tables in total: two tables for word unigrams, 
            two tables for word bigrams, and two tables for word trigrams.
        """        
        # [2-2]
        for key, val in self.inverted_index.items():
            self.final_iidx[key] = {
                "Len": len(val),
                "List": val
            }

        # [4-2] TERM vs DOCID vs TERMFREQ
        doc_freq = collections.defaultdict(dict)
        for term, iidx in self.inverted_index.items():
            doc_term_count = collections.defaultdict(int)
            for each_doc in iidx:
                doc_term_count[each_doc[0]] = each_doc[1]
            
            doc_freq[term] = doc_term_count
        self.doc_freq = doc_freq

    def _write(self, count):

        # [2-1 and 2-2]
        file_path = os.path.join(utils.RESULT_DIR, "Inverted_Index_{}.txt".format(count))
        with open(file_path, 'w') as fp:
            fp.write(json.dumps(self.final_iidx, indent=1, sort_keys=True))

        # # [2-3]
        file_path = os.path.join(utils.RESULT_DIR, "Doc_Term_Count.txt")
        with open(file_path, 'w') as fp:
            fp.write(json.dumps(self.doc_words, indent=1, sort_keys=True))

        # [4-1] TERM vs TERMFREQ
        import operator
        file_path = os.path.join(utils.RESULT_DIR, "Term_Freq_{}.txt".format(count))
        with open(file_path, 'w') as fp:
            fp.write("TERM\t\t\tTERM FREQUENCY\n")
            sorted_termfreq = sorted(self.term_freq.items(), key=operator.itemgetter(1), reverse=True)
            for key in sorted_termfreq:
                fp.write("\"{}\"\t\t\t{}\n".format(key[0], key[1]))

        # [4-2] TERM vs DOCID vs TERMFREQ
        file_path = os.path.join(utils.RESULT_DIR, "Doc_Freq_{}.txt".format(count))
        temp = dict(sorted(self.doc_freq.items()))
        with open(file_path, 'w') as fp:
            fp.write("TERM\t\t\tDOC ID\t\tTERM FREQUENCY\n")
            for term, lst in temp.items():
                for docid, count in lst.items():
                    fp.write("\"{}\"\t\t\t\"{}\"\t\t{}\n".format(term, docid, count))


        # [2-4] POS Index
        if count == 1:
            file_path = os.path.join(utils.RESULT_DIR, "Pos_Index_{}.txt".format(count))
            with open(file_path, 'w') as fp:
                fp.write(json.dumps(self.pos_index))

def main():
    for i in range(1, 4):
        idx = Indexer()
        idx.read(count=i)
        idx.stats()
        idx._write(i)

if __name__ == '__main__':
    utils.load_args()
    main()