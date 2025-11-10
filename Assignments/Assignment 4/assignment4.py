import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap

def euclideanDistance(p1, p2):
    return np.sqrt(np.sum((p2-p1)**2))

def sumOfSquaredErrors(dataset, centroids, closest_centroid):
    sse = 0
    points = dataset.iloc[:, 0:2].to_numpy()

    for k in range(len(centroids)):
        for i in range(len(points)):
            if closest_centroid[i] == k:
                d = euclideanDistance(points[i], centroids[k])
                se = d**2
                sse += se
    return sse

def randIndex(dataset, closest_centroid):
    TP, TN, FP, FN = 0, 0, 0, 0
    points = dataset.to_numpy()
    for i in range(len(points)):
        for j in range(len(closest_centroid)):
            # Can't compare a point to itself
            if i == j:
                continue
            # True positive check
            if (points[i][2] == points[j][2]) & (closest_centroid[i] == closest_centroid[j]):
                TP += 1
            # True negative check
            elif (points[i][2] != points[j][2]) & (closest_centroid[i] != closest_centroid[j]):
                TN += 1
            # False positive check
            elif (points[i][2] != points[j][2]) & (closest_centroid[i] == closest_centroid[j]):
                FP += 1
            # False negative check
            elif (points[i][2] == points[j][2]) & (closest_centroid[i] != closest_centroid[j]):
                FN += 1

    RI = (TP + TN)/(TP + TN + FP + FN)
    return RI

def hierarchicalClustering(dataset, linkage):

    n = len(dataset)
    prox_matrix = np.zeros((n,n))
    # first proximity matrix (nxn)
    for i in range(n):
        p1 = dataset.iloc[i, 0:2].to_numpy()
        for j in range(n):
            p2 = dataset.iloc[j, 0:2].to_numpy()
            prox_matrix[i, j] = euclideanDistance(p1, p2)

    while n > 1:
        # n rows in prox matrix
        clusters = []
        for row in prox_matrix:
            irow = 0
            min_val = np.min(row[np.nonzero(row)])
            min_val_index = np.where(row == min_val)[0][0]
            clusters.append([irow, min_val_index])
            irow += 1

        # recompute proximity matrix
        n = len(clusters)
        prox_matrix = np.zeros((n,n))

        # single linkage
        if linkage == 0:
            clusters_arr = np.array(clusters)
            clusters_arr_flat = np.array(clusters).flatten()
            for i in clusters_arr_flat:
                p1 = dataset.iloc[i, 0:2].to_numpy()
                for j in clusters_arr:
                    row_i, column_i = np.where(clusters_arr == i)
                    row_j, column_j = np.where(clusters_arr == j)
                    if row_i[0] == row_j[0]:
                        return
                    p2 = dataset.iloc[j, 0:2].to_numpy()
                    distance = euclideanDistance(p1, p2)


            # for i in clusters:
            #     min_val = 0
            #     p1 = dataset.iloc[i, 0:2].to_numpy()
            #     for j in clusters:
            #         p1 = dataset.iloc[j, 0:2].to_numpy()
            #         distance = euclideanDistance(p1, p2)
            #         if distance < min_val:
            #             min_val = distance
            return
        # complete linkage
        elif linkage == 1:
            return
        # average linkage
        elif linkage == 2:
            return
        # centroid linkage
        elif linkage == 3:
            return

    return prox_matrix


def main():

    # df = pd.read_csv('spiral-dataset.csv', delimiter='\t', header=None)
    # prox_matrix = hierarchicalClustering(df)
    # for row in prox_matrix:
    #     print(row.dtype)

    arr_2d = np.array([[0, 3, 2],
                       [4, 0, 6],
                       [7, 8, 0]])
    
    for i in arr_2d.flatten():
        print(i)

    
    

if __name__ == '__main__':
    main()