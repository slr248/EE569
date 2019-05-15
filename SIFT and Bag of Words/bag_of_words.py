import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


Image_Height=28
Image_Width=28

def get_image(name):
    image= np.fromfile(str(name), dtype='uint8', sep="")
    image=image.reshape([28, 28])
    img_resized=cv2.resize(image,(56,56))
    return img_resized


zero1=get_image('zero_1.raw')
zero2=get_image('zero_2.raw')
zero3=get_image('zero_3.raw')
zero4=get_image('zero_4.raw')
zero5=get_image('zero_5.raw')

one1=get_image('one_1.raw')
one2=get_image('one_2.raw')
one3=get_image('one_3.raw')
one4=get_image('one_4.raw')
one5=get_image('one_5.raw')

img_array=[zero1,zero2,zero3,zero4,zero5,one1,one2,one3,one4,one5]



sift = cv2.xfeatures2d.SIFT_create()




des=[]
for i in img_array:
    kp,d=sift.detectAndCompute(i,None)
    des.append(d)
print(len(des[1]))
new_des=[]
count=0
for i in des:
    for j in range(0,len(i)):
        new_des.append(des[count][j])
    count+=1

new_des=np.array(new_des)
print(new_des.shape)

kmeans=KMeans(n_clusters=2)
kmeans.fit(new_des)
labels=kmeans.predict(new_des)
centroids=kmeans.cluster_centers_

eight=get_image('eight.raw')


kp8,d8=sift.detectAndCompute(eight,None)

vocab_list=[]
#print(len(centroids[1]))
for i in d8:
    if np.linalg.norm(i-centroids[1]) > np.linalg.norm(i-centroids[0]):
        vocab_list.append('zero')
    else:
        vocab_list.append('one')
print(vocab_list)

frequency_0=0
frequency_1=0

for i in vocab_list:
    if i=='zero':
        frequency_0+=1
    else:
        frequency_1+=1


#img=cv2.drawKeypoints(one1,kp8,eight,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#cv2.imwrite('one_KP.jpg',img)




plt.hist(vocab_list)
plt.xlabel('codebook (centroid)')
plt.ylabel('frequency')
plt.title('bag of words histogram')
plt.show()
