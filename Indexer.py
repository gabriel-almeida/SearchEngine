__author__ = 'gabriel'
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, coo_matrix

def tf_idf(document_term_matrix):
        n_docs, n_terms = np.shape(document_term_matrix)
        buffer_max_tf = np.max(document_term_matrix, axis=0)

        buffer_df = np.zeros(n_terms)
        for term_id in range(n_terms):
            buffer_df[term_id] = np.count_nonzero(document_term_matrix[:, term_id])

        matrix_ids =  np.nonzero(document_term_matrix) # iterates only on valid matrix entries
        for i in range(len(matrix_ids[0])):
            doc_id = matrix_ids[0][i]
            term_id = matrix_ids[1][i]

            tf = 1.0*document_term_matrix[doc_id, term_id]
            max_tf = 1.0*buffer_max_tf[doc_id]
            df = 1.0*buffer_df[term_id]
            tf_idf = tf/max_tf * np.log10(n_docs/df)
            document_term_matrix[doc_id, term_id] = tf_idf


class Indexer():
    def __init__(self, weight_function = tf_idf):
        self.document_term_matrix = np.array([])
        self.weight_function = weight_function

    def generate_model(self, inverted_list):
        n_terms = len(inverted_list)
        n_docs = len({j for i in inverted_list.values() for j in i})

        self.document_term_matrix = np.zeros((n_docs, n_terms))
        self.term_dict = dict()

        term_id = 0

        for term in inverted_list:
            for doc_id in inverted_list[term]:
                self.document_term_matrix[doc_id-1, term_id] += 1
            self.term_dict[term] = term_id
            term_id += 1
        # self.document_term_matrix = csr_matrix(self.document_term_matrix)
        self.weight_function(self.document_term_matrix)

if __name__=="__main__":
    import InvertedList
    docs_dict = {1: "Olá, mundo imundo", 2:"olá mundo mundo", 3: "Teste imundo"}
    invListObj = InvertedList.InvertedListGenerator()
    inverted_list = invListObj.generate_inverted_list(docs_dict)
    indexer = Indexer()
    indexer.generate_model(inverted_list)
    print(indexer.document_term_matrix)
    print(indexer.term_dict)
