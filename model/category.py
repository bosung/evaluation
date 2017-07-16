class Category:

    def __init__(self, category_name):
        self.category = category_name
        # true positive
        self.tp = 0
        # false positive
        self.fp = 0
        # false negative
        self.fn = 0
        # sum of 
        self.ans_sum = 0

    def __str__(self):
        return self.category
