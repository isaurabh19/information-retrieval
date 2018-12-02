clean:
	rm -r src/__pycache__

parse:
	python src/parser.py -case

index:
	python src/indexer.py
	python src/indexer.py -stop
	python src/indexer.py -stem

jm:
	python src/jm-smoothing.py
	python src/jm-smoothing.py -stem
	python src/jm-smoothing.py -stop

tfidf:
	python src/tfidf.py
	python src/tfidf.py -stem
	python src/tfidf.py -stop

bm25:
	python src/bm25.py
	python src/bm25.py -stem
	python src/bm25.py -stop

bm25:
	javac -cp lib/*:. src/lucene.java
	java -cp lib/*:. src/lucene

	# /Users/samkeet/Downloads/IR-Project/data/model/regular
	# /Users/samkeet/Downloads/IR-Project/data/corpus

	# /Users/samkeet/Downloads/IR-Project/data/model/stem
	# /Users/samkeet/Downloads/IR-Project/data/stem_corpus

eval/lucene:
	python src/evaluation.py -m lucene -f stem_False_stop_False_lucene_score.txt
	
eval/jm:
	python src/evaluation.py -m jm -f stem_False_stop_False_jm_score.txt
	python src/evaluation.py -m jm -f stem_False_stop_True_jm_score.txt

eval/tfidf:
	python src/evaluation.py -m tfidf -f stem_False_stop_False_tfidf_score.txt
	python src/evaluation.py -m tfidf -f stem_False_stop_True_tfidf_score.txt
	
eval/bm25:
	python src/evaluation.py -m bm25 -f stem_False_stop_False_bm25_score.txt
	python src/evaluation.py -m bm25 -f stem_False_stop_True_bm25_score.txt