from sklearn import cluster
from matplotlib import pyplot
import numpy as np
import pandas as pd

data = np.genfromtxt('sales-all-counties.csv', delimiter=',')
# data = pd.read_csv("zillow-data.csv")

k = 7
kmeans = cluster.KMeans(n_clusters=k)
kmeans.fit(data)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

for i in range(k):
    # select only data observations with cluster label == i
    ds = data[np.where(labels==i)]
    # plot the data observations
    pyplot.plot(ds[:,10],ds[:,17],'o')
    # print(ds[:,2])
    # plot the centroids
    lines = pyplot.plot(centroids[i,1],centroids[i,2],'kx')
    # make the centroid x's bigger
    pyplot.setp(lines,ms=15.0)
    pyplot.setp(lines,mew=2.0)
pyplot.show()
