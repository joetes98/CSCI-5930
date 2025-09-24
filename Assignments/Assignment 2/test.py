import pandas as pd

def kMeansClustering(dataset, numOfClusters):
    """
    1. Randomly choose three centroids
    2. For each point in the dataset, compute the euclidean distance to each centroid
    3. For each set of distances, compute the min, assign that point to cluster of that centroid
    4. For each cluster, recompute the centroid by taking the avg of all points in that cluster
        Repeat until centroids do not change
    
    """
    # initialize centroids randomly from the dataset
    centroids = dataset.sample(n=numOfClusters)
    clusters = pd.DataFrame({
        'Centroid': [index for index in centroids.index],
        'Points': [[] for _ in range(numOfClusters)]
    })

    while True:

        for i in range(len(dataset)):
            d = pd.DataFrame(columns=['Centroid', 'Distance'])
            # x,y for point 1
            p1 = dataset.iloc[i, 0:2]
            for j in centroids.index:
                # x,y for point 2
                p2 = centroids.loc[j, 0:2]
                # compute euclidean distance between point and centroid
                d.loc[len(d)] = [j, euclideanDistance(p1, p2)]
            # assign datapoint to closest centroid
            min_index = d['Distance'].idxmin()
            closest_centroid = d.loc[min_index, 'Centroid']
            clusters.at(closest_centroid, 'Points').append(i)

        # recompute centroids
        new_centroids = pd.DataFrame()
        for i in range(len(clusters)):
            indices = clusters['Points'][i]
            points = clusters.iloc[indices, 0:2]
            average = points.mean(axis=0)
            for j in range(indices):
                distances = []
                distance = euclideanDistance(j, average)
                distances.append(distance)
            new_centroid = min(distances)
            new_centroids = new_centroids.loc[len(new_centroids)] = new_centroid
        
        if new_centroids.equals(centroids):
            break
        else:
            centroids = new_centroids
            clusters['Points'] = [[] for _ in range(numOfClusters)]