import json
k = 20
blocksize = 4
nodefile = 'sample_nodes.txt'
edgesfile = 'sample_edges.txt'
f = open(nodefile, "r")


# Rationalize the coordinate respective to lower bound to start cell No. from 0
def rationalize(cooridnate, rxmin, rymin):
    cooridnate[1] = cooridnate[1] - rxmin
    cooridnate[2] = cooridnate[2] - rymin
    return cooridnate


def derationalize(cooridnate, rxmin, rxmax):
    cooridnate[1] = cooridnate[1] + rxmin
    cooridnate[2] = cooridnate[2] + rymin
    return cooridnate


# round up to closest multiple of K
def roundup(number, multiple):
    if (multiple == 0):
        return number
    remainder = number % multiple
    if(remainder == 0):
        return number
    else:
        return number + multiple - remainder


# Assigning first co-ordinate to xmax , xmin , ymax , ymin
Node1 = f.readline().split()
xmax = float(Node1[1])
xmin = float(Node1[1])
ymax = float(Node1[2])
ymin = float(Node1[2])

print(xmax, xmin, ymax, ymin)

# finding xmax , xmin , ymax , ymin
for x in f:
    Node = [float(i) for i in x.split()]
    if xmax < Node[1]:
        xmax = Node[1]

    if ymax < Node[2]:
        ymax = Node[2]

    if xmin > Node[1]:
        xmin = Node[1]

    if ymin > Node[2]:
        ymin = Node[2]

f.close()


rxmax = int(xmax) + 1
rymax = int(ymax) + 1
rxmin = int(xmin)
rymin = int(ymin)
diffx = rxmax - rxmin
diffy = rymax - rymin


print("\n")


# print('diffx =', diffx, 'diffy= ', diffy)

NumberOfCellsX = int(roundup(diffx, k) / k)
NumberOfCellsY = int(roundup(diffy, k) / k)

TotalCells = NumberOfCellsX * NumberOfCellsY
print("TotalCells = ", TotalCells)

print("Number of columns =", NumberOfCellsX, "\n"
      "Number of Rows = ", NumberOfCellsY)

upperboundX = NumberOfCellsX * k + rxmin
upperboundY = NumberOfCellsY * k + rymin
print("lower bound = ", rxmin, rymin)
print("upper bound = ",  upperboundX, upperboundY)

# This dictionary contains latest file of cell
latestfile = {
}


def initDictfile():
    i = 0
    while i < TotalCells:
        latestfile[str(i)] = str(i) + '_' + str(0) + '.txt'
        i = i + 1


initDictfile()

# This dictionary contains cell along with nodes
dictofcells = {}


def initDictofcells():
    i = 0
    while i < TotalCells:
        dictofcells[str(i)] = []
        i = i + 1


initDictofcells()

# This dictionary contains Boundary node of each cell
BoundaryNodeInCell = {}


def initBoundaryNodeInCell():
    i = 0
    while i < TotalCells:
        BoundaryNodeInCell[str(i)] = []
        i = i + 1


initBoundaryNodeInCell()

# This dictionary contains inside edge of each cell
Edgeincells = {}


def initEdgeincells():
    i = 0
    while i < TotalCells:
        Edgeincells[str(i)] = []
        i = i + 1


initEdgeincells()

# This dictionary contains Boundary edge of each cell
BoundaryEdgeincells = {}


def initBoundaryEdgeincells():
    i = 0
    while i < TotalCells:
        BoundaryEdgeincells[str(i)] = []
        i = i + 1


initBoundaryEdgeincells()


# Mathematical function to find cell
def findCell(coordinate):
    coordinate = rationalize(coordinate, rxmin, rymin)
    x = int(coordinate[1] / k)
    y = int(coordinate[2] / k)
    cell = y * NumberOfCellsX + x
    # print(x, y, coordinate)
    return cell


file = open(nodefile, 'r')
Allnodes = file.readlines()
file.close()
# finding co-ordinate of node

dictallnodes = {}


def storeCoordinates():
    for x in Allnodes:
        Node = [float(i) for i in x.split()]
        Node[0] = int(Node[0])
        dictallnodes[str(Node[0])] = [Node[1], Node[2]]


storeCoordinates()


def findxycoordinate(nodeid):
    return [nodeid] + dictallnodes[str(nodeid)]


# provide co-ordinate from node id
# def findxycoordinate(nodeid):
#     for key, value in dictofcells.items():
#         for x in value:
#             if nodeid == x[0]:
#                 return x


# def findxycoordinate1(nodeid):
#     for x in Allnodes:
#         Node = [float(i) for i in x.split()]
#         if nodeid == int(Node[0]):
#             return Node


# find cell with node id
def findcellwithnode(node):
    node = findxycoordinate(node)
    cell = findCell(node)
    return cell

# def findcellwithnode(node):
#     for key, value in dictofcells.items():
#         for x in value:
#             if node == x[0]:
#                 return key

# Find if Nodes in given Edge is within cell or outside cell


def ifboundrynode(Edges, rxmin, rymin):
    cell1 = findcellwithnode(int(Edges[0]))
    cell2 = findcellwithnode(int(Edges[1]))
    if(cell1 != cell2):
        return True
    elif cell1 == cell2:
        return False


edgestored = []


def storeedge():
    file = open(edgesfile, 'r')
    f = file.readlines()
    file.close()
    for x in f:
        edge = [float(i) for i in x.split()]
        edgestored.append(tuple(edge))


storeedge()
edgestored = set(edgestored)
# Process all edges and find bundary edge, within edge and boundary node


def edgeProcess():
    # file = open(edgesfile, 'r')
    # f = file.readlines()
    # file.close()
    # prevedge = []
    for x in edgestored:
        edge = list(x)
        # print('Processing Edge ' + str(edge[0]) + "  and  " + str(edge[1]))
        # if (prevedge == edge):
        #     continue
        # prevedge = edge
        if ifboundrynode(edge, rxmin, rymin) is False:
            # coordinate = findxycoordinate(int(edge[0]))
            # coordinate = rationalize(coordinate, rxmin, rymin)
            cell = findcellwithnode(int(edge[0]))
            # print(cell)
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            edge[2] = edge[2]
            Edgeincells[str(cell)].append(str(edge[0]) + " " +
                                          str(edge[1]) + " " + str(edge[2]))
        else:
            cell0 = findcellwithnode(int(edge[0]))
            # cell1 = findCell(coordinate1)
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            edge[2] = edge[2]
            temp = str(edge[0]) + " " + str(edge[1]) + " " + str(edge[2])
            BoundaryEdgeincells[str(cell0)].append(temp)
            coordinate1 = findxycoordinate(int(edge[1]))
            cell0 = findcellwithnode(int(edge[0]))
            temp = str(coordinate1[0]) + " " + \
                str(coordinate1[1]) + " " + str(coordinate1[2])
            BoundaryNodeInCell[str(cell0)].append(temp)


# Write in file Edge within cell
def WriteEdgeincell():
    for key, value in Edgeincells.items():
        if len(value) > 0:
            try:
                current_file = filenum(str(key))
                # print(current_file)
                for y in value:
                    if checkoverflow(current_file):
                        f = open(current_file, 'a')
                        f.write('OVERFLOW\n')
                        f.close()

                    current_file = filenum(str(key))
                    f = open(current_file, 'a')
                    f.write(y)
                    f.write('\n')
                    f.close()
            except FileNotFoundError:
                pass


def removeDuplicate(a_dictionary):
    for key, value in a_dictionary.items():
        print(value)
        a_dictionary[key] = set(value)

# Write in file boundary Edge within cell


def WriteBoundaryEdgeincell():
    # print(BoundaryEdgeincells)
    for key, value in BoundaryEdgeincells.items():
        value = set(value)
        if len(value) > 0:
            try:
                current_file = filenum(str(key))
                # print(current_file)
                for y in value:
                    if checkoverflow(current_file):
                        f = open(current_file, 'a')
                        f.write('OVERFLOW\n')
                        f.close()

                    current_file = filenum(str(key))
                    f = open(current_file, 'a')
                    f.write(y)
                    f.write('\n')
                    f.close()
            except FileNotFoundError:
                pass


# Write in file boundary node in cell
def WriteBoundaryNodeincell():
    for key, value in BoundaryNodeInCell.items():
        value = set(value)
        if len(value) > 0:
            current_file = filenum(str(key))
            # print(current_file)
            for y in value:
                if checkoverflow(current_file):
                    f = open(current_file, 'a')
                    f.write('OVERFLOW\n')
                    f.close()

                current_file = filenum(str(key))
                f = open(current_file, 'a')
                f.write(y)
                f.write('\n')
                f.close()


# Write in Node within cell
def WriteNodeincell():
    for key, value in dictofcells.items():
        if len(value) > 0:
            current_file = filenum(str(key))
            # print(current_file)
            for y in value:
                if checkoverflow(current_file):
                    f = open(current_file, 'a')
                    f.write('OVERFLOW\n')
                    f.close()

                current_file = filenum(str(key))
                f = open(current_file, 'a')
                f.write(str(y[0]) + " " + str(y[1]) + " " + str(y[2]))
                f.write('\n')
                f.close()


# Node partition into cells
def partition():
    # file = open(nodefile, 'r')
    # Data = file.readlines()
    # file.close()
    for key, value in dictallnodes.items():
        Nodex = [int(key), value[0], value[1]]
        # print('Processing Node ' + str(Nodex[0]))
        # Nodex = rationalize(Nodex, rxmin, rymin)
        if(Nodex[1] is not None and Nodex[2] is not None):
            cellnumber = findCell(Nodex)
            # Nodex = derationalize(Nodex, rxmin, rymin)
            Nodex[0] = int(Nodex[0])
            Nodex[1] = Nodex[1]
            Nodex[2] = Nodex[2]
            dictofcells[str(cellnumber)].append(Nodex)


# Seperator Boundary Edge
def seperatorBE():
    i = 0
    while(i < TotalCells):
        try:
            current_file = filenum1(i)
            f = open(current_file, 'r')
            f.close()
            f = open(current_file, 'a')
            if checkoverflow(current_file):
                f.write('OVERFLOW\n')
            f.close()
            current_file = filenum(i)
            f = open(current_file, 'a')
            f.write('BOUNDARYEDGE\n')
            f.close()
        except IOError:
            pass
        i = i + 1


# Seperate Edge In Cell
def SeperatorEIC():
    i = 0
    while(i < TotalCells):
        try:
            current_file = filenum1(i)
            # print(current_file)
            f = open(current_file, 'r')
            f.close()
            f = open(current_file, 'a')
            if checkoverflow(current_file):
                f.write('OVERFLOW\n')
            f.close()
            current_file = filenum(i)
            f = open(current_file, 'a')
            f.write('EDGEINCELL\n')
            f.close()
        except IOError:
            pass
        i = i + 1


# Seperate Boundary Node
def SeperatorBN():
    i = 0
    while(i < TotalCells):
        try:
            current_file = filenum1(i)
            f = open(current_file, 'r')
            f.close()
            f = open(current_file, 'a')
            if checkoverflow(current_file):
                f.write('OVERFLOW\n')
            f.close()
            current_file = filenum(i)
            f = open(current_file, 'a')
            f.write('BOUNDARYNODE\n')
            f.close()
        except IOError:
            pass
        i = i + 1


# Seperator End of File
def EOF():
    i = 0
    while(i < TotalCells):
        try:
            current_file = filenum1(i)
            f = open(current_file, 'r')
            f.close()
            f = open(current_file, 'a')
            if checkoverflow(current_file):
                f.write('OVERFLOW\n')
            f.close()
            current_file = filenum(i)
            f = open(current_file, 'a')
            f.write('EOF\n')
            f.close()
        except IOError:
            pass
        i = i + 1


# Return latest file and create new if required
def filenum(cellnumber):
    f = open(latestfile[str(cellnumber)], 'a')
    f.close()
    f = open(latestfile[str(cellnumber)], 'r')
    x = f.readlines()
    f.close()
    if len(x) < blocksize:
        return latestfile[str(cellnumber)]
    elif len(x) == blocksize:
        x = latestfile[str(cellnumber)].replace(
            '.', " ").replace('_', " ").split()
        x[1] = int(x[1]) + 1
        f = open(str(cellnumber) + '_' + str(x[1]) + '.txt', 'a+')
        f.close()
        latestfile[str(cellnumber)] = str(
            cellnumber) + '_' + str(x[1]) + '.txt'
        return latestfile[str(cellnumber)]


# Only return file when already present
def filenum1(cellnumber):
    try:
        f = open(latestfile[str(cellnumber)], 'r')
        f.close()
        f = open(latestfile[str(cellnumber)], 'r')
        x = f.readlines()
        f.close()
        if len(x) < blocksize:
            return latestfile[str(cellnumber)]
        elif len(x) == blocksize:
            x = latestfile[str(cellnumber)].replace(
                '.', " ").replace('_', " ").split()
            x[1] = int(x[1]) + 1
            f = open(str(cellnumber) + '_' + str(x[1]) + '.txt', 'a+')
            f.close()
            latestfile[str(cellnumber)] = str(
                cellnumber) + '_' + str(x[1]) + '.txt'
            return latestfile[str(cellnumber)]
    except IOError:
        return "random.txt"


# Checks Overflow of file
def checkoverflow(filename):
    f = open(filename, 'r')
    x = f.readlines()
    if len(x) == blocksize - 1:
        return True
    return False


# Provides file names of given cell
def getfilenames(cellid):
    next = 1
    try:
        f = open(str(cellid) + '_0.txt', 'r')
        print(str(cellid) + '_0.txt')
        x = f.readlines()
        f.close()
        while len(x) == blocksize:
            print(str(cellid) + '_' + str(next) + '.txt')
            f = open(str(cellid) + '_' + str(next) + '.txt', 'r')
            x = f.readlines()
            f.close()
            next = next + 1
    except IOError:
        print("\nEither you have not partitioned or Cell doesn't exist or Cell \
has No Nodes\n\n")


# provides Lower and Upper Bound of cell
def providerange(cellid):
    y = int(cellid / NumberOfCellsX)
    x = cellid % NumberOfCellsX
    cellYmin = rymin + y * k
    cellXmin = rxmin + x * k
    cellYmax = cellYmin + k
    cellXmax = cellXmin + k
    print("cellYmin cellYmax cellXmin cellXmax :",
          cellYmin, cellYmax, cellXmin, cellXmax)
    # print(cellYmin, cellYmax, cellXmin, cellXmax)


# Driver Code
def mainfunction():
    stop = False
    while stop is False:
        print("1. Partition \n2. Get File Names of Cell \n3. \
Get Range of a Cell \n4. Get Co-ordinates of Node \n5. \
Get Cell ID with X,Y coordinates \n6. Exit")
        choice = 8
        try:
            choice = int(input('Enter Your Choice:'))

        except ValueError:
            print("\nInteger Choice does not Look like that\n")

        if choice == 1:
            i = 0
            while(i <= TotalCells):
                try:
                    f = open(str(i) + '_0.txt', 'r')
                    f.readline()
                    print("\nAlready Partitioned, Delete all \
Partition before trying again\n")
                    f.close()
                    return

                except IOError:
                    i = i + 1
            print("Partitioning..")
            print('writing Nodes in cell blocks...')
            partition()
            WriteNodeincell()
            # print(latestfile)
            print("Node - Cell Classification Complete")
            print("writing Edge inside cell ...")
            SeperatorEIC()
            edgeProcess()
            WriteEdgeincell()
            print('writing Edge within cell Complete')
            print('Writing Boundary Node...')
            SeperatorBN()
            WriteBoundaryNodeincell()
            print("writing Boundary Node Complete")
            print('Writing Boundary Edges')
            seperatorBE()
            WriteBoundaryEdgeincell()
            print('Writing boundary edge complete')
            print("Marking End of Cell File")
            EOF()

        elif choice == 2:
            cell = input("Enter the cell number: ")
            getfilenames(int(cell))

        elif choice == 3:
            cell = input("Enter the cell number: ")
            providerange(int(cell))
        elif choice == 4:
            NodeInput = int(input("Enter the Node number: "))
            Node = findxycoordinate(NodeInput)
            print('X = ' + str(Node[1]))
            print('Y = ' + str(Node[2]))
        elif choice == 5:
            X = input('Enter X =')
            Y = input('Enter Y =')
            coordinate = [3, float(X), float(Y)]
            cell = findCell(coordinate)
            print(cell)
        elif choice == 6:
            stop = True
        else:
            print('\nWrong Input, Better Luck Next Time\n')


mainfunction()


def dump():
    f = open('assignment3dump.txt', 'a')
    f.write(str(k))
    f.write('\n')
    f.write(str(blocksize))
    f.write('\n')
    f.write(str(rxmin) + " " + str(rymin))
    f.write('\n')
    f.write(str(NumberOfCellsX))
    f.write('\n')
    f.write(str(NumberOfCellsY))
    f.write('\n')
    f.write(str(TotalCells))
    f.write('\n')
    dump = json.dumps(latestfile)
    f.write(dump)
    f.write('\n')
    dump = json.dumps(dictofcells)
    f.write(dump)
    f.write('\n')
    dump = json.dumps(dictallnodes)
    f.write(dump)


dump()

# print(dictallnodes)
# nodeid = 5
# print([nodeid, dictallnodes[str(nodeid)[0]], dictallnodes[str(nodeid)[1]]])
# storeCoordinates()
# print(dictallnodes)


# partition()
# print(findxycoordinate(5))
# print(findcellwithnode(0))
# print(dictofcells)
# edgeProcess()
# print(BoundaryEdgeincells)
# print(Edgeincells)
# SeperatorEIC()
# WriteEdgeincell()
# seperatorBE()
# WriteBoundaryEdgeincell()
# print(findcellwithnode(5))
# SeperatorEIC()
# print(latestfile)
# edgeincell()
# boundarynode()
# edgeboundry()
# partition()
