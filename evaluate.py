from model.category import Category
import argparse
import matplotlib.pyplot as plt
import numpy as np


def f1_score(precision, recall):
    return 2 * (precision * recall) / (precision + recall)


def calc_precision_recall_macro_avg(category_dict):
    macro_precision_sum = []
    macro_recall_sum = []

    for category in category_dict:
        tp, fp, fn = category_dict[category].tp, category_dict[category].fp, category_dict[category].fn

        if (tp + fp) is not 0:
            macro_precision_sum.append(tp / (tp + fp))

        if (tp + fn) is not 0:
            macro_recall_sum.append(tp / (tp + fn))

    macro_precision = np.average(np.array(macro_precision_sum))
    macro_recall = np.average(np.array(macro_recall_sum))

    return macro_precision, macro_recall
    

def calc_precision_recall_micro_avg(category_dict):
    tp_sum = 0
    fp_sum = 0
    fn_sum = 0

    for category in category_dict:
        tp, fp, fn = category_dict[category].tp, category_dict[category].fp, category_dict[category].fn
        tp_sum += tp
        fp_sum += fp
        fn_sum += fn

    micro_precision = tp_sum / (tp_sum + fp_sum)
    micro_recall = tp_sum / (tp_sum + fn_sum)

    return micro_precision, micro_recall


def sum_each_answer_categories(category_dict, ans_list):
    for ans_dict in ans_list:
        ans_dict_ = ans_dict
        for category in ans_dict_:
            category_dict[category].ans_sum += ans_dict_[category]
    return category_dict


def get_multi_ans_dict(answer):
    ret_dict = {}
    ans_list = [x.strip() for x in answer.split(",")]
    for ans in ans_list:
        tokens = ans.split(":")
        if len(tokens) == 2:
            ret_dict[tokens[0]] = float(tokens[1])
    return ret_dict


def evaluate(args):
    _input_path = args.input
    _n = args.n
    _ans_mode = args.ans_mode if args.ans_mode else "single"
    _delimiter = args.delimiter if args.delimiter else "\t"
    _graph = args.graph if args.graph else "n"

    prediction_data_list = []
    ans_flag_list = []
    ans_list = []

    # store all category's data
    category_dict = {}

    f = open(_input_path, "r")
    lines = f.readlines()
    for line in lines:
        _line = line.strip()

        tokens = [x.strip() for x in _line.split(_delimiter)]

        if len(tokens) != 2 and len(tokens) != 3:
            raise BaseException("Wrong input format")

        answer = tokens[0]
        candidates = [x.strip() for x in tokens[1].split(",")]

        if _ans_mode == "single":
            ans_dict = {answer: 1}
            category_dict[answer] = Category(answer)
        else:
            ans_dict = get_multi_ans_dict(answer)
            for category in ans_dict:
                category_dict[category] = Category(category)

        ans_list.append(ans_dict)

        _tmp_predict_data = []
        _tmp_ans_flag = []

        for candi in candidates:
            _tmp_predict_data.append(candi)
            if candi in ans_dict:
                _tmp_ans_flag.append(ans_dict[candi])
            else:
                _tmp_ans_flag.append(0)

        prediction_data_list.append(_tmp_predict_data)
        ans_flag_list.append(_tmp_ans_flag)

    # sum answer categories weight
    category_dict = sum_each_answer_categories(category_dict, ans_list)
    
    # list for graph
    macro_precision_list = []
    micro_precision_list = []
    macro_recall_list = []
    micro_recall_list = []

    n_predict_data = np.transpose(np.array(prediction_data_list))
    n_ans_flag_list = np.transpose(np.array(ans_flag_list))

    for i in range(0, _n):
        data = n_predict_data[i]

        # calc tp, fp
        for j in range(0, len(data)):
            category = data[j]

            if n_ans_flag_list[i][j] > 0:
                # tp
                category_dict[category].tp += n_ans_flag_list[i][j]
            else:
                # fp
                if category not in category_dict:
                    category_dict[category] = Category(category)

                fp = 0
                _tmp_ans_dict = ans_list[j]
                for ans in _tmp_ans_dict:
                    if category != ans:
                        fp += _tmp_ans_dict[ans]

                category_dict[category].fp += fp

        # calc fn
        for category in category_dict:
            # fn = ans sum - tp
            category_dict[category].fn = category_dict[category].ans_sum - category_dict[category].tp

        # macro avg
        macro_precision, macro_recall = calc_precision_recall_macro_avg(category_dict)
        
        # micro avg
        micro_precision, micro_recall = calc_precision_recall_micro_avg(category_dict)

        # print result
        category_num = len(category_dict)
        print("------------------------------------")
        print("N: %s \t# of category set: %s" % (str(i+1), str(category_num)))
        print("\nMacro Precision P@%s: %s" % (str(i+1), str(macro_precision)))
        print("Macro Recall R@%s: %s" % (str(i+1), str(macro_recall)))
        print("Macro F1-score N=%s: %s" % (str(i+1), f1_score(macro_precision, macro_recall)))

        print("\nMicro Precision P@%s: %s" % (str(i+1), str(micro_precision)))
        print("Micro Recall R@%s: %s" % (str(i+1), str(micro_recall)))
        print("Micro F1-score N=%s: %s" % (str(i+1), f1_score(micro_precision, micro_recall)))

        # data for drawing graph
        macro_precision_list.append(macro_precision)
        micro_precision_list.append(micro_precision)
        macro_recall_list.append(macro_recall)
        micro_recall_list.append(micro_recall)
    
    if _graph == "y":
        idx = [i+1 for i in range(0, _n)]
        graph_input = [macro_precision_list, micro_precision_list, macro_recall_list, micro_recall_list]
        plt_show(idx, graph_input)


def plt_show(idx, data):
    plt.clf()
    for e in data:
        plt.plot(idx, e)

    plt.legend(['precision macro avg', 'precision micro avg', 'recall macro avg', 'recall micro avg'], loc='upper left')
    plt.xlabel("N")
    plt.ylim(0.0, 1.0)

    major_ticks = np.arange(1, len(idx)+1, 1)
    plt.xticks(major_ticks)

    plt.title("Precision & Recall")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input file path')
    parser.add_argument('n', type=int, help='The N with R@N, P@N')
    parser.add_argument('--ans_mode', choices=["single", "multi"], help="""
        If each prediction has only one answer, ans_mode=single otherwise ans_mode=multi""")
    parser.add_argument('--delimiter', choices=["y"], help='delimiter')
    parser.add_argument('--graph', choices=["y"], help='show graph')

    args = parser.parse_args()
    evaluate(args)
