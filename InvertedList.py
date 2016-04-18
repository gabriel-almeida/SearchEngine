__author__ = 'gabriel'
import Preprocessor
from xml.dom import minidom
import ConfigReader

class InvertedListGenerator:
    def __init__(self):
        self.in_file = []

    def parse_corpus(self, cfg_file):
        configs = ConfigReader.read_cfg(cfg_file)

        corpus = dict()
        for in_file in configs["LEIA"]:
            document = self.read_xml(in_file)
            corpus.update(document)

        inv_list = self.generate_inverted_list(corpus)
        self.write_inverted_list(inv_list, configs["ESCREVE"][0])

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
    invList = InvertedListGenerator()
    invList.parse_corpus("gli.cfg")