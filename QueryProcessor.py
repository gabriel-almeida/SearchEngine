import ConfigReader
import Preprocessor
from xml.dom import minidom
import logging
import time

__author__ = 'gabriel'


class QueryProcessor:
    def __init__(self):
        self.query_dict = dict()
        self.expected_docs_by_query = dict()

    def write_queries(self, query_file_name, expected_file_name):
        with open(query_file_name, 'w') as file:
            for query_id, query in self.query_dict.items():
                file.write(str(int(query_id)) + ';' + query + '\n')
        with open(expected_file_name, 'w') as file:
            for query_id, tuples in self.expected_docs_by_query.items():
                file.write(str(int(query_id)) + ';[')
                for doc_id, votes in tuples:
                    file.write("(" + str(int(doc_id)) + "," + str(votes) + "),")
                file.write("]\n")

    def _process_xml_query(self, xml_node):
        query_id = xml_node.getElementsByTagName("QueryNumber")[0].firstChild.nodeValue
        query = xml_node.getElementsByTagName("QueryText")[0].firstChild.nodeValue

        processed_query = " ".join(Preprocessor.preprocessor_tokenizer(query))
        self.query_dict[query_id] = processed_query

        records = xml_node.getElementsByTagName("Records")[0]
        relevant_documents_list = list()
        for item in records.getElementsByTagName("Item"):
            doc_id = item.firstChild.nodeValue

            scores = item.getAttribute("score")
            votes = 0
            for i in range(len(scores)):
                if scores[i]!='0':
                    votes += 1

            relevant_documents_list.append((doc_id, votes))
        self.expected_docs_by_query[query_id] = relevant_documents_list

    def process_queries(self, cfg_file_name='pc.cfg'):
        logging.info("Execution begin")

        configs = ConfigReader.read_cfg(cfg_file_name)
        logging.info("Configuration file read")

        begin = time.perf_counter()
        for xml_file_name in configs['LEIA']:
            xml_file = minidom.parse(xml_file_name)
            query_list = xml_file.getElementsByTagName('QUERY')
            for query in query_list:
                self._process_xml_query(query)
        end = time.perf_counter()
        elapsed = end - begin
        logging.info("Queries processed: " + str(len(self.expected_docs_by_query)) + " queries read from " + str(len(configs['LEIA'])) + " file(s)")
        logging.info("Query processor performance: " + str(len(self.expected_docs_by_query)/elapsed) + " queries per second.")

        self.write_queries(configs['CONSULTAS'][0], configs['ESPERADOS'][0])
        logging.info("Query processing saved")
        logging.info("Execution ended")


if __name__ == "__main__":
    logging.basicConfig(filename='log/query-processor.log', level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')
    qp = QueryProcessor()
    qp.process_queries()
