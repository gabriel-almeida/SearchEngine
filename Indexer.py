import math
import ConfigReader
import pickle
import collections
import Preprocessor

__author__ = 'gabriel'

class TfIdf:
    def __init__(self):
        pass

    def generate_model(self, inverted_list):
        self.inverted_list = inverted_list
        self.n_terms = len(inverted_list)
        self.n_docs = len({j for i in inverted_list.values() for j in i})

        self.document_frequency = dict()
        self.term_document_frequency = dict()
        self.document_max_term_frequency = dict()

        for term in inverted_list:
            counter = collections.Counter(inverted_list[term])

            # number of times a term appears on different documents
            self.document_frequency[term] = len(counter.keys())
            self.term_document_frequency[term] = counter
            for doc_id in counter:
                if doc_id not in self.document_max_term_frequency or \
                self.document_max_term_frequency[doc_id] < counter[doc_id]:
                    self.document_max_term_frequency[doc_id] = counter[doc_id]

    def weight(self, term, doc_id):
        if term not in self.document_frequency:
            return 0.0

        tf = self.term_document_frequency[term][doc_id]
        max_tf = self.document_max_term_frequency[doc_id]
        df = self.document_frequency[term]
        tf_idf = tf/max_tf * math.log10(self.n_docs/df)
        return tf_idf

    def query_vector(self, query):
        terms = Preprocessor.preprocessor_tokenizer(query)

        counter = collections.Counter(terms)
        query_vector = dict()
        query_vector_magnitude = 0
        for term in terms:
            if term not in self.document_frequency:
                continue

            max_tf = counter.most_common(1)[0][1] # it returns an list of item + frequency
            tf = counter[term]
            df = self.document_frequency[term]
            val = (0.5 + 0.5*tf/max_tf)*math.log10(self.n_terms/df)
            query_vector[term] = val

            query_vector_magnitude += val*val

        # normalizing step
        query_vector_magnitude = math.sqrt(query_vector_magnitude)
        for term in query_vector:
            query_vector[term] /= query_vector_magnitude

        return query_vector

    def retrieve(self, query):
        query_vec = self.query_vector(query)

        candidates = set()
        for term in query_vec.keys():
            candidates.update(self.inverted_list[term])

        docs_similarity = dict()
        for doc_id in candidates:
            doc_sim = 0
            doc_magnitude = 0

            for query_term in query_vec:
                doc_component = self.weight(query_term, doc_id)
                doc_magnitude += doc_component*doc_component

                # dot product
                doc_sim += doc_component * query_vec[query_term]

            # normalizing step
            doc_magnitude = math.sqrt(doc_magnitude)
            docs_similarity[doc_id] = doc_sim/doc_magnitude
        return docs_similarity


class Indexer():
    def __init__(self, weight_function = TfIdf()):
        self.weight_function = weight_function

    def read_inv_list(self, inv_list_file):
        inv_list = dict()
        with open(inv_list_file) as file:
            for l in file.readlines():
                temp = l.split(';')
                term = temp[0]
                list = temp[1]
                inv_list[term] = eval(list)
        return inv_list

    def do_index(self, cfg_file="index.cfg"):
        cfg = ConfigReader.read_cfg(cfg_file)
        inv_list_file = cfg['LEIA'][0]
        model_file = cfg['ESCREVA'][0]
        inv_list = self.read_inv_list(inv_list_file)

        self.weight_function.generate_model(inv_list)
        with open(model_file, 'wb') as pick_file:
            pickle.dump(self.weight_function, pick_file)


if __name__ == "__main__":
    index = Indexer()
    index.do_index()
