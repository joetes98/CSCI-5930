import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

def euclideanDistance(p1, p2):
    return np.sqrt(np.sum((p2-p1)**2))

def kMeansClustering(dataset, numOfClusters):
    # initialize centroids randomly from the dataset
    centroids = dataset.sample(n=numOfClusters)
    clusters = {key: None for key in centroids.index}

    while True:
        distances = {}
        for i in range(len(dataset)):
            distances[i] = []
            # x,y for point 1
            p1 = dataset.iloc[i, 0:2]
            for j in centroids.index:
                # x,y for point 2
                p2 = centroids.loc[j, 0:2]
                # compute euclidean distance between point and centroid
                distances[i].append(euclideanDistance(p2, p1))
            # assign datapoint to closest centroid
            clusters[i] = min(distances)
            
            




                       



def main(): 
    # Task 1: Generate a figure fom the given dataset that resembles figure 1
    df = pd.read_csv('spiral-dataset.csv', delimiter='\t', header=None)
    # plt.scatter(df[0], df[1], c=df[2])
    # plt.show()

    distances = {}
    for i in range(10):
        distances[i] = []
    print(distances)


    # Task 2: Implement the k-means clustering algorithm. 
    # Choose the Euclidean Distance for calculating distances between data samples

    # Task 2a:
if __name__ == "__main__":
    main()