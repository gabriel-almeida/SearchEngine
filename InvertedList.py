__author__ = 'gabriel'
import Preprocessor

class InvertedListGenerator:
    def __init__(self):
        pass

    def generateInvertedList(self, docs_dict):
        inv_list = dict()
        for (doc_id, doc) in docs_dict.items():
            term_list = Preprocessor.preprocessor_tokenizer(doc)
            for term in term_list:
                if term not in inv_list:
                    inv_list[term] = []
                inv_list[term].append(doc_id)
        return inv_list

if __name__ == "__main__":
    docs_dict = {1: "Olá, mundo imundo", 2:"olá mundo mundo"}
    invList = InvertedListGenerator()
    print(invList.generateInvertedList(docs_dict))