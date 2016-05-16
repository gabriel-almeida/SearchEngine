__author__ = 'gabriel'


def precision_at_n(expected_dict, retrieved_dict, n=10):
    averaged_precision = 0.0

    for query_id, retrieved_docs in retrieved_dict.items():
        expected_docs = { doc_id for doc_id, _ in expected_dict[query_id]}
        true_positives = 0.0
        for i in range(n):
            retrieved_doc_id = retrieved_docs[i][1]
            if retrieved_doc_id in expected_docs:
                true_positives += 1.0
        current_precision = 1.0*true_positives/n
        averaged_precision +=  current_precision
    averaged_precision /= len(expected_dict)
    return averaged_precision

def mean_averaged_precision(expected_dict, retrieved_dict):
    mean_averaged_prec = 0.0
    for query_id, retrieved_docs in retrieved_dict.items():
        expected_docs = { doc_id for doc_id, _ in expected_dict[query_id]}
        averaged_precision = 0.0
        for n in range(1, len(expected_docs)+1):
            true_positives = 0.0
            for i in range(min(n, len(retrieved_docs))):
                retrieved_doc_id = retrieved_docs[i][1]
                if retrieved_doc_id in expected_docs:
                    true_positives += 1.0
            current_precision = 1.0*true_positives/n
            averaged_precision +=  current_precision
        averaged_precision /= len(expected_docs)
        mean_averaged_prec += averaged_precision
    mean_averaged_prec /= len(retrieved_dict)
    return mean_averaged_prec

def f1(expected_dict, retrieved_dict, n = 20):
    averaged_f1 = 0.0

    for query_id, retrieved_docs in retrieved_dict.items():
        expected_docs = { doc_id for doc_id, _ in expected_dict[query_id]}
        true_positives = 0.0

        for i in range(n):
            retrieved_doc_id = retrieved_docs[i][1]
            if retrieved_doc_id in expected_docs:
                true_positives += 1.0

        recall = 1.0*true_positives/len(expected_docs)
        precision = 1.0*true_positives/n
        if recall+precision == 0:
            f1 = 0.0
        else:
            f1 = 2.0*precision*recall/(precision+recall)

        averaged_f1 +=  f1
    averaged_f1 /= len(expected_dict)
    return averaged_f1



class Evaluator:
    def __init__(self):
        pass

    def load_results(self, expected_file_name='out/expected.csv', results_file_name='out/results.csv'):
        self.expected_dict = dict()
        with open(expected_file_name, 'r') as expected_file:
            for line in expected_file.readlines():
                fields = line.split(';')
                query_id = fields[0]
                expected_docs = eval(fields[1])
                self.expected_dict[query_id] = expected_docs

        self.retrieved_dict = dict()
        with open(results_file_name, 'r') as results_file:
            for line in results_file.readlines():
                fields = line.split(';')
                query_id = fields[0]
                retrieved_docs = eval(fields[1])
                self.retrieved_dict[query_id] = retrieved_docs

    def evaluate(self, metric=f1):
        return metric(self.expected_dict, self.retrieved_dict)


if __name__ == "__main__":
    ev = Evaluator()

    ev.load_results(results_file_name="out/results.csv")
    print("Python:\n=========")
    print("Precision@10", ev.evaluate(metric=precision_at_n))
    print("F1", ev.evaluate(metric=f1))
    print("MAP", ev.evaluate(metric=mean_averaged_precision))

    ev.load_results(results_file_name="out/results_lucene.csv")
    print("\nLucene:\n=========")
    print("Precision@10", ev.evaluate(metric=precision_at_n))
    print("F1", ev.evaluate(metric=f1))
    print("MAP", ev.evaluate(metric=mean_averaged_precision))
