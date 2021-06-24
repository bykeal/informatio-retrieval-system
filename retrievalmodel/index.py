import os
import sys
import pickle
import math
from collections import Counter
from .utils import textprocessing, helpers
''' Index data '''

def runfile():
    print('Indexing....')

    resources_path = os.path.join(os.getcwd(), 'retrievalmodel//resources')
    data_path = os.path.join(os.getcwd(), 'retrievalmodel//data')

    if not os.path.isdir(resources_path):
        print('ERROR: The {} is not a directory or does not exist'.format(
            resources_path))
        sys.exit(1)

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # Get dataset path and stopwords file
    dataset_path = os.path.join(resources_path, 'dataset')
    stopwords_file = os.path.join(resources_path, 'stopwords_en.txt')

    # Get stopwords set
    stopwords = helpers.get_stopwords(stopwords_file)

    docs = helpers.get_docs(dataset_path)

    corpus = []
    for doc in docs:
        with open(doc, mode='r') as f:
            text = f.read()
            words = textprocessing.preprocess_text(text, stopwords)
            bag_of_words = Counter(words)
            corpus.append(bag_of_words)

    idf = helpers.compute_idf(corpus)
    for doc in corpus:
        helpers.compute_weights(idf, doc)
        helpers.normalize(doc)

    inverted_index = helpers.build_inverted_index(idf, corpus)

    docs_file = os.path.join(data_path, 'docs.pickle')
    inverted_index_file = os.path.join(data_path, 'inverted_index.pickle')
    dictionary_file = os.path.join(data_path, 'dictionary.txt')

    # Serialize data
    with open(docs_file, 'wb') as f:
        pickle.dump(docs, f)

    with open(inverted_index_file, 'wb') as f:
        pickle.dump(inverted_index, f)

    with open(dictionary_file, 'w') as f:
        for word in idf.keys():
            f.write(word + '\n')

    print('Index done.')
