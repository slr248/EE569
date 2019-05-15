import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from itertools import permutations
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def extend_boundary(matrix,*args):
    ext_matrix=np.zeros((len(matrix),len(matrix)))
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix)):
            ext_matrix[i+2][j+2]=matrix[i][j]
            ext_matrix[1,2:len(matrix)+2],ext_matrix[0,2:len(matrix)+2]=matrix[0,:],matrix[1,:]   #top
            ext_matrix[2:len(matrix)+2,1],ext_matrix[2:len(matrix)+2,0]=matrix[:,0],matrix[:,1]   #left
            ext_matrix[2:len(matrix)+2,len(matrix)+3],ext_matrix[2:len(matrix)+2,len(matrix)+2]=matrix[:,len(matrix)-2],matrix[:,len(matrix)-1]   #right
            ext_matrix[len(matrix)+3,2:len(matrix)+2],ext_matrix[len(matrix)+2,2:len(matrix)+2]=matrix[len(matrix)-2,:],matrix[len(matrix)-1,:]   #bottom
    ext_matrix[:2,:2],ext_matrix[:2,len(matrix)+2:]=matrix[:2,:2],matrix[:2,len(matrix)-2:]              #top left and right corner
    ext_matrix[len(matrix)+2:,:2],ext_matrix[len(matrix)+2:,len(matrix)+2:]=matrix[len(matrix)-2:,:2],matrix[len(matrix)-2:,len(matrix)-2:]      #bottom left and right corner
    return ext_matrix

def extend_boundary2(matrix,n,*args):
    k=int(len(matrix))
    l=int((n-1)/2)
    ext_matrix=np.zeros(((k+n-1),(k+n-1)))
    ext_matrix[:l,l:l+k]=matrix[:l,:] #top
    ext_matrix[l:l+k,:l]=matrix[:,:l] #left
    ext_matrix[l:l+k,l+k:]=matrix[:,k-l:] #right
    ext_matrix[l+k:,l:l+k]=matrix[k-l:,:] #bottom
    ext_matrix[:l,:l]=matrix[:l,:l]  #top left
    ext_matrix[:l,k+l:]=matrix[:l,k-l:]  #top right
    ext_matrix[k+l:,:l]=matrix[k-l:,:l]   #bottom left
    ext_matrix[k+l:,k+l:]=matrix[k-l:,k-l:]   #bottom right

    ext_matrix[l:l+k,l:l+k]=matrix[:,:]
    return ext_matrix

def get_image(name):
    Texture= np.fromfile(str(name), dtype='uint8', sep="")
    Texture=Texture.reshape([510, 510])
    return Texture

def write_file(image,name,*args):
    print(str(name)+' size is :'+str(len(image))+' x '+str(len(image)))
    image =image.astype(np.uint8)
    image.tofile(str(name))

def remove_dc(texture,*args):
    mean=np.average(texture)
    new_texture=texture-mean
    #for i in range(0,len(texture)):
    #    for j in range(0,len(texture)):
    #        if new_texture[i][j]<0:
    #            new_texture[i][j]=0
    return new_texture

def apply_laws(tex_dc_removed,laws25,*args):
    k=len(tex_dc_removed)
    filtered_img=np.zeros((k,k))
    extended_tex=extend_boundary2(tex_dc_removed,5)
    for i in range(0,k):
        for j in range(0,k):
            filtered_img[i][j]=np.sum(np.array(extended_tex[i:(i+5),j:(j+5)])*laws25)  #sum or average??
    return filtered_img

def get_energy(matrix,n,*args):
    extended_matrix=extend_boundary2(matrix,n)
    k=len(matrix)
    energy_matrix=np.zeros((k,k))
    for i in range(0,k):
        for j in range(0,k):
            energy_matrix[i][j]=np.average(np.array(extended_matrix[i:(i+n),j:(j+n)])**2)
    return energy_matrix

def get_laws25(laws1,laws2,*args):
    laws=np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            laws[i][j]=laws1[i]*laws2[j]
    return laws
