import itertools


class RuleMiner(object):

    def __init__(self, support_t, confidence_t): 

        self.support_t = support_t
        self.confidence_t = confidence_t

    def get_support(self, data, itemset):

        return data[itemset].all(axis=1).sum()

    def merge_itemsets(self, itemsets):

        new_itemsets = []

        cur_num_items = len(itemsets[0])

        if cur_num_items == 1:
            for i in range(len(itemsets)):
                for j in range(i + 1, len(itemsets)):
                    new_itemsets.append(list(set(itemsets[i]) | set(itemsets[j])))

        else:
            for i in range(len(itemsets)):
                for j in range(i + 1, len(itemsets)):
                    combined_list = list(set(itemsets[i]) | set(itemsets[j]))
                    combined_list.sort()
                    if len(combined_list) == cur_num_items + 1 and combined_list not in new_itemsets:
                        new_itemsets.append(combined_list)

        return new_itemsets

    def get_rules(self, itemset):
        if len(itemset) == 1:
            return []
        combinations = itertools.combinations(itemset, len(itemset) - 1)
        combinations = [list(combination) for combination in combinations]

        rules = []
        for combination in combinations:
            diff = set(itemset) - set(combination)
            rules.append([combination, list(diff)])
            rules.append([list(diff), combination])

        return rules

    def get_frequent_itemsets(self, data):


        itemsets = [[i] for i in data.columns]
        old_itemsets = []
        flag = True

        while flag:
            new_itemsets = []
            for itemset in itemsets:

                if(self.get_support(data,itemset) >= self.support_t):
                    new_itemsets.append(itemset)
                pass

            if len(new_itemsets) != 0:
                old_itemsets = new_itemsets
                itemsets = self.merge_itemsets(new_itemsets)
            else:
                flag = False
                itemsets = old_itemsets

        return itemsets

    def get_confidence(self, data, rule):


        support_X = self.get_support(data, rule[0])
        support_X_y = self.get_support(data, rule[0] + rule[1])

        return support_X_y / support_X

    def get_association_rules(self, data):

        itemsets = self.get_frequent_itemsets(data)
        rules = []
        for itemset in itemsets:

            rules += self.get_rules(itemset)


        association_rules = []
        for rule in rules:

            if self.get_confidence(data, rule) >= self.confidence_t:
                association_rules.append(rule)


        return association_rules
