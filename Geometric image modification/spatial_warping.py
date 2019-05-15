import numpy as np
from numpy.linalg import inv
from matplotlib import pylab as plt
import math
A = np.fromfile('hat.raw', dtype='uint8', sep="")
A = A.reshape([512, 512])

###################################LEFT TRIANGLE ######################################
P=[[256,256],[256/2,256/2],[(256+512)/2,256/2],[0,0],[511/2,0],[511,0]]
P_cart=np.zeros((6,2))
for i in range(0,6):
    P_cart[i][0]=P[i][1]+0.5
    P_cart[i][1]=511-P[i][0]+0.5
#print(P_cart)
P5=[256,128]
P5_cart=[128+0.5,511-256+0.5]

#inverse matrix

left=np.array([[1,1,1,1,1,1],
                 [P_cart[0][0],P_cart[1][0],P_cart[2][0],P_cart[3][0],P5_cart[0],P_cart[5][0]],
                 [P_cart[0][1],P_cart[1][1],P_cart[2][1],P_cart[3][1],P5_cart[1],P_cart[5][1]],
                 [P_cart[0][0]**2,P_cart[1][0]**2,P_cart[2][0]**2,P_cart[3][0]**2,P5_cart[0]**2,P_cart[5][0]**2],
                 [P_cart[0][0]*P_cart[0][1],P_cart[1][0]*P_cart[1][1],P_cart[2][0]*P_cart[2][1],P_cart[3][0]*P_cart[3][1],P5_cart[0]*P5_cart[1],P_cart[5][0]*P_cart[5][1]],
                 [P_cart[0][1]**2,P_cart[1][1]**2,P_cart[2][1]**2,P_cart[3][1]**2,P5_cart[1]**2,P_cart[5][1]**2]])
#print(P_cart)
input_left=np.array([[P_cart[0][0],P_cart[1][0],P_cart[2][0],P_cart[3][0],P_cart[4][0],P_cart[5][0]],
        [P_cart[0][1],P_cart[1][1],P_cart[2][1],P_cart[3][1],P_cart[4][1],P_cart[5][1]]])

coeff_left=np.matmul(input_left,inv(left))

############################### TOP TRIANGLE ##################################################################
Q=[P[0],P[1],[256/2,(511+256)/2],P[3],[0,256],[0,511]]
Q_cart=np.zeros((6,2))
for i in range(0,6):
    Q_cart[i][0]=Q[i][1]+0.5
    Q_cart[i][1]=511-Q[i][0]+0.5

Q5=[128,256]
Q5_cart=[256+0.5,511-128+0.5]

top=np.array([[1,1,1,1,1,1],
                 [Q_cart[0][0],Q_cart[1][0],Q_cart[2][0],Q_cart[3][0],Q5_cart[0],Q_cart[5][0]],
                 [Q_cart[0][1],Q_cart[1][1],Q_cart[2][1],Q_cart[3][1],Q5_cart[1],Q_cart[5][1]],
                 [Q_cart[0][0]**2,Q_cart[1][0]**2,Q_cart[2][0]**2,Q_cart[3][0]**2,Q5_cart[0]**2,Q_cart[5][0]**2],
                 [Q_cart[0][0]*Q_cart[0][1],Q_cart[1][0]*Q_cart[1][1],Q_cart[2][0]*Q_cart[2][1],Q_cart[3][0]*Q_cart[3][1],Q5_cart[0]*Q5_cart[1],Q_cart[5][0]*Q_cart[5][1]],
                 [Q_cart[0][1]**2,Q_cart[1][1]**2,Q_cart[2][1]**2,Q_cart[3][1]**2,Q5_cart[1]**2,Q_cart[5][1]**2]])

input_top=np.array([[Q_cart[0][0],Q_cart[1][0],Q_cart[2][0],Q_cart[3][0],Q_cart[4][0],Q_cart[5][0]],
        [Q_cart[0][1],Q_cart[1][1],Q_cart[2][1],Q_cart[3][1],Q_cart[4][1],Q_cart[5][1]]])

coeff_top=np.matmul(input_top,inv(top))

################################# RIGHT TRIANGLE #######################
R=[P[0],[(256+511)/2,(256+511)/2],Q[2],[511,511],[256,511],[0,511]]
R_cart=np.zeros((6,2))
for i in range(0,6):
    R_cart[i][0]=R[i][1]+0.5
    R_cart[i][1]=511-R[i][0]+0.5

R5=[256,384]
R5_cart=[384+0.5,511-256+0.5]

right=np.array([[1,1,1,1,1,1],
                 [R_cart[0][0],R_cart[1][0],R_cart[2][0],R_cart[3][0],R5_cart[0],R_cart[5][0]],
                 [R_cart[0][1],R_cart[1][1],R_cart[2][1],R_cart[3][1],R5_cart[1],R_cart[5][1]],
                 [R_cart[0][0]**2,R_cart[1][0]**2,R_cart[2][0]**2,R_cart[3][0]**2,R5_cart[0]**2,R_cart[5][0]**2],
                 [R_cart[0][0]*R_cart[0][1],R_cart[1][0]*R_cart[1][1],R_cart[2][0]*R_cart[2][1],R_cart[3][0]*R_cart[3][1],R5_cart[0]*R5_cart[1],R_cart[5][0]*R_cart[5][1]],
                 [R_cart[0][1]**2,R_cart[1][1]**2,R_cart[2][1]**2,R_cart[3][1]**2,R5_cart[1]**2,R_cart[5][1]**2]])

input_right=np.array([[R_cart[0][0],R_cart[1][0],R_cart[2][0],R_cart[3][0],R_cart[4][0],R_cart[5][0]],
        [R_cart[0][1],R_cart[1][1],R_cart[2][1],R_cart[3][1],R_cart[4][1],R_cart[5][1]]])

coeff_right=np.matmul(input_right,inv(right))

######################## BOTTOM ###############################
S=[P[0],[(256+511)/2,256/2],[(256+511)/2,(256+511)/2],[511,0],[511,256],[511,511]]

S_cart=np.zeros((6,2))
for i in range(0,6):
    S_cart[i][0]=S[i][1]+0.5
    S_cart[i][1]=511-S[i][0]+0.5

S5=[384,256]
S5_cart=[256+0.5,511-384+0.5]

bottom=np.array([[1,1,1,1,1,1],
                 [S_cart[0][0],S_cart[1][0],S_cart[2][0],S_cart[3][0],S5_cart[0],S_cart[5][0]],
                 [S_cart[0][1],S_cart[1][1],S_cart[2][1],S_cart[3][1],S5_cart[1],S_cart[5][1]],
                 [S_cart[0][0]**2,S_cart[1][0]**2,S_cart[2][0]**2,S_cart[3][0]**2,S5_cart[0]**2,S_cart[5][0]**2],
                 [S_cart[0][0]*S_cart[0][1],S_cart[1][0]*S_cart[1][1],S_cart[2][0]*S_cart[2][1],S_cart[3][0]*S_cart[3][1],S5_cart[0]*S5_cart[1],S_cart[5][0]*S_cart[5][1]],
                 [S_cart[0][1]**2,S_cart[1][1]**2,S_cart[2][1]**2,S_cart[3][1]**2,S5_cart[1]**2,S_cart[5][1]**2]])

input_bottom=np.array([[S_cart[0][0],S_cart[1][0],S_cart[2][0],S_cart[3][0],S_cart[4][0],S_cart[5][0]],
        [S_cart[0][1],S_cart[1][1],S_cart[2][1],S_cart[3][1],S_cart[4][1],S_cart[5][1]]])

coeff_bottom=np.matmul(input_bottom,inv(bottom))





#print(coeff)

#temp_xy=[1,P5_cart[0],P5_cart[1],P5_cart[0]**2,P5_cart[0]*P5_cart[1],P5_cart[1]**2]

#print(np.matmul(coeff,temp_xy))

###### LEFT TRIANGLE CHECK #####
op_image=np.array([0 for i in range(0,512*512)]).reshape(512,512)
for i in range(0,512):
    for j in range(0,512):
        x=j+0.5
        y=511-i+0.5
        if(x<-y+511.5 and y>x):
            temp=np.matmul(coeff_left,np.array([1,x,y,x**2,x*y,y**2]))
            if(0<temp[0]<512 and 0<temp[1]<512):
                op_image[i][j]=A[int(511-temp[1]+0.5)][int(temp[0]-0.5)]
        if(x>-y+511.5 and y>x):
            temp=np.matmul(coeff_top,np.array([1,x,y,x**2,x*y,y**2]))
            if(0<temp[0]<512 and 0<temp[1]<512):
                op_image[i][j]=A[int(511-temp[1]+0.5)][int(temp[0]-0.5)]
        if(x>-y+511.5 and y<x):
            temp=np.matmul(coeff_right,np.array([1,x,y,x**2,x*y,y**2]))
            if(0<temp[0]<512 and 0<temp[1]<512):
                op_image[i][j]=A[int(511-temp[1]+0.5)][int(temp[0]-0.5)]
        if(x<-y+511.5 and y<x):
            temp=np.matmul(coeff_bottom,np.array([1,x,y,x**2,x*y,y**2]))
            if(0<temp[0]<512 and 0<temp[1]<512):
                op_image[i][j]=A[int(511-temp[1]+0.5)][int(temp[0]-0.5)]


#x=0.5
#y=511.5
#temp_xy=np.array([1,x,y,x**2,x*y,y**2])
#print(np.matmul(coeff,temp_xy))
count=0;
for i in range(0,512):
    for j in range(511,-1,-1):
        op_image[i][j-count]=op_image[i][j-1-count]
        count+=1
        break


op_image=op_image.reshape(1,512*512)
img = op_image.astype(np.uint8)
img.tofile('warped_triangle.raw')
