import tex_functions as tx
import numpy as np
from tex_functions import get_laws25
from sklearn.cluster import KMeans


class filter:
    def __init__(self,name,values):
        self.name=name
        self.values=values
L5=filter('L5',np.array([1,4,6,4,1]))
E5=filter('E5',np.array([-1,-2,0,2,1]));
S5=filter('S5',np.array([-1,0,2,0,-1]));
W5=filter('W5',np.array([-1,2,0,-2,1]));
R5=filter('R5',np.array([1,-4,6,-4,1]));

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

    TEX1=tx.get_image('comb.raw')
    TEX1_dc_removed=tx.remove_dc(TEX1)  #remove dc component

    feature1=[]

    feature_matrix=np.zeros((510*510,25))
    for i in range(0,25):
        temp=tx.apply_laws(TEX1_dc_removed,filter_array[i])
        temp1=tx.get_energy(temp,7)
        temp2=temp1.flatten()


        feature_matrix[:,i]=temp2
    print(feature_matrix[:20,0])

    norm_feature=np.zeros((510*510,25))
    for i in range(0,25):
        norm_feature[:,i]=(feature_matrix[:,i]-np.average(feature_matrix[:,0]))/np.std(feature_matrix[:,0])
    #for i in range(0,510*510):
    #    norm_feature[i,:]=(feature_matrix[i,:]-np.average(feature_matrix[i,:]))/np.std(feature_matrix[i,:])

    np.savetxt("features1.csv",norm_feature, delimiter=",")
