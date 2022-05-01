from ways import load_map_from_csv
from ways import info
import time
import math
import statistics
import matplotlib.pyplot
import pylab
from ways import compute_distance
from ways import graph
from queue import PriorityQueue
from ways.info import SPEED_RANGES
import sys
import csv
import math
from stats import roads


def idastarCost(father, son):
    for link in father.links:
        if link.target == son.index:
            distance = link.distance / 1000
            speed = info.SPEED_RANGES[link.highway_type][1]
            return distance / speed


def idaReconstructivePath(cameFrom, current):
    totalPath = [current]
    while current in cameFrom:
        current = cameFrom[current]
        totalPath.append(current)
    return totalPath


def hh(start, target):
    huristics = compute_distance(start.lat, start.lon, target.lat, target.lon)
    huristics = huristics / 110
    return huristics


# My implementation for idastar algorithm
def find_idastar(sourceId, targetId, costFunction, hh):
    source = roads[int(sourceId)]
    target = roads[int(targetId)]
    limit = hh(source, target)
    path = [int(sourceId)]
    while True:
        t, _ = idastar_helper_func(path, 0, limit, target, hh, costFunction)
        if t == "FINISHED":
            return path, _
        if t == math.inf:
            return "NOT_FOUND"
        limit = t


# The recursive part of the idastar algorithm
def idastar_helper_func(ret_path, g, limit, goal, h_func, costFunction):
    current_node = roads[int(ret_path[-1])]
    f = g + hh(current_node, goal)
    if f > limit:
        return f, ret_path
    if current_node == goal:
        return "FINISHED", ret_path
    minimum = math.inf
    links = current_node.links
    for link in links:
        next_node = roads[int(link.target)]
        ret_path.append(next_node.index)
        cost = g + costFunction(roads[int(link.source)], roads[int(link.target)])
        t, n_path = idastar_helper_func(ret_path, cost, limit, goal, h_func, costFunction)
        if t == "FINISHED":
            return "FINISHED", n_path,
        if t < minimum:
            minimum = t
        ret_path.pop()
    return minimum, ret_path


if __name__ == '__main__':
    overallTime = 0
    timeListAlgo = []
    i = 0
    resultsFile = open("results/ADStarRuns.txt", "a")
    x_list = []
    y_list = []

    with open('problems.csv', 'r') as the_file:
        for line in the_file:
            i += 1
            print("Doing problem " + str(i))
            line = line.strip()
            start, dest = line.split(",")
            dest = dest[1:]
            int(dest)
            int(start)

            start_time = time.time()
            path, finalCost = find_idastar(start, dest, idastarCost, hh)  ##### call to the right function??
            finishMinusStartTime = time.time() - start_time
            overallTime += finishMinusStartTime  ## which time blablabalbalbal
            h_cost = hh(roads.junctions()[int(start)], roads.junctions()[int(dest)])

            x_list.append(h_cost)
            y_list.append(finalCost)

            resultsFile.write(str(h_cost) + "," + str(finalCost) + "\n")
            timeListAlgo.append(finishMinusStartTime)

            print(path)
            for point in path:
                print(str(point) + " ", end='')
            print("\n")
        averageTime = overallTime / 100
        standartDeviation = statistics.stdev(timeListAlgo)
        print("averageTime: " + str(averageTime))
        print("standartDeviation: " + str(standartDeviation))
    resultsFile.close()

## matplotlib.pyplot.scatter(x_list, y_list)
# matplotlib.pyplot.show()
