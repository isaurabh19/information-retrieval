from utils import PARSED_QUERIES, load_queries, INDEX_DIR, load_corpus_stats, DATA_DIR
import utils
from jm_smoothing import JelinekMercer
import os
import nltk
import logging
import pandas as pd
from itertools import imap
from operator import add, sub

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RELEVANT_DOC_COUNT = 15.
PCH = r"""!#$%&()*+/:;<=>?@[\]^_'"`{|}~,.-'"""
ALPHA = 1
BETA = 1
GAMMA = 0.5

list_queries = load_queries(PARSED_QUERIES)
args = {"debug": False, "isstemmed": False, "isstopped": False}
baseline_run = JelinekMercer(args, os.path.join(INDEX_DIR, "stem_False_stop_False_inverted_index.txt"),
                             load_corpus_stats(), list_queries)
# dict query_id: [[doc_name,score],[],[] ....]
results = baseline_run.jm_scores()


def get_content(doc_names):
    doc_contents = []
    for doc in doc_names:
        with open(os.path.join(utils.CORPUS_DIR, "{}.txt".format(doc)), "rb") as f:
            doc_contents.append(f.read())
    return doc_contents


def vocabularize(corpus_string):
    tokens = nltk.tokenize.word_tokenize(corpus_string)
    vocabulary = {}
    for token in tokens:
        if token in vocabulary:
            vocabulary[token] += 1
        else:
            vocabulary[token] = 1
    return vocabulary.keys()


def get_vocabulary(doc_content):
    # tokens = nltk.tokenize.word_tokenize(doc_content)
    # tokens = filter(remove_special_chars,tokens)
    corpus = " ".join(doc_content)
    corpus_tokens = corpus.split()
    return list(set(corpus_tokens))


def get_vector(data, vocab):
    dimension = len(vocab)
    vector = [0] * dimension
    data = data.split()
    for token in data:
        try:
            position = vocab.index(token)
            vector[position] += 1
        except ValueError:
            logger.error("{} does not exist in vocabulary".format(token))
    return vector


def get_query_terms(query_id):
    return ""


def remove_special_chars(token):
    for p in PCH:
        if token.startswith(p):
            return False
    return not token in PCH


def get_query_tokens(query_terms):
    tokens = nltk.tokenize.word_tokenize(query_terms)
    tokens = filter(remove_special_chars, tokens)
    return tokens


def rocchio(query_vector, rel_vectors, non_rel_vectors):
    sum_rel_vectors = list(imap(sum, zip(*rel_doc_vectors)))
    sum_rel_vectors = map(lambda x: x * BETA / len(rel_vectors), sum_rel_vectors)
    sum_non_rel_vectors = list(imap(sum, zip(*non_rel_doc_vectors)))
    sum_non_rel_vectors = map(lambda x: GAMMA * x / len(non_rel_vectors), sum_non_rel_vectors)
    query_vector = map(lambda x: x * ALPHA, query_vector)
    query_rel_vector = list(map(add, query_vector, sum_rel_vectors))
    new_query_vector = list(map(sub, query_rel_vector, sum_non_rel_vectors))
    return new_query_vector


def get_query(vocab, vector):
    query = ""
    for position, weight in enumerate(vector):
        if weight > 0:
            query += vocab[position]
    return query


modified_queries = []
for query_id, docs in results.iteritems():
    # relevant_docs = docs[:RELEVANT_DOC_COUNT]
    doc_names = map(lambda x: x[0], docs)
    doc_contents = get_content(doc_names)  # return list of strings
    vocabulary = get_vocabulary(doc_contents)
    query_string = get_query_terms(query_id)
    # query_tokens = get_query_tokens(query_terms)
    query_vector = get_vector(query_string, vocabulary)
    df = pd.DataFrame(doc_contents, columns=['document'])
    df['doc_vector'] = df['document'].apply(get_vector, args=(vocabulary,))
    doc_vectors = df['doc_vector'].tolist()
    rel_doc_vectors = doc_vectors[:RELEVANT_DOC_COUNT]
    non_rel_doc_vectors = doc_vectors[RELEVANT_DOC_COUNT:]
    modified_query_vector = rocchio(query_vector, rel_doc_vectors, non_rel_doc_vectors)
    modified_query = get_query(vocabulary, modified_query_vector)
    modified_queries.append(modified_query)

logger.info(modified_queries)