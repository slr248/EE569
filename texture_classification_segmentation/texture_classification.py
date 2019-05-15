
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from itertools import permutations
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

def extend_boundary(matrix,*args):
    ext_matrix=np.zeros((132,132))
    for i in range(0,128):
        for j in range(0,128):
            ext_matrix[i+2][j+2]=matrix[i][j]
            ext_matrix[1,2:130],ext_matrix[0,2:130]=matrix[0,:],matrix[1,:]   #top
            ext_matrix[2:130,1],ext_matrix[2:130,0]=matrix[:,0],matrix[:,1]   #left
            ext_matrix[2:130,131],ext_matrix[2:130,130]=matrix[:,126],matrix[:,127]   #right
            ext_matrix[131,2:130],ext_matrix[130,2:130]=matrix[126,:],matrix[127,:]   #bottom
    ext_matrix[:2,:2],ext_matrix[:2,130:]=matrix[:2,:2],matrix[:2,126:]              #top left and right corner
    ext_matrix[130:,:2],ext_matrix[130:,130:]=matrix[126:,:2],matrix[126:,126:]      #bottom left and right corner
    return ext_matrix

def get_image(name):
    Texture= np.fromfile(str(name), dtype='uint8', sep="")
    Texture=Texture.reshape([128, 128])
    return Texture

def write_file(image,name,*args):
    print(str(name)+' size is :'+str(len(image))+' x '+str(len(image)))
    image =image.astype(np.uint8)
    image.tofile(str(name))

def remove_dc(texture,*args):
    mean=np.average(texture)
    new_texture=texture-mean

    return new_texture

def apply_laws(tex_dc_removed,laws25,*args):
    filtered_img=np.zeros((128,128))
    extended_tex=extend_boundary(tex_dc_removed)
    for i in range(0,128):
        for j in range(0,128):
            filtered_img[i][j]=np.sum(np.array(extended_tex[i:(i+5),j:(j+5)])*laws25)  #sum or average??
    return filtered_img


class filter:
    def __init__(self,name,values):
        self.name=name
        self.values=values
L5=filter('L5',np.array([1,4,6,4,1]))
E5=filter('E5',np.array([-1,-2,0,2,1]));
S5=filter('S5',np.array([-1,0,2,0,-1]));
W5=filter('W5',np.array([-1,2,0,-2,1]));
R5=filter('R5',np.array([1,-4,6,-4,1]));


def get_laws25(laws1,laws2,*args):
    laws=np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            laws[i][j]=laws1[i]*laws2[j]
    return laws

class L5XX(filter):
    def __init__(self,name,values):
        self.name=name
        self.values=values

L5L5=L5XX('L5L5',get_laws25(L5.values,L5.values))
L5E5=L5XX('L5E5',get_laws25(L5.values,E5.values))
L5S5=L5XX('L5S5',get_laws25(L5.values,S5.values))
L5W5=L5XX('L5W5',get_laws25(L5.values,W5.values))
L5R5=L5XX('L5L5',get_laws25(L5.values,R5.values))

class E5XX(filter):
    def __init__(self,name,values):
        self.name=name
        self.values=values

E5L5=E5XX('E5L5',get_laws25(E5.values,L5.values))
E5E5=E5XX('E5E5',get_laws25(E5.values,E5.values))
E5S5=E5XX('E5S5',get_laws25(E5.values,S5.values))
E5W5=E5XX('E5W5',get_laws25(E5.values,W5.values))
E5R5=E5XX('E5L5',get_laws25(E5.values,R5.values))

class S5XX(filter):
    def __init__(self,name,values):
        self.name=name
        self.values=values

S5L5=S5XX('S5L5',get_laws25(S5.values,L5.values))
S5E5=S5XX('S5E5',get_laws25(S5.values,E5.values))
S5S5=S5XX('S5S5',get_laws25(S5.values,S5.values))
S5W5=S5XX('S5W5',get_laws25(S5.values,W5.values))
S5R5=S5XX('S5L5',get_laws25(S5.values,R5.values))

class W5XX(filter):
    def __init__(self,name,values):
        self.name=name
        self.values=values

W5L5=W5XX('W5L5',get_laws25(W5.values,L5.values))
W5E5=W5XX('W5E5',get_laws25(W5.values,E5.values))
W5S5=W5XX('W5S5',get_laws25(W5.values,S5.values))
W5W5=W5XX('W5W5',get_laws25(W5.values,W5.values))
W5R5=W5XX('W5L5',get_laws25(W5.values,R5.values))

class R5XX(filter):
    def __init__(self,name,values):
        self.name=name
        self.values=values

R5L5=R5XX('R5L5',get_laws25(R5.values,L5.values))
R5E5=R5XX('R5E5',get_laws25(R5.values,E5.values))
R5S5=R5XX('R5S5',get_laws25(R5.values,S5.values))
R5W5=R5XX('R5W5',get_laws25(R5.values,W5.values))
R5R5=R5XX('R5L5',get_laws25(R5.values,R5.values))

filter_array=[L5L5.values,L5E5.values,L5S5.values,L5W5.values,L5R5.values,
              E5L5.values,E5E5.values,E5S5.values,E5W5.values,E5R5.values,
              S5L5.values,S5E5.values,S5S5.values,S5W5.values,S5R5.values,
              W5L5.values,W5E5.values,W5S5.values,W5W5.values,W5R5.values,
              R5L5.values,R5E5.values,R5S5.values,R5W5.values,R5R5.values]

if __name__=='__main__':

    TEX1=get_image('texture1.raw')
    TEX1_dc_removed=remove_dc(TEX1)  #remove dc component

    feature1=[]
    for i in filter_array:
        temp=apply_laws(TEX1_dc_removed,i)
        feature1.append(np.average(abs(temp)))
    print(max(feature1))
    feature1=np.array(feature1).reshape(25,1)

    ############ TEXTURE 2################

    TEX2=get_image('texture2.raw')
    TEX2_dc_removed=remove_dc(TEX2)  #remove dc component

    feature2=[]
    for i in filter_array:
        temp=apply_laws(TEX2_dc_removed,i)
        #feature2.append(np.average(temp**2))
        feature2.append(np.average(abs(temp)))
    print(max(feature2))
    feature2=np.array(feature2).reshape(25,1)

####################TEXTURE 3##########################
    TEX3=get_image('texture3.raw')
    TEX3_dc_removed=remove_dc(TEX3)  #remove dc component

    feature3=[]
    for i in filter_array:
        temp=apply_laws(TEX3_dc_removed,i)
        #feature3.append(np.average(temp**2))
        feature3.append(np.average(abs(temp)))
    print(max(feature3))
    feature3=np.array(feature3).reshape(25,1)


################# TEXTURE 4 #########################

    TEX4=get_image('texture4.raw')
    TEX4_dc_removed=remove_dc(TEX4)  #remove dc component

    feature4=[]
    for i in filter_array:
        temp=apply_laws(TEX4_dc_removed,i)
        #feature4.append(np.average(temp**2))
        feature4.append(np.average(abs(temp)))
    print(max(feature4))
    feature4=np.array(feature4).reshape(25,1)
##############TEXTURE 5#######################################

    TEX5=get_image('texture5.raw')
    TEX5_dc_removed=remove_dc(TEX5)  #remove dc component

    feature5=[]
    for i in filter_array:
        temp=apply_laws(TEX5_dc_removed,i)
        #feature5.append(np.average(temp**2))
        feature5.append(np.average(abs(temp)))
    print(max(feature5))
    feature5=np.array(feature5).reshape(25,1)

########### TEXTURE 6##########################################

    TEX6=get_image('texture6.raw')
    TEX6_dc_removed=remove_dc(TEX6)  #remove dc component

    feature6=[]
    for i in filter_array:
        temp=apply_laws(TEX6_dc_removed,i)
        #feature6.append(np.average(temp**2))
        feature6.append(np.average(abs(temp)))
    print(max(feature6))
    feature6=np.array(feature6).reshape(25,1)


########### TEXTURE 7 #########################################

    TEX7=get_image('texture7.raw')
    TEX7_dc_removed=remove_dc(TEX7)  #remove dc component

    feature7=[]
    for i in filter_array:
        temp=apply_laws(TEX7_dc_removed,i)
        #feature7.append(np.average(temp**2))
        feature7.append(np.average(abs(temp)))
    print(max(feature7))
    feature7=np.array(feature7).reshape(25,1)

######### TEXTURE 8#############################################3
    TEX8=get_image('texture8.raw')
    TEX8_dc_removed=remove_dc(TEX8)  #remove dc component

    feature8=[]
    for i in filter_array:
        temp=apply_laws(TEX8_dc_removed,i)
        #feature8.append(np.average(temp**2))
        feature8.append(np.average(abs(temp)))
    print(max(feature8))
    feature8=np.array(feature8).reshape(25,1)

####### TEXTURE 9###############################################

    TEX9=get_image('texture9.raw')
    TEX9_dc_removed=remove_dc(TEX9)  #remove dc component

    feature9=[]
    for i in filter_array:
        temp=apply_laws(TEX9_dc_removed,i)
        #feature9.append(np.average(temp**2))
        feature9.append(np.average(abs(temp)))
    print(max(feature9))
    feature9=np.array(feature9).reshape(25,1)

######### TEXTURE 10############################################3

    TEX10=get_image('texture10.raw')
    TEX10_dc_removed=remove_dc(TEX10)  #remove dc component

    feature10=[]
    for i in filter_array:
        temp=apply_laws(TEX10_dc_removed,i)
        #feature10.append(np.average(temp**2))
        feature10.append(np.average(abs(temp)))
    print(max(feature10))
    feature10=np.array(feature10).reshape(25,1)

######## TEXTURE 11###############################################

    TEX11=get_image('texture11.raw')
    TEX11_dc_removed=remove_dc(TEX11)  #remove dc component

    feature11=[]
    for i in filter_array:
        temp=apply_laws(TEX11_dc_removed,i)
        #feature11.append(np.average(temp**2))
        feature11.append(np.average(abs(temp)))
    print(max(feature11))
    feature11=np.array(feature11).reshape(25,1)

######## TEXTURE 12 #############################################

    TEX12=get_image('texture12.raw')
    TEX12_dc_removed=remove_dc(TEX12)  #remove dc component

    feature12=[]
    for i in filter_array:
        temp=apply_laws(TEX12_dc_removed,i)
        #feature12.append(np.average(temp**2))
        feature12.append(np.average(abs(temp)))
    print(max(feature12))
    feature12=np.array(feature12).reshape(25,1)

################################################################
    #feature_vector=np.transpose(np.array([feature1,feature2]))
    feature_vector=np.transpose(np.hstack((feature1,feature2,feature3,feature4,feature5,feature6,feature7,feature8,feature9,feature10,feature11,feature12)))         #normalize entire sample separately or normalize each feature for all samples separately???
    #feature_vector=np.transpose(np.hstack((feature1,feature2,feature6,feature7,feature8,feature9,feature11,feature12)))
    #norm_feature=np.zeros((12,25))
    norm_feature=np.zeros((12,25))
    for i in range(0,12):
        #norm_feature[:,i]=(feature_vector[:,i]-np.average(feature_vector[:,i]))/np.std(feature_vector[:,i])
        norm_feature[i,:]=(feature_vector[i,:]-np.average(feature_vector[i,:]))/np.std(feature_vector[i,:])
        #norm_feature[:,i]=(feature_vector[:,i]-min(feature_vector[:,i]))/(max(feature_vector[:,i])-min(feature_vector[:,i]))
    print(norm_feature.shape)
########################## PCA ###############################3
    pca=PCA(n_components=3)
    #pca.fit(norm_feature)
    pca.fit(feature_vector)
    feature_pca=pca.fit_transform(norm_feature)
    #feature_pca=pca.fit_transform(feature_vector)
    print(feature_pca.shape)

############## K-MEANS ###########################

kmeans=KMeans(n_clusters=4)
#kmeans.fit(norm_feature)
kmeans.fit(feature_pca)
#print(kmeans.labels_)
labels=kmeans.predict(feature_pca)
print(labels)
print(feature_pca)
sample=norm_feature[0,:].reshape(1,-1)
#sample=feature_pca[0,:].reshape(1,-1)
#prediction=kmeans.predict(sample)
#print('prediction is : '+str(prediction))
    #x=(feature3-np.average(feature3))/(np.std(feature3))
    #print(x)



    ########## 3d plot ###########
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(feature_pca[:,0], feature_pca[:,1],feature_pca[:,2],c='r',marker='o') #zdir='z', s=20, c=None, depthshade=True, *args, **kwargs)
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
plt.show()
