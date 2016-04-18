import ConfigReader
import pickle
import logging
import time
from Indexer import TfIdf


class Searcher:
    def __init__(self):
        pass

    def do_search(self, config_file_name="busca.cfg"):
        logging.info("Execution begin")
        cfg = ConfigReader.read_cfg(config_file_name)
        logging.info("Configuration file read")

        model_file_name = cfg["MODELO"][0]
        queries_file_name = cfg["CONSULTAS"][0]
        results_file_name = cfg["RESULTADOS"][0]

        self.model = pickle.load(open(model_file_name, 'rb'))
        logging.info("Model loaded")

        queries = dict()
        with open(queries_file_name) as queries_file:
            for l in queries_file.readlines():
                temp = l.split(';')
                query_id = temp[0]
                query = temp[1]
                queries[query_id] = query

        n_queries = len(queries)
        logging.info("Queries file loaded: " + str(n_queries) + " loaded")

        query_results = dict()
        begin_time = time.perf_counter()
        for query_id in queries:
            similarities = self.model.retrieve(queries[query_id])
            query_results[query_id] = similarities

        end_time = time.perf_counter()
        elapsed_time = end_time - begin_time

        logging.info("Retrieval done")
        logging.info("Retrieval performance: " + str(n_queries/elapsed_time) + " queries per seconds")

        with open(results_file_name, 'w') as results_file:
            for query_id in query_results:
                self._write(query_id, query_results[query_id], results_file)

        logging.info("Queries results saved")
        logging.info("Execution ended")

    def _write(self, query_id, similarities, results_file):
        sorted_docs = list(similarities .keys())
        sorted_docs.sort(key=lambda doc_id: similarities[doc_id], reverse=True)

        results_file.write(query_id + "; [")
        i = 1
        for doc_id in sorted_docs:
            results_file.write("(" + str(i) + ", " + str(doc_id) + ", " + str(similarities[doc_id]) + "), ")
            i += 1
        results_file.write("]\n")

if __name__ == "__main__":
    logging.basicConfig(filename='log/searcher.log', level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')
    searcher = Searcher()
    searcher.do_search()