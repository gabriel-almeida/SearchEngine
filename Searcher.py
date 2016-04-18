__author__ = 'gabriel'

import ConfigReader
import pickle
from Indexer import TfIdf


class Searcher:
    def __init__(self):
        pass

    def do_search(self, config_file_name="busca.cfg"):
        cfg = ConfigReader.read_cfg(config_file_name)
        model_file_name = cfg["MODELO"][0]
        queries_file_name = cfg["CONSULTAS"][0]
        results_file_name = cfg["RESULTADOS"][0]

        self.model = pickle.load(open(model_file_name, 'rb'))
        with open(results_file_name, 'w') as results_file:
            with open(queries_file_name) as queries:
                for l in queries.readlines():
                    temp = l.split(';')
                    query_id = temp[0]
                    query = temp[1]
                    self._write(query_id, query, results_file)

    def _write(self, query_id, query, results_file):
        similarities = self.model.retrieve(query)
        sorted_docs = list(similarities .keys())
        sorted_docs.sort(key=lambda doc_id: similarities[doc_id], reverse=True)

        results_file.write(query_id + "; [")
        i = 1
        for doc_id in sorted_docs:
            results_file.write("(" + str(i) + ", " + str(doc_id) + ", " + str(similarities[doc_id]) + "), ")
            i += 1
        results_file.write("]\n")

if __name__=="__main__":
    searcher = Searcher()
    searcher.do_search()