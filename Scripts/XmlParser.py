class XmlNode(object):
    def __init__(self, name, parent):
        self.__name = name
        self.__parent = parent
        self.__attr = {}
        self.__child = []
        pass

    def getName(self):
        return self.__name
        pass

    def setAttr(self, attr):
        self.__attr = attr
        pass

    def getAttr(self, key, default=None):
        value = self.__attr.get(key, default)

        return value
        pass

    def addChild(self, node):
        self.__child.append(node)
        pass

    def getParent(self):
        return self.__parent
        pass

    def getChild(self):
        return self.__child
        pass

    def filterChild(self, name):
        filter_child = [node for node in self.__child if node.__name == name]
        return filter_child
        pass

    def __iter__(self):
        return self.__child.__iter__()
        pass

    def __getattr__(self, item):
        return self.__attr.get(item)
        pass
    pass

class SaxParser(object):
    def __init__(self):
        self.root = None
        self.current = None
        pass

    def getRoot(self):
        return self.root
        pass

    def begin(self, name):
        node = XmlNode(name, self.current)

        if self.current is not None:
            self.current.addChild(node)
            pass

        self.current = node

        if self.root is None:
            self.root = self.current
            pass
        pass

    def attr(self, attr):
        self.current.setAttr(attr)
        pass

    def end(self):
        self.current = self.current.getParent()
        pass
    pass

def parse(category, path):
    p = SaxParser()
    Mengine.parseXml(category, path, p)

    root = p.getRoot()
    return root
    pass