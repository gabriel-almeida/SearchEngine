__author__ = 'gabriel'
import numpy as np
from scipy.sparse import lil_matrix

def tf_idf(doc_id, term_id, document_term_matrix):
        n_docs, n_terms = np.shape(document_term_matrix)

        tf = document_term_matrix[doc_id, term_id]
        max_tf = np.max(document_term_matrix[doc_id, :])

        df = np.count_nonzero(document_term_matrix[:, term_id])

        tf_idf = tf/max_tf * np.log(n_docs/df)

        return tf_idf


class Indexer():
    def __init__(self, weight_function = tf_idf):
        self.document_term_matrix = np.array([])

    def generate_model(self, inverted_list):
        n_terms = len(inverted_list)
        n_docs = len({j for i in inverted_list.values() for j in i})

        self.document_term_matrix = lil_matrix((n_docs, n_terms))
        self.term_dict = dict()

        term_id = 0

        for term in inverted_list:
            for doc_id in inverted_list[term]:
                self.document_term_matrix[doc_id-1, term_id] += 1
            self.term_dict[term] = term_id
            term_id += 1


if __name__=="__main__":
    import InvertedList
    docs_dict = {1: "Olá, mundo imundo", 2:"olá mundo mundo"}
    invListObj = InvertedList.InvertedListGenerator()
    inverted_list = invListObj.generateInvertedList(docs_dict)
    indexer = Indexer()
    indexer.generate_model(inverted_list)
    print(indexer.document_term_matrix)
