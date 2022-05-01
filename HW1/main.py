'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
from ucs import ucs_search, cost, hhh
from AStar import astar_search, astarCost, h


def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    path = ucs_search(source, target, cost, hhh)
    pathListIndex = []
    for part in path[0]:
        pathListIndex.append(part.index)
    return pathListIndex


def find_astar_route(source, target):
    path = astar_search(source, target, astarCost, h)
    pathListIndex = []
    for part in path[0]:
        pathListIndex.append(part.index)
    return pathListIndex


def find_idastar_route(source, target):
    from idastar import find_idastar
    path = find_idastar(source, target, astarCost, h)[0]
   # print(path)
    return path


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv

    dispatch(argv)
