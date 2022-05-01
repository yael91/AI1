from ways import load_map_from_csv
import random
DFS_DEPTH_LIMIT = 10

def dfs(visited, graph, node, limit):
    if limit == 0:
        return visited
    if node not in visited:
        visited.append(node)
        for link in node.links:
            neighbour = graph.junctions()[link.target]
            dfs(visited, graph, neighbour, limit-1)
    return visited

#
# if __name__ == '__main__':
#
#     with open('problems.csv', 'a') as the_file:
#         graphh = load_map_from_csv()
#         for i in range(100):
#             randomStartIndex = random.randint(0, len(graphh.junctions()))
#             nodesList = dfs([], graphh,  graphh.junctions()[randomStartIndex], DFS_DEPTH_LIMIT)
#             nodesList.remove(graphh.junctions()[randomStartIndex])
#             randomEndIndex = random.randint(0, len(nodesList)-1)
#             randomEndNode = nodesList[randomEndIndex]
#             print("Problem number " + str(i) + " is: " + str(randomStartIndex) + "->" + str(randomEndNode.index))
#             the_file.write(str(randomStartIndex) + ", " + str(randomEndNode.index) + "\n")
