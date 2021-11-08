import heapq
import json
# from collections import defaultdict
listofcells = []
filesopen = []
# starting_vertex = '35'
# ending_vertex = '36'
k = 0
blocksize = 0
NumberOfCellsX = 0
NumberOfCellsY = 0
TotalCells = 0
latestfile = {}
dictofcells = {}
dictallnodes = {}
rxmin = 0
rymin = 0
overflowblocks = 0
filecount = 0
parent = {}
f = open('assignment3dump.txt', 'r')
x = f.readlines()
k = int(x[0])
blocksize = int(x[1])
temp = [int(i) for i in x[2].split()]
for i in temp:
    rxmin = temp[0]
    rymin = temp[1]
NumberOfCellsX = int(x[3])
NumberOfCellsY = int(x[4])
TotalCells = int(x[5])
latestfile = json.loads(x[6])
dictofcells = json.loads(x[7])
dictallnodes = json.loads(x[8])


# Mathematical function to calculate cell
def findCell(coordinate):
    coordinate = rationalize(coordinate, rxmin, rymin)
    x = int(coordinate[1] / k)
    y = int(coordinate[2] / k)
    cell = y * NumberOfCellsX + x
    # print(x, y, coordinate)
    return cell


# find cell with node id
def findcellwithnode(node):
    node = findxycoordinate(node)
    cell = findCell(node)
    return cell


# Rationalize the coordinate respective to lower bound to start cell No. from 0
def rationalize(cooridnate, rxmin, rymin):
    cooridnate[1] = cooridnate[1] - rxmin
    cooridnate[2] = cooridnate[2] - rymin
    return cooridnate


# find findxycoordinate of Node
def findxycoordinate(nodeid):
    try:
        return [nodeid] + dictallnodes[str(nodeid)]
    except KeyError:
        print("Node does not exist")


def Dijkstra_algo(starting_vertex, ending_vertex):
    global graph_seen_so_far
    global distances
    distances[starting_vertex] = 0
    parent[str(starting_vertex)] = str(starting_vertex)

    priorityQueue = [(0, starting_vertex)]
    while len(priorityQueue) > 0:
        current_distance, current_vertex = heapq.heappop(priorityQueue)
        cell = findcellwithnode(int(current_vertex))
        if cell not in listofcells:  # adding new cell,node is not in same cell
            oldgraph = graph_seen_so_far.copy()
            listofcells.append(cell)
            celldata = retrieve_all(cell)
            graph_seen_so_far = build_graph(
                celldata, graph_seen_so_far)  # updating graph_seen_so_far
            for key in graph_seen_so_far.keys():
                if key not in oldgraph.keys():
                    distances[str(key)] = float('infinity')

        if current_distance > distances[current_vertex]:
            continue
        try:
            for neighbor, weight in graph_seen_so_far[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priorityQueue, (distance, neighbor))
                    parent[str(neighbor)] = current_vertex
            if current_vertex == ending_vertex:
                break
        except KeyError:
            pass

    return distances


def Dijkstra_algo_standard(starting_vertex, ending_vertex):
    global entire_graph
    global distances
    distances[starting_vertex] = 0
    parent[str(starting_vertex)] = str(starting_vertex)

    priorityQueue = [(0, starting_vertex)]
    while len(priorityQueue) > 0:
        current_distance, current_vertex = heapq.heappop(priorityQueue)
        if current_distance > distances[current_vertex]:
            continue
        try:
            for neighbor, weight in entire_graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priorityQueue, (distance, neighbor))
                    parent[str(neighbor)] = current_vertex
            if current_vertex == ending_vertex:
                break
        except KeyError:
            pass

    return distances


def retrieve_all(cell):
    global filesopen
    next = 0
    x = []
    value = True
    while value is True:
        try:
            f = open(str(cell) + "_" + str(next) + '.txt', 'r')
            filesopen.append(str(cell) + "_" + str(next) + '.txt')
            x = x + [x.strip() for x in f.readlines()]
            f.close()
            next = next + 1
        except FileNotFoundError:
            value = False
            return x


graph_seen_so_far = {}
distances = {}


def build_graph(celldata, graph):
    global overflowblocks
    global filecount
    current = "NODES"
    for x in celldata:
        if x == 'OVERFLOW':
            overflowblocks = overflowblocks + 1
            continue
        elif current == "NODES" and x != 'EDGEINCELL':
            temp = [int(float(i)) for i in x.split()]
            graph[str(temp[0])] = {}
        elif x == 'EDGEINCELL':
            current = 'EDGEINCELL'
            continue
        elif current == 'EDGEINCELL' and x != 'BOUNDARYNODE':
            temp = [float(i) for i in x.split()]
            graph[str(int(temp[0]))][str(int(temp[1]))] = temp[2]
        elif x == 'BOUNDARYNODE':
            current = 'BOUNDARYNODE'
            continue
        elif current == 'BOUNDARYNODE' and x != 'BOUNDARYEDGE':
            temp = [int(float(i)) for i in x.split()]
            if str(temp[0]) not in graph.keys():
                graph[str(temp[0])] = {}
        elif x == 'BOUNDARYEDGE':
            current = 'BOUNDARYEDGE'
            continue
        elif current == 'BOUNDARYEDGE' and x != 'EOF':
            temp = [float(i) for i in x.split()]
            graph[str(int(temp[0]))][str(int(temp[1]))] = temp[2]
        else:
            filecount = filecount + 1
            return graph


entire_graph = {}


def build_entire_graph():
    entire_graph = {}
    for x in dictofcells.keys():
        cell_data = retrieve_all(int(x))
        if len(cell_data) > 0:
            entire_graph = build_graph(cell_data, entire_graph)
    return entire_graph


entire_graph = build_entire_graph()
listofcells = []
filesopen = []
overflowblocks = 0
filecount = 0
parent = {}


def findpath(ending_node, starting_node):
    current = str(ending_node)
    list = [str(ending_node)]
    current = parent[current]
    while current != str(starting_node):
        list.append(current)
        current = parent[current]
    list.append(str(starting_node))
    return list


def mainfunction_partition():
    global distances
    global graph_seen_so_far
    distances = {}
    graph_seen_so_far = {}
    starting_vertex = input("Enter the starting vertex :  ")
    ending_vertex = input("Enter the Ending Verter :  ")
    if str(starting_vertex) not in dictallnodes.keys() or \
            str(ending_vertex) not in dictallnodes.keys():
        print("\nEither starting vertex or ending vertex not in graph\n")
    else:
        cellx = findcellwithnode(starting_vertex)
        listofcells.append(cellx)
        celldata = retrieve_all(cellx)
        graph_seen_so_far = build_graph(celldata, graph_seen_so_far)
        distances = {vertex: float('infinity') for vertex in graph_seen_so_far}
        distances[str(ending_vertex)] = float('infinity')
        Distance_vector = Dijkstra_algo(starting_vertex, ending_vertex)
        # print(Distance_vector)
        if Distance_vector[str(ending_vertex)] == float('infinity'):
            print("NO PATH EXIST")
            print('Number of Blocks in Memory is', len(filesopen))
        else:
            print("Shortest Distance is  ",
                  Distance_vector[str(ending_vertex)])
            intermediate_nodes = findpath(ending_vertex, starting_vertex)
            intermediate_nodes.reverse()
            print(intermediate_nodes[0], end=" ")
            for i in intermediate_nodes[1:]:
                print(' ->', str(i),  end=' ')
            print('\n')
            print('Number of Blocks in Memory is', len(filesopen))
            print('\n')
            print("List of Open files")
            print(str(filesopen))
            print('\n')
            print("List of cells in Memory \n", listofcells)
            print('\n')
            print("Number of Overflow block", overflowblocks)
            if starting_vertex == ending_vertex:
                print("Path length is 0")
                print('\n')
            else:
                print("Path length is : ", len(intermediate_nodes) - 1)
                print('\n')


def mainfunction_standard():
    global distances
    global entire_graph
    distances = {}
    starting_vertex = input("Enter the starting vertex :  ")
    ending_vertex = input("Enter the Ending Verter :  ")
    if str(starting_vertex) not in dictallnodes.keys() or \
            str(ending_vertex) not in dictallnodes.keys():
        print("\nEither starting vertex or ending vertex not in graph\n")
    else:
        distances = {vertex: float('infinity') for vertex in entire_graph}
        Distance_vector = Dijkstra_algo(starting_vertex, ending_vertex)
        distances[starting_vertex] = 0

        if Distance_vector[str(ending_vertex)] != float('infinity'):
            print("Shortest Distance is  ",
                  Distance_vector[str(ending_vertex)])
            intermediate_nodes = findpath(ending_vertex, starting_vertex)
            intermediate_nodes.reverse()
            print(intermediate_nodes[0], end=" ")
            for i in intermediate_nodes[1:]:
                print(' ->', str(i),  end=' ')
            print('\n')
            if starting_vertex == ending_vertex:
                print("Path length is 0")
                print('\n')
            else:
                print("Path length is : ", len(intermediate_nodes) - 1)
                print('\n')

        else:
            print("NO PATH EXIST")


def choice():
    global listofcells
    global filesopen
    global overflowblocks
    global filecount
    global parent
    choice = 34
    while choice != 'q' or choice != 'Q':
        listofcells = []
        filesopen = []
        overflowblocks = 0
        filecount = 0
        parent = {}
        print("Press  0 to quit  \nPress  1 to Run Dijktra on Partitioned Graph \
        \nPress  2 to Run Dijktra on Standard Graph   \n")
        choice = int(input("Enter your choice : "))
        if choice == 0:
            break
        elif choice == 1:
            mainfunction_partition()
        elif choice == 2:
            mainfunction_standard()
        else:
            print('Wrong Input')


choice()
