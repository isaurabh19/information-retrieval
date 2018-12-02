clean:
	rm -r src/__pycache__
	rm data/index/*

parse:
	python src/parser.py -case

index:
	python src/indexer.py
	python src/indexer.py -stop
	python src/indexer.py -stem

jm:
	python src/jm-smoothing.py -ifile stem_False_stop_False_inverted_index.txt -cfile stem_False_stop_False_corpus_stats.txt
	python src/jm-smoothing.py -stem -ifile stem_True_stop_False_inverted_index.txt -cfile stem_True_stop_False_corpus_stats.txt
	python src/jm-smoothing.py -stop -ifile stem_False_stop_True_inverted_index.txt -cfile stem_False_stop_True_corpus_stats.txt

lucene:
	javac -cp lib/*:. src/lucene.java
	java -cp lib/*:. src/lucene

	# /Users/samkeet/Downloads/IR-Project/data/index/lucene/regular
	# /Users/samkeet/Downloads/IR-Project/data/corpus

	# /Users/samkeet/Downloads/IR-Project/data/index/lucene/stem
	# /Users/samkeet/Downloads/IR-Project/data/stem_corpus

eval:
	# jm regular
	# jm stopped
	# lucene regular