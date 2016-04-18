__author__ = 'gabriel'
import ConfigReader
import Preprocessor
from xml.dom import minidom

class QueryProcessor:
    def __init__(self):
        self.query_dict = dict()
        self.expected_docs_by_query = dict()

    def write_queries(self, query_file_name, expected_file_name):
        with open(query_file_name, 'w') as file:
            for query_id, query in self.query_dict.items():
                file.write(query_id + ';' + query + '\n')
        with open(expected_file_name, 'w') as file:
            for query_id, tuples in self.expected_docs_by_query.items():
                file.write(query_id + ';[')
                for doc_id, votes in tuples:
                    file.write("(" + doc_id + "," + str(votes) + "),")
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
        configs = ConfigReader.read_cfg(cfg_file_name)
        for xml_file_name in configs['LEIA']:
            xml_file = minidom.parse(xml_file_name)
            query_list = xml_file.getElementsByTagName('QUERY')
            for query in query_list:
                self._process_xml_query(query)
        self.write_queries(configs['CONSULTAS'][0], configs['ESPERADOS'][0])


if __name__ == "__main__":
    qp = QueryProcessor()
    qp.process_queries()