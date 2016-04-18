import Preprocessor
from xml.dom import minidom
import ConfigReader
import logging
import time

__author__ = 'gabriel'


class InvertedListGenerator:
    def __init__(self):
        self.in_file = []

    def parse_corpus(self, cfg_file):
        logging.info("Execution begin")

        configs = ConfigReader.read_cfg(cfg_file)
        logging.info("Configuration file read")

        corpus = dict()
        for in_file in configs["LEIA"]:
            document = self.read_xml(in_file)
            corpus.update(document)

        logging.info("Corpus read: " + str(len(corpus)) + " documents readed from " + str(len(configs["LEIA"])) + " files")

        begin = time.perf_counter()
        inv_list = self.generate_inverted_list(corpus)
        end = time.perf_counter()
        elapsed = end - begin

        logging.info("Inverted list generated: " + str(len(inv_list)) + " terms collected")
        logging.info("Inverted list performance: " + str(len(corpus)/elapsed) + " documents per second")

        self.write_inverted_list(inv_list, configs["ESCREVE"][0])
        logging.info("Inverted list saved")
        logging.info("Execution ended")

    def write_inverted_list(self, inverted_list, out_file):
        with open(out_file, 'w') as out:
            for term, docs in inverted_list.items():
                out.write(term + ";" + str(docs) + "\n")

    def read_xml(self, xml_file):
        xml_file = minidom.parse(xml_file)
        item_list = xml_file.getElementsByTagName('RECORD')
        docs_dict = dict()

        for item in item_list:
            record_num = item.getElementsByTagName('RECORDNUM')
            record_num =  int(record_num[0].firstChild.nodeValue)
            abstract = item.getElementsByTagName('ABSTRACT')

            if len(abstract) > 0:
                current_doc = abstract[0].firstChild.nodeValue
            else:
                extract = item.getElementsByTagName('EXTRACT')
                if len(extract) > 0:
                    current_doc = extract[0].firstChild.nodeValue
                else:
                    continue

            docs_dict[record_num] = current_doc
        return docs_dict

    def generate_inverted_list(self, docs_dict):
        inv_list = dict()
        for (doc_id, doc) in docs_dict.items():
            term_list = Preprocessor.preprocessor_tokenizer(doc)
            for term in term_list:
                if term not in inv_list:
                    inv_list[term] = []
                inv_list[term].append(doc_id)
        return inv_list

if __name__ == "__main__":
    logging.basicConfig(filename='log/inverted_list.log', level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')
    invList = InvertedListGenerator()
    invList.parse_corpus("gli.cfg")