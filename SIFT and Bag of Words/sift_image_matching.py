#Name : SANIL L REGO
#USC ID: 9233942261
#USC email: srego@usc.edu
#DATE: 03/19/2019


import numpy as np
import cv2
import matplotlib.pyplot as plt
Image_Height=1024
Image_Width=768
img1=np.fromfile('river1.raw',dtype='uint8',sep="").reshape([Image_Height,Image_Width,3])
img2=np.fromfile('river2.raw',dtype='uint8',sep="").reshape([Image_Height,Image_Width,3])
img1=cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
img2=cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
kp1,d1=sift.detectAndCompute(img1,None)
kp2,d2=sift.detectAndCompute(img2,None)

#img=cv2.drawKeypoints(img1,kp1,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#cv2.imwrite('sift_keypoints1_gray.jpg',img)

x=[]
for i in range(0,len(d1)):
    x.append(np.linalg.norm(d1[i]))

print(x.index(max(x)))
print(x[4141])


max_vector=np.array(d1[x.index(max(x))]).reshape(1,128)
#print(x.index(max(x)))
#print(max_vector.shape)

bf = cv2.BFMatcher()
#matches = bf.knnMatch(max_vector,d2,k=2)   #knn
matches = bf.match(d1,d2)




target=[matches[4141]]


img3 = cv2.drawMatches(img1,kp1,img2,kp2,target,None)


plt.imshow(img3),plt.show()



#img=cv2.drawKeypoints(img1,d,img1)#,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#cv2.imwrite('river1_largest.jpg',img)

#######################################
