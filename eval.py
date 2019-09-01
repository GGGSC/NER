import os
from sklearn.metrics import f1_score, recall_score, precision_score

tag2label = {"B-ENT": 0, "I-ENT": 1,
             "B-HYPER": 2, "I-HYPER": 3,
             "O": 4
             }
               # "ENT-B": 0,   "ENT-I": 1,
#              "ENT-E": 2,   "ENT-S": 3,
#              "BIRTH-B": 4, "BIRTH-I": 5,
#              "BIRTH-E": 6, "BIRTH-S": 7,
#              "BPLACE-B": 8, "BPLACE-I": 9,
#              "BPLACE-E": 10, "BPLACE-S": 11,
#              "COM-B": 12,  "COM-I": 13,
#              "COM-E": 14, "COM-S": 15,
#              "COLLEGE-B": 16, "COLLEGE-I": 17,
#              "COLLEGE-E": 18, "COLLEGE-S": 19,
#              "DEAD-B": 20, "DEAD-I": 21,
#              "DEAD-E": 22, "DEAD-S": 23,
#              "O": 24


def conlleval(label_predict, label_path, metric_path):
    """
    :param label_predict
    :param label_path
    :param metric_path
    :return:
    """
    eval_perl = "./conlleval_rev.pl"
    # Writing the final results
    with open(label_path, "w", encoding='utf8') as fw:
        line = []
        real_result = []
        predict_result = []
        for sent_result in label_predict:
            for char, tag, tag_ in sent_result:
                tag_ = 'O' if tag_ == 0 else tag_
                tag = 'O' if tag == 0 else tag
                line.append("{} {} {}\n".format(char, tag, tag_))
                real_result.append(int(tag2label[tag]))
                predict_result.append(int(tag2label[tag_]))
            line.append("\n")
        f1 = f1_score(real_result, predict_result, average='macro')
        recall = recall_score(real_result, predict_result, average='macro')
        precision = precision_score(real_result, predict_result, average='macro')
        results = "Precision = {} , Recall = {}, f1 = {}".format(precision, recall, f1)
        fw.writelines(line)
    os.system("perl {} < {} > {}".format(eval_perl, label_path, metric_path))
    with open(metric_path, 'w', encoding='utf8') as fr:
        fr.write(results)
    return results

