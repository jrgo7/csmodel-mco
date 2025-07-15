import numpy as np
import pandas as pd

class KMeans:

    def __init__(self, k, num_observations, data):
        self.k = k
        self.num_observations = num_observations
        self.setified_data = data.agg(set, axis=1)
        self.centroids = []
            
    def setify_data(self, data):
        return data.agg(set, axis=1)

    def initialize_centroids(self):

        index = np.random.randint(low=0, high=self.num_observations)
        self.centroids.append(self.setified_data.iloc[index])

        for i in range(1, self.k):

            distances_df = pd.DataFrame()
            
            for j in range(len(self.centroids)):
               distance_col = self.get_jaccard_distance(self.setified_data, self.centroids[j]).to_frame().T
               distances_df = pd.concat([distances_df, distance_col])
            
            index = distances_df.min().idxmax()

            self.centroids.append(self.setified_data[index])

        return self.centroids

    def get_jaccard_distance(self, point1, point2):
        jaccard_distance = lambda point1, point2: 1 - ( len(point1.intersection(point2)) / ( 12 - len(point1.intersection(point2)) ) )
    
        if isinstance(point1, set) and isinstance(point2, set):
            return jaccard_distance(point1,point2)
        else:
            return point1.apply(lambda x: jaccard_distance(x,point2))
            

    def group_observations(self):

        distances = pd.DataFrame()

        for i in range(self.k):
            distances[i] = self.get_jaccard_distance(self.setified_data, self.centroids[i])
        
        groups = distances.idxmin(axis=1)

        return groups

    def adjust_centroids(self, data, groups):

        centroids = []
        for x in range(self.k):
            distances = []

            filtered_dataset = data[groups == x]
            grouped_dataset = self.setify_data(filtered_dataset)


            for index, row1 in grouped_dataset.items():
                sum = 0
                for index, row2 in grouped_dataset.items():
                    sum += self.get_jaccard_distance(row1, row2)
                distances.append(sum)

            distances = pd.Series(distances, index=grouped_dataset.index)
            new_centroid = grouped_dataset.loc[distances.idxmin()]

            centroids.append(new_centroid)
            
        return centroids

    def WCSS(self, data, groups):
        total_sum = 0
        for x in range(self.k):
            sum = 0
            filtered_dataset = data[groups == x]
            grouped_dataset = self.setify_data(filtered_dataset)

            for index, row in grouped_dataset.items():
                sum += (self.get_jaccard_distance(self.centroids[x], row))
            total_sum += sum
        return total_sum
            
    def train(self, data, iters):
        self.initialize_centroids()

        cur_groups = pd.Series(-1, index=[i for i in range(self.num_observations)])
        i = 0
        flag_groups = False
        flag_centroids = False

        while i < iters and not flag_groups and not flag_centroids:

            groups = self.group_observations()

            centroids = self.adjust_centroids(data, groups)

            if cur_groups.equals(groups):
                flag_groups = True
            
            if centroids == self.centroids:
                flag_centroids = True

            cur_groups = groups
            self.centroids = centroids

            i += 1
            print('Iteration', i)

        print('Done clustering!')
        return cur_groups
