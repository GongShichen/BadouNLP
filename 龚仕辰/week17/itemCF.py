import math
from collections import defaultdict
from itertools import combinations

class ItemCF:
    def __init__(self):
        self.user_items = defaultdict(set)  
        self.item_users = defaultdict(set)  
        self.cooccur = defaultdict(lambda: defaultdict(float))  
        self.sim_matrix = defaultdict(dict)

    def fit(self, data):
        for user, item in data:
            self.user_items[user].add(item)
            self.item_users[item].add(user)
        
        for user, items in self.user_items.items():
            items = list(items)
            user_len = len(items)
            if user_len < 2:
                continue
            weight = 1.0 / math.log(1 + user_len)
            for i, j in combinations(items, 2):
                self.cooccur[i][j] += weight
                self.cooccur[j][i] += weight
        
        for i in self.item_users:
            for j in self.cooccur[i]:
                denominator = math.sqrt(len(self.item_users[i]) * len(self.item_users[j]))
                if denominator == 0:
                    self.sim_matrix[i][j] = 0
                else:
                    self.sim_matrix[i][j] = self.cooccur[i][j] / denominator

    def recommend(self, user, top_n=10):
        interacted_items = self.user_items.get(user, set())
        if not interacted_items:
            return []
        
        scores = defaultdict(float)
        for item in interacted_items:
            if item not in self.sim_matrix:
                continue
            for related_item, sim in self.sim_matrix[item].items():
                if related_item in interacted_items:
                    continue 
                scores[related_item] += sim
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


if __name__ == "__main__":

    data = [
        ('user1', 'item1'),
        ('user1', 'item2'),
        ('user1', 'item3'),
        ('user2', 'item1'),
        ('user2', 'item4'),
        ('user3', 'item2'),
        ('user3', 'item3'),
        ('user3', 'item4'),
    ]

    model = ItemCF()
    model.fit(data)
    
    print("Recommendations for user1:", model.recommend('user1', top_n=2))
