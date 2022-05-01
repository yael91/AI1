from ways import info
import time
import math
import statistics
from stats import roads as graph


def cost(father, son):
    for link in father.links:
        if link.target == son.index:
            distance = link.distance / 1000
            speed = info.SPEED_RANGES[link.highway_type][1]
            return distance / speed


def minimumFScore(openSet, fScore):
    number = math.inf
    monNode = None
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


def ucs_search(root, end, funCost, h):
    start = graph.junctions()[int(root)]
    target = graph.junctions()[int(end)]

    openSet = set()
    openSet.add(start)
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = h()

    while openSet:
        current = minimumFScore(openSet, fScore)
        openSet.remove(current)

        if current.index == target.index:
            #print(gScore[current])
            return reconstructivePath(cameFrom, current), gScore[current]

        for link in current.links:
            neighbor = graph.junctions()[link.target]
            tentativeGScore = gScore[current] + funCost(current, neighbor)
            if tentativeGScore < gScore.setdefault(neighbor, math.inf):

                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = gScore[neighbor] + h()

                if neighbor not in openSet:
                    openSet.add(neighbor)
    return None


def hhh():
    return 0


if __name__ == '__main__':
    overallTime = 0
    timeListAlgo = []
    i = 0
    resultsFile = open("results/UCSRuns.txt", "a")

    with open('problems.csv', 'r') as the_file:
        for line in the_file:
            i += 1
            print("Doing problem " + str(i))
            line = line.strip()
            start, dest = line.split(",")
            dest = dest[1:]

            start_time = time.time()
            path, finalCost = ucs_search(start, dest, cost, hhh)
            finishMinusStartTime = time.time() - start_time
            overallTime += finishMinusStartTime  ## which time blablabalbalbal
            resultsFile.write(str(finalCost) + "\n")

            timeListAlgo.append(finishMinusStartTime)

            for point in path:
                print(str(point.index) + " ", end='')
            print("\n")
        averageTime = overallTime / 100
        standartDeviation = statistics.stdev(timeListAlgo)
        print("averageTime: " + str(averageTime))
        print("standartDeviation: " + str(standartDeviation))
    print(str(overallTime))
    resultsFile.close()
