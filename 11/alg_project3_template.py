"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster
import random

#cluster = alg_cluster.Cluster([],6,5,[],[])

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    min_dist = float('inf')
    min_idx1 = 0
    min_idx2 = 0
    min_info = (min_dist,min_idx1,min_idx2)
    for index1 in range(len(cluster_list)):
        for index2 in range(index1 + 1 , len(cluster_list)):
            min_info = min(pair_distance(cluster_list,index1,index2),min_info)

    return min_info

#print slow_closest_pair(cluster)

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    length = len(cluster_list)
    min_dist = float('inf')
    min_idx1 = 0
    min_idx2 = 0
    min_info = (min_dist,min_idx1,min_idx2)
    if length <= 3:
        #base
        return slow_closest_pair(cluster_list)
    else:
        #devid
        middle = length/2
        sub_min1,index1,index2 = fast_closest_pair(cluster_list[0:middle])
        sub_min2,index3,index4 = fast_closest_pair(cluster_list[middle:length])
        if sub_min1 < sub_min2:
            min_dist = sub_min1
            min_idx1 = index1
            min_idx2 = index2
        else:
            min_dist = sub_min2
            min_idx1 = index3 + middle
            min_idx2 = index4 + middle
        #marge
        min_info = (min_dist,min_idx1,min_idx2)
        center_line = (cluster_list[middle-1].horiz_center() +  cluster_list[middle].horiz_center())/2
        min_info = min(closest_pair_strip(cluster_list,center_line,min_dist),min_info)
        
    return min_info


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    cluster_sub = [] 
    for  index,cluster in enumerate(cluster_list):
        if abs(horiz_center - cluster.horiz_center()) < half_width:
            cluster_sub.append(index)
    
    cluster_sub.sort(key = lambda index: cluster_list[index].vert_center())
    min_dist = float('inf')
    min_idx1 = -1
    min_idx2 = -1
    min_info = (min_dist,min_idx1,min_idx2)
    length = len(cluster_sub)
    for index1 in range(length - 1):
        for index2 in range(index1+1,min(index1 + 4,length)):
            origin_index1 = cluster_sub[index1]
            origin_index2 = cluster_sub[index2]
            min_info = min(pair_distance(cluster_list,origin_index1,origin_index2),min_info)
            
    return min_info
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    cluster_list.sort(key = lambda cluster:cluster.horiz_center())
    while(len(cluster_list) > num_clusters):
        _,index1,index2 = fast_closest_pair(cluster_list)
        cluster_list[index1].merge_clusters(cluster_list[index2])
        cluster_list.pop(index2)
        cluster_list.sort(key = lambda cluster:cluster.horiz_center())
    #assert len(cluster_list) == num_clusters
    return cluster_list


######################################################################
# Code for k-means clustering

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    #new_list = sorted(cluster_list,key = lambda cluster:cluster.total_population(),reverse=True)
    center_cluster = sorted(cluster_list,key = lambda cluster:cluster.total_population(),reverse=True)[0:num_clusters]
    for _ in range(num_iterations):
        new_center = [alg_cluster.Cluster(set([]),0,0,0.0,0) for _ in range(num_clusters)]
        for cluster in cluster_list:
            min_dist = float('inf')
            min_idx = -1
            for index,center in enumerate(center_cluster):
                distance = cluster.distance(center)
                if distance < min_dist:
                    min_dist = distance
                    min_idx = index
            new_center[min_idx].merge_clusters(cluster)
        center_cluster = list(new_center)
    return center_cluster
