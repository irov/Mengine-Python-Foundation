class Graph(object):
    class Node(object):
        def __init__(self, value):
            self.value = value
            self.links = []
            self.neighbors = []
            pass

        def addLink(self, node):
            self.links.append(node)

            if node not in self.neighbors:
                self.neighbors.append(node)
                pass

            if self not in node.neighbors:
                node.neighbors.append(self)
                pass
            pass

        def destroy(self):
            self.links = []
            self.neighbors = []
            pass
        pass

    def __init__(self):
        self.nodes = []
        pass

    def destroy(self):
        for node in self.nodes:
            node.destroy()
            pass
        self.nodes = []
        pass

    def createNode(self, value):
        node = Graph.Node(value)
        self.nodes.append(node)

        return node
        pass

    def findNode(self, value):
        for node in self.nodes:
            if node.value == value:
                return node
                pass
            pass

        return None
        pass

    def findSpiral(self, aroundNode):
        if aroundNode not in self.nodes:
            return None
            pass

        sortNodes = [aroundNode]

        findNodes = sortNodes[:]

        while True:
            findLeafs = []

            for node in findNodes:
                for link in node.links:
                    if link in sortNodes:
                        continue

                    findLeafs.append(link)
                    sortNodes.append(link)
                    pass

            if len(findLeafs) == 0:
                break

            findNodes = findLeafs
            pass

        return sortNodes
        pass

    def findWay(self, nodeFrom, nodeTo):
        if nodeFrom is nodeTo:
            return [nodeFrom]
            pass

        wayMap = self.__makeWayMap(nodeFrom)

        if nodeTo not in wayMap:
            return [nodeFrom]
            pass

        way = [nodeTo]

        currentNode = nodeTo

        while True:
            stepNode = self.__nextStep(wayMap, currentNode)

            if stepNode is None:
                return [nodeFrom]
                pass

            if stepNode is None:
                continue
                pass

            way.append(stepNode)

            if stepNode is nodeFrom:
                break
                pass

            currentNode = stepNode
            pass

        return way[::-1]
        pass

    def __nextStep(self, wayMap, nodeFrom):
        costFrom = wayMap[nodeFrom]

        minimalCost = costFrom
        stepNode = None
        for node in nodeFrom.neighbors:
            if node not in wayMap:
                continue
                pass

            linkCost = wayMap[node]

            if linkCost < minimalCost:
                minimalCost = linkCost
                stepNode = node
                pass
            pass

        return stepNode
        pass

    def __makeWayMap(self, aroundNode):
        wayMap = {}
        wayMap[aroundNode] = 0

        findNodes = [aroundNode]

        while True:
            findLeafs = []

            for node in findNodes:
                currentCost = wayMap[node]

                for link in node.links:
                    if link in wayMap:
                        wayCost = wayMap[link]

                        if wayCost > currentCost + 1:
                            wayMap[link] = currentCost + 1
                        else:
                            continue
                            pass
                    else:
                        wayMap[link] = currentCost + 1
                        pass

                    findLeafs.append(link)
                    pass

            if len(findLeafs) == 0:
                break

            findNodes = findLeafs
            pass

        return wayMap
        pass
    pass