# KeyGames: pke+

This is the repository for the pke+ implementation of KeyGames and other systems from the paper "KeyGames: A Game Theoretic approach to Keyphrase Extraction" published at COLING 2020. 

## Requirements

- [FastText-Pre-trained-word-vectors](https://fasttext.cc/docs/en/english-vectors.html)
	- Download the "wiki-news-300d-1M-subword.vec.zip" model (~7GB)
- [Input-datasets](https://github.com/mangalm96/KeyGames-pke/tree/master/data/input)
	- Clone with `git clone https://github.com/mangalm96/KeyGames-pke/tree/master/data/input`
	- Contains three datasets: Inspec, SemEval 2010 and DUC 2001.
- [pke](https://github.com/boudinfl/pke)
	- Install with `python3 -m pip install git+https://github.com/boudinfl/pke`
	- To execute EmbedRank you will need [sent2vec_wiki_bigrams](https://drive.google.com/open?id=0B6VhzidiLvjSaER5YkJUdWdPWU0) (16GB !) downloadable from [epfml/sent2vec]

## Running Pipeline

Follow along the general_pipeline.py to run the pipeline end to end from candidate selection to extraction.

## Citing this paper

If you use KeyGames, please cite the following paper:

```
@inproceedings{saxena-etal-2020-keygames,
    title = "{K}ey{G}ames: A Game Theoretic Approach to Automatic Keyphrase Extraction",
    author = "Saxena, Arnav  and
      Mangal, Mudit  and
      Jain, Goonjan",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.coling-main.184",
    pages = "2037--2048",
}
```
