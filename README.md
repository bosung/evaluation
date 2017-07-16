# evaluation
This is simple evaluation tool for classification, information retrieval with precision, recall and F-measure.
Input and output is text file and you can see the graph if you want (set the option --graph y)

# Precision and Recall
ref. https://en.wikipedia.org/wiki/Precision_and_recall

when:
True positive: the weight of true among the result from Classifier(or System)
False positive: the weight of false among the result from Classfier(or System)
False negative: the weight of false among the technically true set(or answer set)

then:
Precision = true positive / (true positive + false positive)

Recall = true positive / (true positive + false negative)


# F-measure
The harmonic average of precision and recall.

F = 2 * (precision * recall) / (precision + recall)

# Usage
usage: evaluate.py [-h] [--ans_mode {single,multi}] [--delimiter {y}]
                   [--graph {y}]
                   input n


# Input file format (separator is '\t')

- ans_mode is "single"

answer  category1, category2, ... , categoryN   dummy_string

answer  category1, category2, ... , categoryN   dummy_string

answer  category1, category2, ... , categoryN   dummy_string

answer  category1, category2, ... , categoryN   dummy_string

answer  category1, category2, ... , categoryN   dummy_string

.
.
.

- ans_mode is "multi"

answer:0.8,answer:0.2   category1, category2, ... , categoryN   dummy_string

answer:0.7,answer:0.3   category1, category2, ... , categoryN   dummy_string

answer:0.7,answer:0.3   category1, category2, ... , categoryN   dummy_string

answer:0.9,answer:0.1   category1, category2, ... , categoryN   dummy_string

.
.
.


# Example (file: sample_input_single.txt)

- result
N: 1 	# of category set: 5

Macro Precision P@1: 0.307142857143

Macro Recall R@1: 0.316666666667

Macro F1-score N=1: 0.311832061069

Micro Precision P@1: 0.368421052632

Micro Recall R@1: 0.368421052632

Micro F1-score N=1: 0.368421052632

------------------------------------

N: 2 	# of category set: 5

Macro Precision P@2: 0.276666666667

Macro Recall R@2: 0.566666666667

Macro F1-score N=2: 0.371805006588

Micro Precision P@2: 0.315789473684

Micro Recall R@2: 0.631578947368

Micro F1-score N=2: 0.421052631579

------------------------------------

N: 3 	# of category set: 5

Macro Precision P@3: 0.237062937063

Macro Recall R@3: 0.666666666667

Macro F1-score N=3: 0.349754965179

Micro Precision P@3: 0.245614035088

Micro Recall R@3: 0.736842105263

Micro F1-score N=3: 0.368421052632

------------------------------------

N: 4 	# of category set: 5

Macro Precision P@4: 0.195798319328

Macro Recall R@4: 0.75

Macro F1-score N=4: 0.310528653932

Micro Precision P@4: 0.210526315789

Micro Recall R@4: 0.842105263158

Micro F1-score N=4: 0.336842105263
