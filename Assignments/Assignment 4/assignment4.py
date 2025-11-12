import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy.cluster.hierarchy import dendrogram
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import pdist

# --------------------
# Distance Calculation
# --------------------
def euclideanDistance(p1, p2):
    return np.sqrt(np.sum((p2-p1)**2))

# ---------------
# SSE Calculation
# ---------------
def sumOfSquaredErrors(dataset, clusters):
    sse = 0
    points = dataset.iloc[:, 0:2].to_numpy()

    for cluster in clusters:
        cluster_points = points[cluster]
        centroid = np.mean(cluster_points, axis=0)
        for point in cluster_points:
            d = euclideanDistance(centroid, point)
            sse += d ** 2
    return sse

# ---------------
# RI Calculation
# ---------------
def randIndex(dataset, clusters):
    TP, TN, FP, FN = 0, 0, 0, 0
    
    points = dataset.iloc[:, 2].to_numpy()
    cluster_labels = np.zeros(len(dataset), dtype = int)
    for i, cluster in enumerate(clusters):
        for j in cluster:
            cluster_labels[j] = i

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            # True positive check
            if (points[i] == points[j]) & (cluster_labels[i] == cluster_labels[j]):
                TP += 1
            # True negative check
            elif (points[i] != points[j]) & (cluster_labels[i] != cluster_labels[j]):
                TN += 1
            # False positive check
            elif (points[i] != points[j]) & (cluster_labels[i] == cluster_labels[j]):
                FP += 1
            # False negative check
            elif (points[i] == points[j]) & (cluster_labels[i] != cluster_labels[j]):
                FN += 1

    RI = (TP + TN)/(TP + TN + FP + FN)
    return RI

# ---------------
# CCC Calculation
# ---------------
def copheneticCorrelationCoefficient(points, merge_history):
    n = len(points)
    # Original pairwise distances
    dists = pdist(points)

    # distances from dendrogram
    ccc_matrix = np.zeros((n, n))
    cluster_points = {i: [i] for i in range(n)}
    for i, j, dist in merge_history:
        members_i = cluster_points.pop(i, [])
        members_j = cluster_points.pop(j, [])
        merged = members_i + members_j
        for p in members_i:
            for q in members_j:
                ccc_matrix[p, q] = dist
                ccc_matrix[q, p] = dist
        new_index = max(cluster_points.keys(), default=-1) + 1
        cluster_points[new_index] = merged

    # Flatten upper triangle
    ccc_flat = ccc_matrix[np.triu_indices(n, k=1)]

    # Compute Pearson correlation
    return np.corrcoef(dists, ccc_flat)[0, 1]

# ---------------------------------------------------
# Create linkage matrix for Scipy dendrogram function
# ---------------------------------------------------
def linkage_matrix(merge_history, n):
    Z = []
    
    # Track cluster sizes
    cluster_sizes = {i: 1 for i in range(n)}
    next_id = n
    
    for i_old, j_old, dist in merge_history:
        # current sizes of clusters
        size_i = cluster_sizes[i_old]
        size_j = cluster_sizes[j_old]
        size_new = size_i + size_j
        
        # Add to linkage matrix
        Z.append([i_old, j_old, dist, size_new])
        
        # Update cluster sizes
        # new cluster gets next_id
        cluster_sizes[next_id] = size_new
        del cluster_sizes[i_old]
        del cluster_sizes[j_old]
        
        next_id += 1
    
    return np.array(Z)


# ------------
# Plot dataset
# ------------
def plotClusters(dataset, clusters):
    colors = ['red', 'green', 'blue']
    plt.figure(figsize=(6, 5))

    for i, cluster in enumerate(clusters):
        points = dataset.iloc[cluster, 0:2].to_numpy()
        plt.scatter(points[:, 0], points[:, 1], s=20, color=colors[i], label=f'Cluster {i+1}')

    plt.title("Hierarchical Clustering")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

# --------------------
# Clustering Algorithm
# --------------------
def hierarchicalClustering(dataset, linkage, target_clusters = 3):
    points = dataset.iloc[:, 0:2].to_numpy()
    n = len(points)

    # Each point is a clusters + global IDs for dendrogram
    clusters = {i: [i] for i in range(n)}
    next_id = n
    merge_history = []

    # We merge down to a single cluster for compatability with scipy dendrogram
    while len(clusters) > 1:
        keys = list(clusters.keys())
        min_val = np.inf
        i_min = j_min = None

        # linkage step
        for x, i in enumerate(keys):
            for y, j in enumerate(keys):
                if x >= y: # reduce number of calcuations (avoid repeats)
                    continue

                # single linkage
                if linkage == 0:
                    distance = min([euclideanDistance(points[p1], points[p2])
                                for p1, p2 in itertools.product(clusters[i], clusters[j])])

                # complete linkage
                elif linkage == 1:
                    distance = max([euclideanDistance(points[p1], points[p2])
                                for p1, p2 in itertools.product(clusters[i], clusters[j])])
                    
                # average linkage
                elif linkage == 2:
                    distance = np.mean([euclideanDistance(points[p1], points[p2])
                                for p1, p2 in itertools.product(clusters[i], clusters[j])])

                # centroid linkage
                elif linkage == 3:
                    centroid1 = np.mean(points[clusters[i]], axis = 0)
                    centroid2 = np.mean(points[clusters[j]], axis = 0)
                    distance = euclideanDistance(centroid1, centroid2)
                    

                if distance < min_val: # find min val for merge step
                    min_val = distance
                    i_min, j_min = i, j

        # Merge step
        new_cluster = clusters[i_min] + clusters[j_min]
        clusters[next_id] = new_cluster
        merge_history.append((i_min, j_min, min_val))
        del clusters[i_min], clusters[j_min]
        next_id += 1

        # snapshot of clusters when reaching 3 clusters
        # This is done because the dendrogram function requires the algorithm to merge down
        # To a single cluster in order to properly function
        if len(clusters) == target_clusters:
            final_clusters = list(clusters.values())
            final_labels = np.zeros(n, dtype=int)
            for i, cluster in enumerate(final_clusters):
                for point in cluster:
                    final_labels[point] = i

    return final_clusters, merge_history, final_labels


def main():

    df = pd.read_csv('spiral-dataset.csv', delimiter='\t', header=None)
    points = df.iloc[:, 0:2].to_numpy()
    n = len(df)
    
    print("Select linkage type: ")
    print("0: Single \n" \
          "1: Complete \n" \
          "2: Average \n" \
          "3: Centroid")
    selection = int(input())

    if selection not in [0, 1, 2, 3]:
        print("Non-valid linkage type")
        return

    # Run clustering algorithm
    clusters, merge_history, cluster_labels = hierarchicalClustering(df, selection)

    # Compute metrics
    sse = sumOfSquaredErrors(df, clusters)
    ri = randIndex(df, clusters)
    ccc = copheneticCorrelationCoefficient(points, merge_history)
    sc = silhouette_score(points, cluster_labels)

    # Build linkage matrix for Scipy dendrogram
    Z = linkage_matrix(merge_history, n)

    # Plot dendrogram
    plt.figure(figsize=(12, 6))
    dendrogram(Z, no_labels=True)
    plt.xlabel("Data Points")
    plt.ylabel("Distance")
    plt.title("Hierarchical Clustering Dendrogram")
    plt.show()

    # Plot the clusters
    plotClusters(df, clusters)
    
    # Print metrics
    print(f"SSE: {sse:.4f}")
    print(f"Rand Index: {ri:.4f}")
    print(f"Cophenetic Correlation Coefficient: {ccc:.4f}")
    print(f"Silhouette Score: {sc:.4f}")

if __name__ == '__main__':
    main()