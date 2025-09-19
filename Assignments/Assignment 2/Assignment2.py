import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

def euclideanDistance(p1, p2):
    return np.sqrt(np.sum((p2-p1)**2))

def kMeansClustering(dataset, numOfClusters):
    clusters = {}
    # initialize centroids randomly from the dataset
    centroids = dataset.sample(n=numOfClusters)

    return 0



def main(): 
    # Task 1: Generate a figure fom the given dataset that resembles figure 1
    df = pd.read_csv('spiral-dataset.csv', delimiter='\t', header=None)
    plt.scatter(df[0], df[1], c=df[2])
    plt.show()

    # Task 2: Implement the k-means clustering algorithm. 
    # Choose the Euclidean Distance for calculating distances between data samples

    # Task 2a:
if __name__ == "__main__":
    main()