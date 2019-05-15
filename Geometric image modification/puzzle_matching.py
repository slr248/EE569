import numpy as np
from numpy.linalg import inv
from matplotlib import pylab as plt
import math
from math import floor,ceil

lighthouse1 = np.fromfile('lighthouse1.raw', dtype='uint8', sep="")
lighthouse1 = lighthouse1.reshape([256, 256])

lighthouse2=np.fromfile('lighthouse2.raw',dtype='uint8',sep="")
lighthouse2=lighthouse2.reshape(256,256)

lighthouse3=np.fromfile('lighthouse3.raw',dtype='uint8',sep="")
lighthouse3=lighthouse3.reshape(256,256)

def bilinear(lh,temp,*arg):
    r=255-temp[1]+0.5
    s=temp[0]+0.5
    lh1=(ceil(s)-s)*lh[int(floor(r))][int(floor(s))]+(s-floor(s))*lh[int(floor(r))][int(ceil(s))]
    lh2=(ceil(s)-s)*lh[int(ceil(r))][int(floor(s))]+(s-floor(s))*lh[int(ceil(r))][int(ceil(s))]
    lh3=(ceil(r)-r)*lh1+(r-floor(r))*lh2
    return lh3

def get_cart(array,*args):
    cart=np.zeros((len(array),2))
    for i in range(0,len(array)):
        cart[i][0]=array[i][1]+0.5
        cart[i][1]=255-array[i][0]+0.5
    return cart


def get_corners(lighthouse2,*args):      #returns corners in image coordinates
    row=[]
    col=[]
    center_2=[]
    corners_2=[]
    for i in range(0,256):
        for j in range(0,256):
            if(lighthouse2[i][j]<255):
                row.append(i)
                col.append(j)
    for j in range(0,256):
        if(lighthouse2[min(row)][j]<255):
            corners_2.append([min(row),j])
            break
    for j in range(0,256):
        if(lighthouse2[j][max(col)]<255):
            corners_2.append([j,max(col)])
            break
    for j in range(0,256):
        if(lighthouse2[max(row)][j]<255):
            corners_2.append([max(row),j])
            break
    for j in range(0,256):
        if(lighthouse2[j][min(col)]<255):
            corners_2.append([j,min(col)])
            break
    return corners_2

#print(corner)

def get_center(corner,*args):           #returns center in cartesian coordinates
    center=[(corner[0][0]+corner[2][0])/2,(corner[0][1]+corner[2][1])/2]
    center_c=[center[1]+0.5,255-center[0]+0.5]
    return center_c

#print(center_2)

def get_theta(corner,*args):       #RETURNS ANGLE THETA , PASS: CORNERS IN IMAGE COORDINATES
    y2=256-corner[2][0]+0.5
    y1=256-corner[1][0]+0.5
    x2=corner[2][1]+0.5
    x1=corner[1][1]+0.5
    theta=np.arctan((y2-y1)/(x2-x1))
    return theta

#print(theta2*180/math.pi)

def get_R(theta,center_c):         #RETURNS ROTATION MATRIX :PASS THETA , CENTER(CARTESIAN)
    R=np.array([[np.cos(-theta),-np.sin(-theta),-center_c[0]*np.cos(-theta)+center_c[1]*np.sin(-theta)+center_c[0]],
                [np.sin(-theta),np.cos(-theta),-center_c[0]*np.sin(-theta)-center_c[1]*np.cos(-theta)+center_c[1] ],
                [0,0,1]]).reshape(3,3)
    return R


#print(R2)

def get_inv_S(corner,*args):          #RETURNS INVERSE SCALING MATRIX , PASS CORNERS
    piece_width=round(math.hypot((corner[1][1]-corner[0][1]),(corner[1][0]-corner[0][0])))
    piece_height=round(math.hypot((corner[2][1]-corner[1][1]),(corner[2][0]-corner[1][0])))
    Sx=160/piece_width
    Sy=160/piece_height
    S_inv=np.array([[1/Sx,0,0],[0,1/Sy,0],[0,0,1]]).reshape(3,3)
    return S_inv

def get_T_inv(corner,center,*args):     # RETURNS INVERSE TRANSLATION MATRIX, PASS CORNERS (image coordinates) AND CENTER(cartesian)
    piece_width=round(math.hypot((corner[1][1]-corner[0][1]),(corner[1][0]-corner[0][0])))
    piece_height=round(math.hypot((corner[2][1]-corner[1][1]),(corner[2][0]-corner[1][0])))
    tx=-(center[0]-piece_width/2)
    #tx=-96.5
    ty=-(center[1]-piece_height/2)
    #ty=-50.5
    T_inv=np.array([[1,0,-tx],[0,1,-ty],[0,0,1]]).reshape(3,3)
    return T_inv

#S2_inv=get_inv_S(corner_2)
#print(S2_inv)


#temp=np.matmul(R2,np.array([corner_2_cart[2][0],corner_2_cart[2][1],1]))
#print(temp)
#######LIGHTHOUSE 1##############
corner_1=get_corners(lighthouse1)
center_1=get_center(corner_1)
theta1=get_theta(corner_1)
R1=get_R(theta1,center_1)
T1_inv=get_T_inv(corner_1,center_1)
S1_inv=get_inv_S(corner_1)
corner_1_cart=get_cart(corner_1)
print(theta1*180/math.pi)

###### LIGHTHOUSE 2###########
corner_2=get_corners(lighthouse2)
center_2=get_center(corner_2)
theta2=get_theta(corner_2)+89*math.pi/180
R2=get_R(theta2,center_2)
T2_inv=get_T_inv(corner_2,center_2)
S2_inv=get_inv_S(corner_2)
corner_2_cart=get_cart(corner_2)

######## LIGHTHOUSE 3 ########
corner_3=get_corners(lighthouse3)
center_3=get_center(corner_3)
theta3=get_theta(corner_3)+271*math.pi/180
R3=get_R(theta3,center_3)
T3_inv=get_T_inv(corner_3,center_3)
S3_inv=get_inv_S(corner_3)
corner_3_cart=get_cart(corner_3)

#######################################
#print(corner_2_cart[0])
N=256
LH1=np.array([0 for i in range(0,N*N)]).reshape(N,N)
LH2=np.array([0 for i in range(0,N*N)]).reshape(N,N)
LH3=np.array([0 for i in range(0,N*N)]).reshape(N,N)
for i in range(0,N):
    for j in range(0,N):
        x=j+0.5
        y=N-1-i+0.5
        temp_1=np.matmul(T1_inv,np.array([x,y,1]))
        temp_2=np.matmul(T2_inv,np.array([x,y,1]))
        temp_3=np.matmul(T3_inv,np.array([x,y,1]))
        temp_11=np.matmul(inv(R1),temp_1)
        temp_22=np.matmul(inv(R2),temp_2)
        temp_33=np.matmul(inv(R3),temp_3)
        if(0<=temp_11[0]<=254 and 0<=temp_11[1]<=254):
            #LH1[i][j]=lighthouse1[int(N-1-temp_11[1]+0.5)][int(temp_11[0]-0.5)]
            intensity1=bilinear(lighthouse1,temp_11)
            LH1[i][j]=intensity1
        if(0<temp_22[0]<N and 0<temp_22[1]<N):
            LH2[i][j]=lighthouse2[int(N-1-temp_22[1]+0.5)][int(temp_22[0]-0.5)]
            #intensity2=bilinear(lighthouse2,temp_22)
            #LH2[i][j]=intensity2
        if(2<temp_33[0]<254 and 2<temp_33[1]<254):
            #LH3[i][j]=lighthouse3[int(N-1-temp_33[1]+0.5)][int(temp_33[0]-0.5)]
            intensity3=bilinear(lighthouse3,temp_33)
            LH3[i][j]=intensity3
N=160
LH1_S=np.array([255 for i in range(0,N*N)]).reshape(N,N)
LH2_S=np.array([0 for i in range(0,N*N)]).reshape(N,N)
LH3_S=np.array([0 for i in range(0,N*N)]).reshape(N,N)
for i in range(0,N):
    for j in range(0,N):
        x=j+0.5
        y=N-1-i+0.5
        temp_1=np.matmul(S1_inv,np.array([x,y,1]))
        temp_2=np.matmul(S2_inv,np.array([x,y,1]))
        temp_3=np.matmul(S3_inv,np.array([x,y,1]))
        if(1<=temp_1[0]<256 and 1<temp_1[1]<256):
            #LH1_S[i][j]=LH1[int(255-temp_1[1]+0.5)][int(temp_1[0]-0.5)]
            LH1_S[i][j]=bilinear(LH1,temp_1)
        if(0<=temp_2[0]<256 and 0<temp_2[1]<256):
            LH2_S[i][j]=LH2[int(255-temp_2[1]+0.5)][int(temp_2[0]-0.5)]
            #LH2_S[i][j]=bilinear(LH2,temp_2)
        if(0<=temp_3[0]<256 and 0<temp_3[1]<256):
            #LH3_S[i][j]=LH3[int(255-temp_3[1]+0.5)][int(temp_3[0]-0.5)]
            LH3_S[i][j]=bilinear(LH3,temp_3)

########## COPYING TO LIGHTHOUSE############3
lighthouse=np.fromfile('lighthouse.raw',dtype='uint8',sep="")
lighthouse=lighthouse.reshape(512,512)

LH=lighthouse
for i in range(0,160):
    for j in range(0,160):
        LH[i+157][j+62]=LH1_S[i][j]
        LH[i+31][j+278]=LH2_S[i][j]
        LH[i+328][j+326]=LH3_S[i][j]

print("T1 :"+str(theta1*180/math.pi))
print("T2 :"+str(theta2*180/math.pi))
print("T3 :"+str(theta3*180/math.pi))
#print(center_1)"""
"""LH3=LH3.reshape(N,N)
img = LH3.astype(np.uint8)
img.tofile('LH3_rot.raw')
print(S3_inv)"""
LH=LH.reshape(512,512)
img = LH.astype(np.uint8)
img.tofile('LH.raw')

LH2_S=LH2_S.reshape(N,N)
img = LH2_S.astype(np.uint8)
img.tofile('LH2.raw')

LH3_S=LH3_S.reshape(N,N)
img = LH3_S.astype(np.uint8)
img.tofile('LH3.raw')
