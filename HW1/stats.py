'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
import math 

def load():
    r = load_map_from_csv()
    return r

roads = load()

def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    linkCounter = linkDisCounter = avg_dis = avg_branch = 0
    max_dis = max_branch = -math.inf
    min_dis = min_branch = math.inf
    dic = {}
    
    # foreach vertex in graph
    for junction in roads.junctions():
        linkCounter += len(junction.links)
        
        # Calc Outgoing branching factor
        if max_branch < len(junction.links):
            max_branch = len(junction.links)
        if min_branch > len(junction.links):
            min_branch = len(junction.links)
        
        # foreach edge in vertex
        for link in junction.links:
            linkDisCounter += link.distance
            
            # Calc Link type histogram
            if link.highway_type in dic:
                dic[link.highway_type] += 1
            else:
                dic[link.highway_type] = 1
                
            # Calc Link distance
            if max_dis < link.distance:
                max_dis = link.distance
            if min_dis > link.distance:
                min_dis = link.distance
    avg_dis = linkDisCounter / linkCounter
    avg_branch = linkCounter / len(roads.junctions())
    return {
        'Number of junctions' : len(roads.junctions()),
        'Number of links' : linkCounter,
        'Outgoing branching factor' : Stat(max=max_branch, min=min_branch, avg=avg_branch),
        'Link distance' : Stat(max=max_dis, min=min_dis, avg=avg_dis),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : dic,  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
