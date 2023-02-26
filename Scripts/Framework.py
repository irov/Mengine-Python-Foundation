# coding=utf-8

# ----------------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------------
M_PI = 3.1415926535897932384626433832795
M_PI2 = 1.5707963267948966192313216916398
M_PI4 = 0.78539816339744830961566084581988
M_3PI4 = 2.3561944901923449288469825374596
M_5PI4 = 3.9269908169872415480783042290994
M_7PI4 = 5.74977871437821381673096259207391
M_PI8 = 0.39269908169872415480783042290994

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# ----------------------------------------------------------------------------
def setCenterAlign(node, set, nodeType="Sprite"):
    centerAlign = node.getCenterAlign()
    if centerAlign == set: return

    if nodeType == "Sprite":
        size = node.getSurfaceSize()
        pass

    x, y = getVec2f(node.getLocalPosition())
    if set == True:
        direction = 1
    else:
        direction = -1
    x += size.x / 2 * direction
    y += size.y / 2 * direction
    node.setLocalPosition(Menge.vec2f(x, y))
    node.setCenterAlign(set)
    pass

# ----------------------------------------------------------------------------
# Metod: setupHotspot
# Description:
# -
# ----------------------------------------------------------------------------
def setupHotspot(hotspot, points):
    hotspot.clearPoints()
    for point in points:
        hotspot.addPoint(point)
        pass
    pass

# ----------------------------------------------------------------------------
# Metod: tanf
# Description:
# -
# ----------------------------------------------------------------------------
def tanf(value):
    return Menge.sinf(value) / Menge.cosf(value)
    pass

# ----------------------------------------------------------------------------
def sign(value):
    if value >= 0:
        return 1
    return -1

# ----------------------------------------------------------------------------
# Metod: calculateDistance
# Description:
# -
# ----------------------------------------------------------------------------
def calculateDistance(x1, y1, x2, y2):
    return Menge.sqrtf((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    pass

# ----------------------------------------------------------------------------
# Metod: testHotSpot
# Description:
# -
# ----------------------------------------------------------------------------
def testHotSpots(point, hotspots):
    for hotspot in hotspots:
        if point.testHotSpot(hotspot):
            return True
    return False
    pass

# ----------------------------------------------------------------------------
# Metod: setSoundResource
# Description:
# -
# ----------------------------------------------------------------------------
def playSound(node, resource=None, rangeVal=None, stop=True):
    if stop == False and node.isPlaying() == True: return False

    if resource != None:
        number = ""
        if rangeVal != None:
            number += str(Menge.randint(rangeVal[0], rangeVal[1] + 1))
        node.setResourceSound(resource + number)
        pass

    if stop == True:
        node.stop()
    node.play()
    return True

# ----------------------------------------------------------------------------
def playSoundPool(pool, resource=None, rangeVal=None, stop=True):
    for node in pool:
        if playSound(node, resource, rangeVal, stop) == True:
            break
    pass

# ----------------------------------------------------------------------------
# Metod: rotateVec2f
# Description:
# -
# ----------------------------------------------------------------------------
def rotateVec2f(vec, angle):
    cosa = Menge.cosf(angle)
    sina = Menge.sinf(angle)
    x, y = getVec2f(vec)
    dx = x * cosa - y * sina
    dy = x * sina + y * cosa
    return Menge.vec2f(dx, dy)
    pass

# ----------------------------------------------------------------------------
# Method: getVectorsAngle
# Description:
# - param: 0 - вернуть угол, 1 - вернуть косинус, 2 - вурнуть синус, 3 - модуль угла
# ----------------------------------------------------------------------------
def getVectorsAngle(vec1, vec2, param=0):
    x1, y1 = getVec2f(vec1)
    x2, y2 = getVec2f(vec2)

    length1 = Menge.sqrtf(x1 * x1 + y1 * y1)
    length2 = Menge.sqrtf(x2 * x2 + y2 * y2)
    dotProduct = x1 * x2 + y1 * y2
    vecProduct = x1 * y2 - y1 * x2

    # print x1, y1, x2, y2

    cos = float(dotProduct) / (length1 * length2)
    sin = float(vecProduct) / (length1 * length2)

    if cos > 1: cos = 1
    if cos < -1: cos = -1
    if sin > 1: sin = 1
    if sin < -1: sin = -1

    if param in [0, 3]:
        angle = Menge.acosf(cos)
        if sin < 0 and param == 0: angle *= -1
        return angle
    elif param == 1:
        return cos
    elif param == 2:
        return sin

    return None
    pass

# ----------------------------------------------------------------------------
# Method: normVector
# Description:
# -
# ----------------------------------------------------------------------------
def normVector(*vector):
    if len(vector) == 1:
        x, y = getVec2f(vector[0])
        isVec2f = True
        pass
    elif len(vector) == 2:
        x, y = vector
        isVec2f = False
        pass
    else: return None

    length = calculateDistance(0, 0, x, y)
    x = float(x) / length
    y = float(y) / length

    if isVec2f == True:
        return Menge.vec2f(x, y)
    else:
        return x, y

    pass

# ----------------------------------------------------------------------------
# Method: convertTime
# Description:
# - flag: 0 - дописывать ноль перед одним порядком
# ----------------------------------------------------------------------------
def convertTime(time, flag=0):
    parsTime = ""
    minutes = int(time / 60)
    seconds = time % 60
    if flag == 0 and minutes < 10:
        parsTime += "0"
    parsTime += str(minutes) + ":"
    if flag == 0 and seconds < 10:
        parsTime += "0"
    parsTime += str(seconds)

    return parsTime
    pass

# ----------------------------------------------------------------------------
def getTimeInMinutes():
    return Menge.getTimeInSeconds() / 60.0

# ----------------------------------------------------------------------------
# Method: setRightAlign
# Description:
# -
# ----------------------------------------------------------------------------
def setRightAlign(text):
    length = Menge.getVec2fX(text.getLength())
    posX, posY = getVec2f(text.getLocalPosition())
    text.setLocalPosition(Menge.vec2f(posX - length, posY))
    pass

# ----------------------------------------------------------------------------
# Method: getType
# Description:
# -
# ----------------------------------------------------------------------------
def getType(object):
    return type(object).__name__

    pass

# ----------------------------------------------------------------------------
# Method: getClassName
# Description:
# -
# ----------------------------------------------------------------------------
def getClassName(object):
    return object.__class__.__name__
    pass

# ----------------------------------------------------------------------------
# Method: include
# Description:
# -
# ----------------------------------------------------------------------------
def include(list1, list2):
    tempList1 = list1[:]
    for item in list2:
        if item not in tempList1: return False
        tempList1.remove(item)
        pass

    return True
    pass

# ----------------------------------------------------------------------------
# Method: getSizeHotSpot
# Description:
# -
# ----------------------------------------------------------------------------
def getSizeHotSpot(size, center=False, left=0, top=0, right=0, bottom=0):
    if center == True:
        center = 1
    else:
        center = 0

    width, height = getVec2f(size)

    points = []
    points.append(Menge.vec2f(0 - width / 2 * center - left, 0 - height / 2 * center - top))
    points.append(Menge.vec2f(width - width / 2 * center + right, 0 - height / 2 * center - top))
    points.append(Menge.vec2f(width - width / 2 * center + right, height - height / 2 * center + bottom))
    points.append(Menge.vec2f(0 - width / 2 * center - left, height - height / 2 * center + bottom))

    return points
    pass

# ----------------------------------------------------------------------------
# Method: clearActiveTasksArray
# Description:
# -
# ----------------------------------------------------------------------------
def clearActiveTasksArray():
    global activatedTasks
    activatedTasks = []
    pass

# ----------------------------------------------------------------------------
# Method:
# Description:
# -
# ----------------------------------------------------------------------------
blocketScenes = {}

def blockGame():
    scene = Menge.getCurrentScene()
    blocketScenes[scene] = scene.getBlockInput()
    scene.blockInput(True)
    for subscene in scene.subScenes.values():
        blocketScenes[subscene] = subscene.getBlockInput()
        subscene.blockInput(True)
        pass
    pass

# ----------------------------------------------------------------------------
# Method:
# Description:
# -
# ----------------------------------------------------------------------------
def unblockGame():
    scene = Menge.getCurrentScene()
    scene.blockInput(blocketScenes[scene])
    for subscene in scene.subScenes.values():
        subscene.blockInput(blocketScenes[subscene])
        pass
    pass

# ----------------------------------------------------------------------------
# Method:
# Description:
# -
# ----------------------------------------------------------------------------
def setWorldPosition(Node, *position):
    position = getLocalPosFromWorld(Node, *position)

    if len(position) == 2:
        position = Menge.vec2f(*position)
        pass

    Node.setLocalPosition(position)
    pass

# ----------------------------------------------------------------------------
def getLocalPosFromWorld(Node, *position):
    if len(position) == 1:
        newWorldX, newWorldY = getVec2f(position)
    else:
        newWorldX, newWorldY = position

    oldWorldX, oldWorldY = getVec2f(Node.getWorldPosition())
    oldLocalX, oldLocalY = getVec2f(Node.getLocalPosition())
    dispX = oldWorldX - oldLocalX
    dispY = oldWorldY - oldLocalY

    newLocalX = newWorldX - dispX
    newLocalY = newWorldY - dispY
    if len(position) == 1:
        return Menge.vec2f(newLocalX, newLocalY)
    else:
        return newLocalX, newLocalY
    pass

# ----------------------------------------------------------------------------
# Method:
# Description:
# -
# ----------------------------------------------------------------------------
def adjustSize(currentSize, neededSize, onlyMinus=False):
    currentSizeX, currentSizeY = getVec2f(currentSize)
    neededSizeX, neededSizeY = getVec2f(neededSize)
    percentX = float(neededSizeX) / currentSizeX
    percentY = float(neededSizeY) / currentSizeY

    scale = min(percentX, percentY)
    if onlyMinus == True and scale > 1: scale = 1

    return Menge.vec2f(scale, scale)
    pass

# ----------------------------------------------------------------------------
def shuffle(x, acc=1000):
    # спизжено с модуля random
    # acc - точность

    for i in reversed(xrange(1, len(x))):
        # pick an element in x[:i+1] with which to exchange x[i]
        j = int(float(Menge.randint(0, acc)) / acc * (i + 1))
        x[i], x[j] = x[j], x[i]
    pass

# ----------------------------------------------------------------------------
def choice(seq, acc=1000):
    """Choose a random element from a non-empty sequence."""
    return seq[int(float(Menge.randint(0, acc)) / acc * len(seq))]  # raises IndexError if seq is empty

# ----------------------------------------------------------------------------
class Rectangle(object):
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        pass

    def __repr__(self):
        return str((self._x1, self._y1, self._x2, self._y2))

    def setX1(self, x1):
        self._x1 = x1
        pass

    def getX1(self):
        return self._x1

    p_X1 = property(getX1, setX1)

    def setY1(self, y1):
        self._y1 = y1
        pass

    def getY1(self):
        return self._y1

    p_Y1 = property(getY1, setY1)

    def setX2(self, x2):
        self._x2 = x2
        pass

    def getX2(self):
        return self._x2

    p_X2 = property(getX2, setX2)

    def setY2(self, y2):
        self._y2 = y2
        pass

    def getY2(self):
        return self._y2

    p_Y2 = property(getY2, setY2)

# ----------------------------------------------------------------------------
def subtractRectangle(inRectangles, rect):
    outRectangles = []
    for inRectangle in inRectangles:
        # if substract rectangle out of inRectangle
        if rect.p_X2 < inRectangle.p_X1 or rect.p_X1 > inRectangle.p_X2 or rect.p_Y2 < inRectangle.p_Y1 or rect.p_Y1 > inRectangle.p_Y2:
            outRectangles.append(inRectangle)
            pass
        # if substract rectangle fully in rectangle
        elif rect.p_X1 > inRectangle.p_X1 and rect.p_X2 < inRectangle.p_X2 and rect.p_Y1 > inRectangle.p_Y1 and rect.p_Y2 < inRectangle.p_Y2:
            outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X2, rect.p_Y1))
            outRectangles.append(Rectangle(rect.p_X2, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y2))
            outRectangles.append(Rectangle(rect.p_X1, rect.p_Y2, inRectangle.p_X2, inRectangle.p_Y2))
            outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y1, rect.p_X1, inRectangle.p_Y2))
            pass
        # if substract rectangle penetrates on one edge
        elif rect.p_Y1 > inRectangle.p_Y1 and rect.p_Y2 < inRectangle.p_Y2:
            if rect.p_X2 > inRectangle.p_X1 and rect.p_X2 < inRectangle.p_X2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y1))
                outRectangles.append(Rectangle(rect.p_X2, rect.p_Y1, inRectangle.p_X2, rect.p_Y2))
                outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y2, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            elif rect.p_X1 > inRectangle.p_X1 and rect.p_X1 < inRectangle.p_X2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y1))
                outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y1, rect.p_X1, rect.p_Y2))
                outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y2, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            elif rect.p_X1 < inRectangle.p_X1 and rect.p_X2 > inRectangle.p_X2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y1))
                outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y2, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            pass
        elif rect.p_X1 > inRectangle.p_X1 and rect.p_X2 < inRectangle.p_X2:
            if rect.p_Y2 > inRectangle.p_Y1 and rect.p_Y2 < inRectangle.p_Y2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X1, inRectangle.p_Y2))
                outRectangles.append(Rectangle(rect.p_X1, rect.p_Y2, rect.p_X2, inRectangle.p_Y2))
                outRectangles.append(Rectangle(rect.p_X2, inRectangle.p_Y1, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            elif rect.p_Y1 > inRectangle.p_Y1 and rect.p_Y1 < inRectangle.p_Y2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X1, inRectangle.p_Y2))
                outRectangles.append(Rectangle(rect.p_X1, inRectangle.p_Y1, rect.p_X2, rect.p_Y1))
                outRectangles.append(Rectangle(rect.p_X2, inRectangle.p_Y1, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            elif rect.p_Y1 < inRectangle.p_Y1 and rect.p_Y2 > inRectangle.p_Y2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X1, inRectangle.p_Y2))
                outRectangles.append(Rectangle(rect.p_X2, inRectangle.p_Y1, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            pass
        # if substract rectangle penetrates on two edges
        elif rect.p_X2 > inRectangle.p_X1 and rect.p_X2 < inRectangle.p_X2 and rect.p_Y2 > inRectangle.p_Y1 and rect.p_Y2 < inRectangle.p_Y2 and rect.p_X1 < inRectangle.p_X1 and rect.p_Y1 < inRectangle.p_Y1:
            outRectangles.append(Rectangle(rect.p_X2, inRectangle.p_Y1, inRectangle.p_X2, inRectangle.p_Y2))
            outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y2, rect.p_X2, inRectangle.p_Y2))
            pass
        elif rect.p_X1 > inRectangle.p_X1 and rect.p_X1 < inRectangle.p_X2 and rect.p_Y2 > inRectangle.p_Y1 and rect.p_Y2 < inRectangle.p_Y2 and rect.p_X2 > inRectangle.p_X2 and rect.p_Y1 < inRectangle.p_Y1:
            outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X1, inRectangle.p_Y2))
            outRectangles.append(Rectangle(rect.p_X1, rect.p_Y2, inRectangle.p_X2, inRectangle.p_Y2))
            pass
        elif rect.p_X2 > inRectangle.p_X1 and rect.p_X2 < inRectangle.p_X2 and rect.p_Y1 > inRectangle.p_Y1 and rect.p_Y1 < inRectangle.p_Y2 and rect.p_X1 < inRectangle.p_X1 and rect.p_Y2 > inRectangle.p_Y2:
            outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y1))
            outRectangles.append(Rectangle(rect.p_X2, rect.p_Y1, inRectangle.p_X2, inRectangle.p_Y2))
            pass
        elif rect.p_X1 > inRectangle.p_X1 and rect.p_X1 < inRectangle.p_X2 and rect.p_Y1 > inRectangle.p_Y1 and rect.p_Y1 < inRectangle.p_Y2 and rect.p_X2 > inRectangle.p_X2 and rect.p_Y2 > inRectangle.p_Y2:
            outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X1, inRectangle.p_Y2))
            outRectangles.append(Rectangle(rect.p_X1, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y1))
            pass
        # if substract rectangle penetrates on tree edges
        elif rect.p_Y1 < inRectangle.p_Y1 and rect.p_Y2 > inRectangle.p_Y2:
            if rect.p_X2 > inRectangle.p_X1 and rect.p_X2 < inRectangle.p_X2:
                outRectangles.append(Rectangle(rect.p_X2, inRectangle.p_Y1, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            elif rect.p_X1 > inRectangle.p_X1 and rect.p_X1 < inRectangle.p_X2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, rect.p_X1, inRectangle.p_Y2))
                pass
            pass
        elif rect.p_X1 < inRectangle.p_X1 and rect.p_X2 > inRectangle.p_X2:
            if rect.p_Y2 > inRectangle.p_Y1 and rect.p_Y2 < inRectangle.p_Y2:
                outRectangles.append(Rectangle(inRectangle.p_X1, rect.p_Y2, inRectangle.p_X2, inRectangle.p_Y2))
                pass
            elif rect.p_Y1 > inRectangle.p_Y1 and rect.p_Y1 < inRectangle.p_Y2:
                outRectangles.append(Rectangle(inRectangle.p_X1, inRectangle.p_Y1, inRectangle.p_X2, rect.p_Y1))
                pass

    return outRectangles