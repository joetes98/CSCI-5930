import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap


def euclideanDistance(p1, p2):
    return np.sqrt(np.sum((p2-p1)**2))

def cosineSimilarity(p1, p2):
    dot_product = np.dot(p1, p2)
    lengthp1 = np.linalg.norm(p1)
    lengthp2 = np.linalg.norm(p2)
    cosine_similarity = dot_product/(lengthp1*lengthp2)

    return cosine_similarity

def L3Distance(p1, p2):
    return np.sum(np.abs(p2 - p1)**3)**(1/3)

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


def kMeansClustering(dataset, numOfClusters, distance_func = None, nIterations=500, convergenceThreshold=1e-3):
    """
    1. Randomly choose three centroids
    2. For each point in the dataset, compute the euclidean distance to each centroid
    3. For each set of distances, compute the min, assign that point to cluster of that centroid
    4. For each cluster, recompute the centroid by taking the avg of all points in that cluster
        Repeat until centroids do not change   
    """
    # default to euclidean distance if type is not specified
    if distance_func == None:
        distance_func = euclideanDistance 

    # initialize centroids randomly from the dataset
    centroids = dataset.sample(n=numOfClusters).iloc[:, 0:2].to_numpy()

    for i in range(nIterations):
        closest_centroid = []
        for j in range(len(dataset)):
            # x,y for dataset point
            p = dataset.iloc[j, 0:2].to_numpy()
            # compute distance to each centroid
            d = [distance_func(p, centroid) for centroid in centroids]
            # assign datapoint to closest centroid
            if distance_func == euclideanDistance or distance_func == L3Distance:
                closest_centroid.append(np.argmin(d))
            else:
                closest_centroid.append(np.argmax(d))

        closest_centroid = np.array(closest_centroid)

        # recompute centroids
        new_centroids = []
        for k in range(numOfClusters):
            # find all points in cluster k
            points = dataset.iloc[:, 0:2].to_numpy()[closest_centroid == k]
            new_centroids.append(points.mean(axis=0))
        new_centroids = np.array(new_centroids)
            
        # convergence check
        if np.allclose(new_centroids, centroids, atol=convergenceThreshold):
            break
        centroids = new_centroids
    
    # returns the final centroids and the centroid each point was assigned to
    return centroids, closest_centroid


def main():

    df = pd.read_csv('spiral-dataset.csv', delimiter='\t', header=None)
    rgb_map = ListedColormap(['red', 'blue', 'green'])

    # centroids and clusters
    tenRunAssignments = []
    # SSE and RI
    tenRunMetrics = []

    while True:
        print("Select an option: \n" \
            "1. Task 1: Generate a figure fom the given dataset \n" \
            "2. Task 2: Run k-means clustering algorithm. Output SSE and RI for a single run and average over 10 runs \n" \
            "3. Task 3: Graphs for clustering results for task 2 \n" \
            "4. Task 4: Cosine similarity \n" \
            "5. Task 5: L3 distance \n" \
            "6. Exit")
        
        selection = int(input())
        if selection == 1:
            # Task 1: Generate a figure fom the given dataset that resembles figure 1
            plt.scatter(df[0], df[1], c=df[2], cmap = rgb_map)
            plt.show()
            
        elif selection == 2:
            # Task 2a: Run k-means clustering algorithm w/ k=3
            # Task 2b: Compute and output the SSE and RI for a single run
            # Task 2c: Repeat task another nine times. Output the best SSE & best RI
            tenRunAssignments.clear()
            tenRunMetrics.clear()

            for i in range(10):
                centroids, results = kMeansClustering(df, 3, euclideanDistance)
                SSE = sumOfSquaredErrors(df, centroids, results)
                RI = randIndex(df, results)

                tenRunAssignments.append((centroids, results))
                tenRunMetrics.append([SSE, RI])
                
                # Output SSE and RI for first run
                if i == 0:
                    print(f"Single Run Metrics - SSE: {SSE}, RI: {RI}")
                
            tenRunMetrics = np.array(tenRunMetrics)
            bestSSE = tenRunMetrics[:, 0].min()
            bestRI = tenRunMetrics[:, 1].max()

            # Output best SSE and best RI
            print(f"Best SSE over 10 runs: {bestSSE}")
            print(f"Best RI over 10 runs: {bestRI}")

        elif selection == 3:
            # Task 3: Plot clustering results for all 10 runs from task 2
            if not tenRunAssignments:
                print("Run task 2 to generate clusters")
                continue

            fig, axes = plt.subplots(2, 5, figsize=(20, 8))
            axes = axes.flatten()
            plt.suptitle("K Means Clustering using Euclidean Distance")

            for i, (centroids, results) in enumerate(tenRunAssignments):
                ax = axes[i]
                # plot points and color code based on cluster
                ax.scatter(df[0], df[1], c=results, cmap = rgb_map, s=50)
                # show the centroid of each cluster
                ax.scatter(centroids[:, 0], centroids[:, 1], c='orange', marker='+', s=150)
                ax.set_title(f'Run {i + 1}')
            
            plt.tight_layout()
            plt.show()
        
        elif selection == 4:
            # Task 4: Run k means clustering using cosine similarity
            cosineAssignments = []
            cosineMetrics = []
            for i in range(10):
                centroids, results = kMeansClustering(df, 3, cosineSimilarity)
                SSE = sumOfSquaredErrors(df, centroids, results)
                RI = randIndex(df, results)
                cosineAssignments.append((centroids, results))
                cosineMetrics.append([SSE, RI])

            cosineMetrics = np.array(cosineMetrics)
            bestSSE = cosineMetrics[:, 0].min()
            bestRI = cosineMetrics[:, 1].max()

            # Output the best SSE and RI for cosine similarity
            print(f"Best SSE over 10 runs: {bestSSE}")
            print(f"Best RI over 10 runs: {bestRI}")


            # Plot all 10 runs for cosine similarity
            fig, axes = plt.subplots(2, 5, figsize=(20, 8))
            axes = axes.flatten()
            plt.suptitle("K Means Clustering using Cosine Similarity")

            for i, (centroids, results) in enumerate(cosineAssignments):
                ax = axes[i]
                # plot points and color code based on cluster
                ax.scatter(df[0], df[1], c=results, cmap = rgb_map, s=50)
                # show the centroid of each cluster
                ax.scatter(centroids[:, 0], centroids[:, 1], c='orange', marker='+', s=150)
                ax.set_title(f'Run {i + 1}')
            
            plt.tight_layout()
            plt.show()


        elif selection == 5:
            # Task 4: Run k means clustering using L3 Distance
            L3Assignments = []
            L3Metrics = []
            for i in range(10):
                centroids, results = kMeansClustering(df, 3, L3Distance)
                SSE = sumOfSquaredErrors(df, centroids, results)
                RI = randIndex(df, results)
                L3Assignments.append((centroids, results))
                L3Metrics.append([SSE, RI])

            L3Metrics = np.array(L3Metrics)
            bestSSE = L3Metrics[:, 0].min()
            bestRI = L3Metrics[:, 1].max()

            # Output the best SSE and RI for L3 Distance
            print(f"Best SSE over 10 runs: {bestSSE}")
            print(f"Best RI over 10 runs: {bestRI}")


            # Plot all 10 runs for L3 Distance
            fig, axes = plt.subplots(2, 5, figsize=(20, 8))
            axes = axes.flatten()
            plt.suptitle("K Means Clustering using L3 Distance")

            for i, (centroids, results) in enumerate(L3Assignments):
                ax = axes[i]
                # plot points and color code based on cluster
                ax.scatter(df[0], df[1], c=results, cmap = rgb_map, s=50)
                # show the centroid of each cluster
                ax.scatter(centroids[:, 0], centroids[:, 1], c='orange', marker='+', s=150)
                ax.set_title(f'Run {i + 1}')
            
            plt.tight_layout()
            plt.show()

        elif selection == 6:
            break
    
if __name__ == "__main__":
    main()