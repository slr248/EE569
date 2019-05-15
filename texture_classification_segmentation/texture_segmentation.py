import tex_functions as tx
import numpy as np
from tex_functions import get_laws25
from sklearn.cluster import KMeans
import csv
from sklearn.decomposition import PCA

with open('features1.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
#features=[map(int,i) for i in data]
#print(features[0])

features=np.zeros((510*510,25))
for i in range(0,510*510):
    for j in range(0,25):
        features[i][j]=float(data[i][j])

print(features.shape)

layer=np.array([0, 42, 84, 126, 168, 210, 255])

pca=PCA(n_components=3)
pca.fit(features)
feature_pca=pca.fit_transform(features)




kmeans=KMeans(n_clusters=7)
#kmeans.fit(features)
kmeans.fit(feature_pca)
labels=kmeans.labels_
labels=labels.reshape(510,510)
segmented_image=np.zeros((510,510))


for i in range(0,510):
    for j in range(0,510):
        if labels[i][j]==0:
            segmented_image[i][j]=layer[0]
        if labels[i][j]==1:
            segmented_image[i][j]=layer[1]
        if labels[i][j]==2:
            segmented_image[i][j]=layer[2]
        if labels[i][j]==3:
            segmented_image[i][j]=layer[3]
        if labels[i][j]==4:
            segmented_image[i][j]=layer[4]
        if labels[i][j]==5:
            segmented_image[i][j]=layer[5]
        if labels[i][j]==6:
            segmented_image[i][j]=layer[6]


#a=tx.get_image('comb.raw')
#b=tx.extend_boundary2(a,501)
tx.write_file(segmented_image,'segmented_image.raw')
