# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2




# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
image = cv2.imread('C:\Users\kjahn\Desktop\python imaging\python-kmeans-dominant-colors\images\batman.png') #insert file path here
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imshow('image',image)

# show our image
plt.figure()
plt.axis("off")
plt.imshow(image)

# reshape the image to be a list of pixels
image = image.reshape((image.shape[0] * image.shape[1], 3))

# cluster the pixel intensities
clt = KMeans(n_clusters = 3) #add number of clusters here
clt.fit(image)

# build a histogram of clusters and then create a figure
# representing the number of pixels labeled to each color
hist = utils.centroid_histogram(clt)
bar = utils.plot_colors(hist, clt.cluster_centers_)

# show our color bart
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()
