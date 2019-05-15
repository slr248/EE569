import numpy as np
from numpy.linalg import inv
from matplotlib import pylab as plt
import math
from math import sqrt
A = np.fromfile('classroom.raw', dtype='uint8', sep="")
A = A.reshape([712, 1072])

k1=-0.3536
k2=0.1730
k11=-k1
k22=-3*k1**2-k2
uc=536+0.5
vc=712-356+0.5

op_image=np.array([0 for i in range(0,712*1072)]).reshape(712,1072)



for i in range(0,712):
    for j in range(0,1072):
        camx=(i-356)/600
        camy=(j-536)/600
        #xd=(x-uc)/600
        #yd=(y-vc)/600

        xd=camx*(1+k1*(camx**2+camy**2)+k2*(camx**2+camy**2)**2)
        yd=camy*(1+k1*(camx**2+camy**2)+k2*(camx**2+camy**2)**2)

        #xc=x*(1+k11*(x**2+y**2)+k22*(x**2+y**2)**2)
        #yc=y*(1+k11*(x**2+y**2)+k22*(x**2+y**2)**2)

        xd=600*xd+356
        yd=600*yd+536

        if(0<xd<712 and 0<yd<1072):
            #op_image[int(711-yc+0.5)][int(xc-0.5)]=A[i][j]
            #op_image[i][j]=A[int(711-yc+0.5)][int(xc-0.5)]
            op_image[i][j]=A[int(xd)][int(yd)]
            #op_image[int(xc)][int(yc)]=A[i][j]

op_image=op_image.reshape(1,712*1072)
img = op_image.astype(np.uint8)
img.tofile('corrected_classroom.raw')
