from ways import info
import time
import math
import statistics
import matplotlib.pyplot as plt
import pylab
from ways import compute_distance
from stats import roads as graph
from ways import draw as draw


def astarCost(father, son):
    for link in father.links:
        if link.target == son.index:
            distance = link.distance / 1000
            speed = info.SPEED_RANGES[link.highway_type][1]
            return distance / speed


def minimumFScore(openSet, fScore):
    number = fScore[openSet[0]]
    monNode = openSet[0]
    for node in openSet:
        if fScore[node] < number:
            number = fScore[node]
            monNode = node
    return monNode


def reconstructivePath(cameFrom, current):
    totalPath = [current]
    while current in cameFrom:
        current = cameFrom[current]
        totalPath.append(current)
    totalPath.reverse()
    return totalPath


def astar_search(root, dest, funCost, h):
    start = graph.junctions()[int(root)]
    target = graph.junctions()[int(dest)]

    openSet = []
    openSet.append(start)
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = h(start, target)

    while openSet:
        current = minimumFScore(openSet, fScore)
        if current == target:
            return reconstructivePath(cameFrom, current), gScore[current]

        openSet.remove(current)
        for link in current.links:
            neighbor = graph.junctions()[link.target]
            tentativeGScore = gScore[current] + funCost(current, neighbor)
            if tentativeGScore < gScore.setdefault(neighbor, math.inf):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = gScore[neighbor] + h(current,
                                                        neighbor);  # there is a chance i accidently mix the h parameters

                if neighbor not in openSet:
                    openSet.append(neighbor)


def h(start, target):
    huristics = compute_distance(start.lat, start.lon, target.lat, target.lon)
    huristics = huristics / 110
    return huristics


if __name__ == '__main__':
    overallTime = 0
    timeListAlgo = []
    i = 0
    resultsFile = open("results/AStarRuns.txt", "a")
    x_list = []
    y_list = []

    with open('problems.csv', 'r') as the_file:
        for index, line in enumerate(the_file):
            i += 1
            print("Doing problem " + str(i))
            line = line.strip()
            start, dest = line.split(",")
            dest = dest[1:]

            start_time = time.time()
            path, finalCost = astar_search(start, dest, astarCost, h)
            finishMinusStartTime = time.time() - start_time
            overallTime += finishMinusStartTime  ## which time blablabalbalbal
            h_cost = h(graph.junctions()[int(start)], graph.junctions()[int(dest)])

            # if index == 11:
            #     draw.plot_path(graph, [item.index for item in path])
            #     plt.show()

            x_list.append(h_cost)
            y_list.append(finalCost)

            resultsFile.write(str(h_cost) + "," + str(finalCost) + "\n")
            timeListAlgo.append(finishMinusStartTime)

            for point in path:
                print(str(point.index) + " ", end='')
            print("\n")
        averageTime = overallTime / 100
        standartDeviation = statistics.stdev(timeListAlgo)
        print("averageTime: " + str(averageTime))
        print("standartDeviation: " + str(standartDeviation))
    resultsFile.close()

    # matplotlib.pyplot.scatter(x_list, y_list)
    # matplotlib.pyplot.show()
