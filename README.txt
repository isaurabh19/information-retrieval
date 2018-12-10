Run Instructions:

Follwing commands are to be run from the src directory

[0] Preprocessing
This step involves pre-processing the cacm.queries.txt, cacm.rel.txt

python parser_cacm_query.py
python parser_query_map.py
python parser_cacm_rel.py

[1] Parsing and cleaning corpus
python parser.py -case

[2] Parsing stem corpus
python parser_cacm_stem_corpus.py

[3] Create 3 Inverted indexes
python indexer.py
python indexer.py -stop
python indexer.py -stem

[4] JM Smoothing
python jmsmoothing.py
python jmsmoothing.py -stem
python jmsmoothing.py -stop

[5] TF-IDF
python tfidf.py
python tfidf.py -stem
python tfidf.py -stop

[6] BM25
python bm25.py
python bm25.py -stem
python bm25.py -stop

[7] Lucene
javac -cp lib/*:. lucene.java
java -cp lib/*:. lucene

To parse the results from the files
python parser_lucene_result.py

[8] Query Enrichment Run
python query_enrichment.py

[9] Snippet Generation
python snippetgenerator.py -d -m bm25 -f stem_False_stop_False_bm25_score.json

[10] Evaluation
python evaluation.py