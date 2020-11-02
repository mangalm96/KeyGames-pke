# KeyGames: pke+

This is the repository for the pke+ implementation of KeyGames and other systems from the paper "KeyGames: A Game Theoretic approach to Keyphrase Extraction" accepted at COLING 2020. 

## Requirements

- [FastText-Pre-trained-word-vectors](https://fasttext.cc/docs/en/english-vectors.html)
	- Download the "wiki-news-300d-1M-subword.vec.zip" model (~7GB)
- [pke](https://github.com/boudinfl/pke)
	- Install with `python3 -m pip install git+https://github.com/boudinfl/pke`
	- To execute EmbedRank you will need [sent2vec_wiki_bigrams](https://drive.google.com/open?id=0B6VhzidiLvjSaER5YkJUdWdPWU0) (16GB !) downloadable from [epfml/sent2vec]
- [Input-datasets](https://github.com/mangalm96/KeyGames-pke/tree/master/data/input)
	- Clone with `git clone https://github.com/mangalm96/KeyGames-pke/tree/master/data/input`
	- Contains three datasets: Inspec, SemEval 2020 and DUC 2001.

## Running Pipeline

Follow along the general_pipeline.py to run the pipeline end to end from candidate selection to extraction.

## Citing this paper

"KeyGames: A Game Theoretic approach to Keyphrase Extraction" at COLING 2020. 