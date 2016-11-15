from alg_project3_template import fast_closest_pair
from alg_project3_template import slow_closest_pair
import alg_cluster
import random
import time
import matplotlib.pyplot as plt

def gen_random_clusters(num_clusters):
    '''
    return a list with cluster randomly
    '''
    cluster_list = []
    for _ in range(num_clusters):
        random_y = random.randrange(-2,2)
        random_x = random.randrange(-2,2)
        cluster_list.append(alg_cluster.Cluster(0,random_x,random_y,1,1))
    return cluster_list

num_list = [n for n in range(2,200)]
time_list1 = []
time_list2 = []
for num in num_list:
    cluster_list = gen_random_clusters(num)
    time1 = time.clock()
    fast_closest_pair(cluster_list)
    time2 = time.clock()
    time_list1.append(time2 - time1)
    time1 = time.clock()
    slow_closest_pair(cluster_list)
    time2 = time.clock()
    time_list2.append(time2 - time1)

l1,l2= plt.plot(num_list,time_list1,'b-',num_list,time_list2,'r-')
plt.legend((l1,l2),('fast pair','slow pair'),'upper right')
plt.show()
        
