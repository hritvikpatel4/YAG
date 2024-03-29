# Yet Another Google (YAG) [Algorithms for Information Retrieval]

Search Engine Implementation in Python

This project was implemented as part of a course.

The problem statement:
1. Build a search engine for [Environmental News NLP archive](https://www.kaggle.com/amritvirsinghx/environmental-news-nlp-dataset).
2. Build a corpus for archive with at least 418 documents.

Our search engine is capable of the following query types
* Simple Boolean Query (for eg: good deed -> this would translate to "good AND deed")
* Phrase Query (for eg: prince charles)
* Wildcard Query (for eg: nat* , \*til , nat\*nal)

Some features include
* Corpus and Query Preprocessing
* Inverted Index
* Parallelized Index Construction
* Ranked Results (for top K documents retrieval)
* Searching on a single index (for eg: republicans and democrats | CNN.201710.csv)

## Getting Started

The following steps will help you setup and run the project.

### Prerequisites

Installing external libraries using requirements.txt

```
python -m pip install -r requirements.txt
```

## Executing Code

* Windows
```
python main.py
```

* Linux
```
python3 main.py
```

## Built With

* [NLTK](https://www.nltk.org/) - For Natural Language processing and Corpus Preprocessing
* [pandas](https://pandas.pydata.org/) - For reading and interpreting csv files in the dataset
* [bidict](https://bidict.readthedocs.io/en/master/) - For the Bidirectional Dictionary
* [pygtrie](https://github.com/google/pygtrie) - For Index Construction

## Authors

* **Archana Prakash** - [GitHub](https://github.com/ArchPrak)
* **Hritvik Patel**  - [GitHub](https://github.com/hritvikpatel4)
* **Shreyas BS** - [GitHub](https://github.com/bsshreyas99)
* **Sriram SK** - [GitHub](https://github.com/sriramsk1999)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
