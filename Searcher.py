__author__ = 'gabriel'
import Indexer
import Preprocessor
import numpy as np

class Searcher:
    def __init__(self, index = Indexer.Indexer()):
        self.index = index

    def search(self, query):
        tokens = Preprocessor.preprocessor_tokenizer(query)
        candidate_docs = None
        n_docs, n_terms = np.shape(self.index.document_term_matrix)

        query_vector = np.zeros((1, n_terms))
        for token in tokens:
            if token not in self.index.term_dict:
                continue
            term_id = self.index.term_dict[token]
            query_vector[0, term_id] +=  1

            # candidates = np.where(self.index.document_term_matrix[:, term_id][0])
            # candidates = set(candidates)
            # if candidate_docs is None:
            #     candidate_docs = candidates
            # else:
            #     candidate_docs.intersection(candidates)

        docs_sim = []
        for doc_id in range(n_docs):
            similarity = self.index.document_term_matrix[doc_id, :] * query_vector.T
            docs_sim.append(similarity[0][0])

        return docs_sim

if __name__=="__main__":
    import InvertedList
    docs_dict = {1: "Olá, mundo imundo", 2:"olá mundo mundo"}
    invListObj = InvertedList.InvertedListGenerator()
    inverted_list = invListObj.generate_inverted_list(docs_dict)
    indexer = Indexer.Indexer()
    indexer.generate_model(inverted_list)
    searcher = Searcher(indexer)
    print(searcher.search("mundo"))