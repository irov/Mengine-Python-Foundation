import math

from Foundation.ObjectManager import ObjectManager

def createImageHotspot(image, name):
    imageResource = image.getResourceImage()

    imageHotspot = Mengine.createNode("HotSpotImage")
    imageHotspot.setResourceImage(imageResource)
    imageHotspot.setAlphaTest(0.1)

    return imageHotspot
    pass

def Fmax(*arg):
    max = arg[0]
    for x in arg:
        if x > max:
            max = x
            pass
        pass
    return max
    pass

def Fmin(*arg):
    min = arg[0]
    for x in arg:
        if x < min:
            min = x
            pass
        pass
    return min
    pass

def HsvToRgb360(hsv):
    h, s, v = hsv

    h = float(h) / 360.0
    s = float(s) / 100.0
    v = float(v) / 100.0

    r = 0
    g = 0
    b = 0

    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    leftI = i % 6

    if leftI == 0:
        r = v
        g = t
        b = p
        pass
    elif leftI == 1:
        r = q
        g = v
        b = p
        pass
    elif leftI == 2:
        r = p
        g = v
        b = t
        pass
    elif leftI == 3:
        r = p
        g = q
        b = v
        pass
    elif leftI == 4:
        r = t
        g = p
        b = v
        pass
    elif leftI == 5:
        r = v
        g = p
        b = q
        pass

    return [r, g, b]
    pass

def RgbToHsv360(rgb):
    r, g, b = rgb

    r = float(r) / 255.0
    g = float(g) / 255.0
    b = float(b) / 255.0

    max = Fmax(r, g, b)
    min = Fmin(r, g, b)

    h = max
    s = max
    v = max

    d = max - min
    if max == 0:
        s = 0
        pass
    else:
        s = 1 - min / max
        pass

    if max == min:
        h = 0
        pass
    else:
        if max == r:
            if g < b:
                sub = 6
                pass
            else:
                sub = 0
                pass
            h = (g - b) / d + sub
            pass
        elif max == g:
            h = (b - r) / d + 2
            pass
        elif max == b:
            h = (r - g) / d + 4
            pass
        h /= 6
        pass

    return [h * 360, s * 100, v * 100]
    pass

def createBBSpriteHotspot(name, sprite):
    imageSize = sprite.getSurfaceSize()

    BBHotspot = Mengine.createNode("HotSpotPolygon")

    polygon = []
    polygon.append((0.0, 0.0))
    polygon.append((imageSize.x, 0.0))
    polygon.append((imageSize.x, imageSize.y))
    polygon.append((0.0, imageSize.y))

    BBHotspot.setPolygon(polygon)
    return BBHotspot
    pass

def createPolygonScene(layer, ox, oy):
    size = layer.getSize()
    polygon = [(-ox, -oy), (-ox, size.y - oy), (size.x - ox, size.y - oy), (size.x - ox, -oy)]
    return polygon
    pass

def chance_element(population, chance_provider, chance_range=100.0):
    elements = []

    for element in population:
        chance = chance_provider(element)

        bones = Mengine.randf(chance_range)

        if chance >= bones:
            elements.append(element)
            pass
        pass

    if len(elements) == 0:
        return None
        pass

    best_element = rand_element(elements)

    return best_element
    pass

def weight_element(population, chance_provider, chance_range=100.0):
    elements = []

    while len(elements) == 0:
        cycle = True
        for element in population:
            if element in elements:
                continue
                pass

            cycle = False

            chance = chance_provider(element)

            bones = Mengine.randf(chance_range)

            if chance >= bones:
                elements.append(element)
                pass
            pass

        if cycle is True:
            break
            pass
        pass

    if len(elements) == 0:
        return None
        pass

    best_element = rand_element(elements)

    return best_element
    pass

def weight_elements(population, k, chance_provider, chance_range=100.0):
    elements = []

    while len(elements) < k:
        cycle = True
        for element in population:
            if element in elements:
                continue
                pass

            cycle = False

            chance = chance_provider(element)

            bones = Mengine.randf(chance_range)

            if chance >= bones:
                elements.append(element)
                pass
            pass

        if cycle is True:
            return elements
            pass
        pass

    if len(elements) == 0:
        return []
        pass

    best_elements = rand_sample_list(elements, k)

    return best_elements
    pass

def rand_list(population, randomizer=None):
    if isinstance(population, list) is False:
        Trace.log("Utils", 0, "Utils.rand_sample_list: population should be list, received %s" % type(population).__name__)
        return None
        pass

    rand_count = len(population)

    rand_population = population[:]
    for index in range(rand_count):
        if randomizer is None:
            rand_index = Mengine.rand(rand_count)
        else:
            rand_index = randomizer.getRandom(rand_count)
        rand_population[index], rand_population[rand_index] = rand_population[rand_index], rand_population[index]
        pass

    return rand_population
    pass

def rand_element(population, randomizer=None):
    rand_count = len(population)

    if rand_count == 0:
        Trace.log("Utils", 0, "Utils.rand_element: population should be not empty")

        return None
        pass

    if randomizer is None:
        rand_index = Mengine.rand(rand_count)
    else:
        rand_index = randomizer.getRandom(rand_count)

    if isinstance(population, list):
        element = population[rand_index]
    elif isinstance(population, dict):
        element = population.values()[rand_index]
        pass
    else:
        Trace.log("Utils", 0, "Utils.rand_element: population should be list or dict, received '%s'" % type(population).__name__)
        return None
        pass

    return element
    pass

def rand_sample_list(population, k, randomizer=None):
    if isinstance(population, list) is False:
        Trace.log("Utils", 0, "Utils.rand_sample_list: population should be list, received %s" % type(population).__name__)
        return None
        pass

    rand_count = len(population)

    if k > rand_count:
        Trace.log("Utils", 0, "Utils.rand_sample_list: population size(%d) less then k(%d)" % (rand_count, k))
        return None
        pass

    rand_population = population[:]
    for index in range(rand_count):
        if randomizer is None:
            rand_index = Mengine.rand(rand_count)
        else:
            rand_index = randomizer.getRandom(rand_count)
        rand_population[index], rand_population[rand_index] = rand_population[rand_index], rand_population[index]
        pass

    sample_rand_population = rand_population[:k]

    return sample_rand_population
    pass

def rand_sample_list2(population, k):
    if isinstance(population, list) is False:
        Trace.log("Utils", 0, "Utils.rand_sample_list: population should be list, received %s" % type(population).__name__)
        return None
        pass

    rand_count = len(population)

    if k > rand_count:
        Trace.log("Utils", 0, "Utils.rand_sample_list: population size(%d) less then k(%d)" % (rand_count, k))
        return None
        pass

    rand_population = population[:]
    for index in range(rand_count):
        rand_index = Mengine.rand(rand_count)
        rand_population[index], rand_population[rand_index] = rand_population[rand_index], rand_population[index]
        pass

    sample_rand_population = rand_population[:k]
    other_rand_population = rand_population[k:]

    return sample_rand_population, other_rand_population
    pass

def rand_circle_element(Radius, Count, ElementRadius, TestCount=25):
    elements = []
    for count_index in xrange(int(Count)):
        for test_index in xrange(int(TestCount)):
            Position = Mengine.radius_randf(Radius)

            def __test(elements, Position):
                if Mengine.sqrlength_v2_v2((0.0, 0.0), Position) > (Radius - ElementRadius) * (Radius - ElementRadius):
                    return False
                    pass

                for element in elements:
                    if Mengine.sqrlength_v2_v2(element, Position) < ElementRadius * ElementRadius:
                        return False
                        pass
                    pass

                return True
                pass

            if __test(elements, Position) is False:
                continue
                pass

            elements.append(Position)
            break
            pass
        pass

    return elements
    pass

def calculateBoundedSize(orgSize, frameSize):
    """Calculates maximum size of item, inscribed in frame, keeping aspect.
    """
    if orgSize[0] == 0 or orgSize[1] == 0:
        print("WARNING: Utils.calculateBoundedSize: zero image size specified:", orgSize, frameSize)
        return orgSize

    h = orgSize[1]
    w = frameSize[0]
    h = h * w / orgSize[0]

    if h > frameSize[1]:
        oldH = h
        h = frameSize[1]
        w = w * h / oldH
        pass

    return (w, h)
    pass

def clamp(value, minLimit, maxLimit):
    return min(maxLimit, max(minLimit, value))
    pass

def floor(value):
    return int(value) if value >= 0 else int(value) - 1
    pass

def hasResourceMovie(GroupName, MovieName):
    if GroupName is None:
        return False
        pass

    if MovieName is None:
        return False
        pass

    ResourceMovieName = "Movie%s_%s" % (GroupName, MovieName)

    if Mengine.hasResource(ResourceMovieName) is False:
        return False
        pass

    return True
    pass

def getMovieDuration(GroupName, MovieName):
    ResourceMovieName = "Movie%s_%s" % (GroupName, MovieName)

    if Mengine.hasResource(ResourceMovieName) is False:
        Trace.log("Entity", 0, "Utils.getMovieDuration not found resource %s" % (ResourceMovieName))

        return None
        pass

    ResourceMovie = Mengine.getResourceReference(ResourceMovieName)

    duration = ResourceMovie.getDuration()

    return duration
    pass

def getMovieLayerIn(GroupName, MovieName, LayerName):
    ResourceMovieName = "Movie%s_%s" % (GroupName, MovieName)

    if Mengine.hasResource(ResourceMovieName) is False:
        Trace.log("Entity", 0, "Utils.getMovieDuration not found resource %s" % (ResourceMovieName))

        return None
        pass

    ResourceMovie = Mengine.getResourceReference(ResourceMovieName)

    In = ResourceMovie.getLayerIn(LayerName)

    return In
    pass

def makeResourceMovie(GroupName, MovieName, Important=False):
    if MovieName is None:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeResourceMovie MovieName is None")
            pass

        return None
        pass

    ResourceMovieName = "Movie%s_%s" % (GroupName, MovieName)

    if Mengine.hasResource(ResourceMovieName) is False:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeResourceMovie not found resource %s" % (ResourceMovieName))
            pass

        return None
        pass

    ResourceMovie = Mengine.getResourceReference(ResourceMovieName)

    return ResourceMovie
    pass

def makeResourceMovie2(GroupName, Important=False):
    if GroupName is None:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeResourceMovie2 GroupName is None")
            pass

        return None
        pass

    ResourceMovieName = "Movie2_%s" % (GroupName)

    if Mengine.hasResource(ResourceMovieName) is False:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeResourceMovie2 not found resource %s" % (ResourceMovieName))
            pass

        return None
        pass

    ResourceMovie = Mengine.getResourceReference(ResourceMovieName)

    return ResourceMovie
    pass

def makeMovie(GroupName, MovieName, Position=[0, 0], Enable=True, Play=False, Loop=False, Name=None, Random=False, Important=False):
    ResourceMovie = Utils.makeResourceMovie(GroupName, MovieName, Important)

    if ResourceMovie is None:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeMovie invalid make resource %s movie name %s" % (GroupName, MovieName))
            pass

        return None
        pass

    if Name is None:
        Name = MovieName
        pass

    MoviePosition = [Position[0], Position[1]]

    Movie = ObjectManager.createObjectUnique("Movie", Name, None, ResourceMovie=ResourceMovie, Position=MoviePosition, Enable=Enable, Play=Play, Loop=Loop)

    if Random is True:
        Duration = Movie.getDuration()
        rand = rand_number100()

        Timing = Duration * float(rand) / 100.0
        Movie.setStartTiming(Timing)
        pass

    return Movie
    pass

def makeMovie2(GroupName, CompName, Enable=True, Play=False, Loop=False, Name=None, ParentNode=None):
    """
    :param GroupName: str, movie2 compositions should be in this group resource movie
    :param CompName: str should be without Movie2_ prefix
    :param Name: str returned obj movie2 name (if none will be "Movie2" + CompName
    :param ParentNode: node to attach (if none will be attached to Group in this case no need to destroy() obj manually)
    :return: ObjectMovie2 instance
    """

    if GroupName is None:
        return

    ResourceMovie = Utils.makeResourceMovie2(GroupName)
    ResourceMovieName = CompName

    if Name is None:
        Name = "Movie2_" + CompName

    Movie = ObjectManager.createObjectUnique("Movie2", Name, None, ResourceMovie=ResourceMovie, CompositionName=ResourceMovieName, Enable=Enable, Play=Play, Loop=Loop)

    if Movie:
        Movie.setEnable(Enable)

        if ParentNode and Movie.isActive():
            ParentNode.addChild(Movie.getEntityNode())

    return Movie

def makeMovie2Button(GroupName, CompName, OutName=None, Enable=True, ParentNode=None):
    """
    :param GroupName: str, movie2button compositions should be in this group resource movie
    :param CompName: str should be without Movie2Button_ prefix and state suffix
    :param OutName: str returned obj movie2button name
    :param ParentNode: node to attach (if none will be attached to Group in this case no need to destroy() obj manually)
    :return: ObjectMovie2Button instance
    """
    if GroupName is None:
        return

    ResourceMovie = Utils.makeResourceMovie2(GroupName)
    ResourceMovieName = ResourceMovie.getName()

    if OutName is None:
        OutName = "Movie2Button_" + CompName

    Movie2ButtonObj = ObjectManager.createObjectUnique("Movie2Button", OutName, None, ResourceMovie=ResourceMovieName, CompositionNameIdle=CompName + "_Idle", CompositionNameAppear=CompName + "_Appear", CompositionNameEnter=CompName + "_Enter", CompositionNameOver=CompName + "_Over", CompositionNameLeave=CompName + "_Leave", CompositionNamePush=CompName + "_Push", CompositionNamePressed=CompName + "_Pressed", CompositionNameRelease=CompName + "_Release", CompositionNameClick=CompName + "_Click",
        CompositionNameBlock=CompName + "_Block", CompositionNameBlockEnter=CompName + "_BlockEnter", CompositionNameBlockEnd=CompName + "_BlockEnd", CompositionNameSelected=CompName + "_Selected", CompositionNameSelectedEnter=CompName + "_SelectedEnter", CompositionNameSelectedEnd=CompName + "_SelectedEnd", Enable=Enable)

    if Movie2ButtonObj:
        Movie2ButtonObj.setEnable(Enable)

        if ParentNode and Movie2ButtonObj.isActive():
            ParentNode.addChild(Movie2ButtonObj.getEntityNode())

    return Movie2ButtonObj

def makeMovieNode(GroupName, MovieName, Position=None, Enable=True, AutoPlay=True, Loop=False, Name=None, Important=False):
    ResourceMovie = Utils.makeResourceMovie(GroupName, MovieName, Important)

    if ResourceMovie is None:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeMovieNode invalid make resource %s movie name %s" % (GroupName, MovieName))
            pass

        return None
        pass

    Movie = Mengine.createNode("Movie")

    if Name is None:
        Name = MovieName
        pass

    Movie.setName(Name)

    Movie.setResourceMovie(ResourceMovie)

    if Position is not None:
        Movie.setLocalPosition(Position)
        pass

    animation = Movie.getAnimation()

    animation.setLoop(Loop)

    if AutoPlay is not None:
        animation.setAutoPlay(AutoPlay)
        pass

    if Enable is True:
        Movie.enable()
        pass
    else:
        Movie.disable()
        pass

    return Movie
    pass

def makeMovie2Node(GroupName, MovieName, Position=None, Enable=True, AutoPlay=True, Loop=False, Name=None, Important=False, Interactive=True):
    ResourceMovie = Utils.makeResourceMovie2(GroupName, Important)

    if ResourceMovie is None:
        if Important is True:
            Trace.log("Entity", 0, "Utils.makeMovieNode invalid make resource %s movie name %s" % (GroupName, MovieName))
            pass

        return None
        pass

    Movie = Mengine.createNode("Movie2")

    if Name is None:
        Name = MovieName
        pass

    Movie.setName(Name)

    Movie.setResourceMovie2(ResourceMovie)
    Movie.setCompositionName(MovieName)

    if Position is not None:
        Movie.setLocalPosition(Position)
        pass

    if Interactive is True:
        Movie.setInteractive(True)
        pass

    animation = Movie.getAnimation()

    animation.setLoop(Loop)

    if AutoPlay is not None:
        animation.setAutoPlay(AutoPlay)
        pass

    if Enable is True:
        Movie.enable()
        pass
    else:
        Movie.disable()
        pass

    return Movie
    pass

def makeSpineNode(ResourceName, InitialAnimationName=None, InitialState=None, Position=None, Loop=False, Enable=True, Play=False):
    Spine = Mengine.createNode("Spine")
    ResourceSpine = Mengine.getResourceReference(ResourceName)
    Spine.setResourceSpine(ResourceSpine)

    if Position:
        Spine.setLocalPosition(Position)

    if InitialAnimationName and InitialState:
        if not Spine.isCompile():
            Spine.compile()

        Spine.setStateAnimation(InitialState, InitialAnimationName, 0.0, 1.0, Loop)

        if Enable:
            Spine.enable()

        Spine.setLoop(Loop)

        if Play:
            Spine.play()

    return Spine

def getMovieSocketPolygon(GroupName, MovieName, SocketName):
    ResourceMovie = Utils.makeResourceMovie(GroupName, MovieName)

    if ResourceMovie is None:
        return None
        pass

    ResourceShape = ResourceMovie.getSocketResourceShape(SocketName)

    if ResourceShape is None:
        return None
        pass

    Polygon = ResourceShape.getPolygon()

    return Polygon
    pass

def getMovieSocketPolygonWM(GroupName, MovieName, SocketName, Position):
    MovieNode = Utils.makeMovieNode(GroupName, MovieName, Position=Position)

    if MovieNode is None:
        return None
        pass

    MovieNode.compile()

    Socket = MovieNode.getSocket(SocketName)

    if Socket is None:
        Mengine.destroyNode(MovieNode)

        return None
        pass

    Socket.compile()

    Polygon = Socket.getWorldPolygon()

    Mengine.destroyNode(MovieNode)

    return Polygon
    pass

def getMovieSocketPolygonWM2(Movie, SocketName):
    MovieEntity = Movie.getEntity()

    Socket = MovieEntity.getSocket(SocketName)

    if Socket is None:
        return None
        pass

    if not Socket.isCompile():
        Socket.compile()

    Polygon = Socket.getWorldPolygon()

    return Polygon
    pass

def getMovieSocketWidth(movie, socket_name):
    socket = movie.getSocket(socket_name)
    bounding_box = Mengine.getHotSpotPolygonBoundingBox(socket)
    return getBoundingBoxWidth(bounding_box)

def getMovieSocketHeight(movie, socket_name):
    socket = movie.getSocket(socket_name)
    bounding_box = Mengine.getHotSpotPolygonBoundingBox(socket)
    return getBoundingBoxHeight(bounding_box)

def getBoundingBoxWidth(bounding_box):
    return bounding_box.maximum.x - bounding_box.minimum.x

def getBoundingBoxHeight(bounding_box):
    return bounding_box.maximum.y - bounding_box.minimum.y

def attachMovieSlotNode(Movie, SlotName, Node):
    Slot = Movie.getMovieSlot(SlotName)

    if Slot is None:
        return False
        pass

    Slot.addChild(Node)

    return True
    pass

def getMovieLayerPosition(GroupName, MovieName, LayerName):
    ResourceMovie = Utils.makeResourceMovie(GroupName, MovieName)

    if ResourceMovie is None:
        return None
        pass

    Position = ResourceMovie.getLayerPosition(LayerName)

    return Position
    pass

def clearMovieSlots(Movie):
    if Movie is None:
        return
        pass

    if Movie.isActive() is False:
        return
        pass

    MovieEntity = Movie.getEntity()

    slots = MovieEntity.getSlots()

    for movie, name, slot in slots:
        slot.destroyChildren()
        pass
    pass

def make_functor(params, name, args="Args", kwds="Kwds"):
    Fn = params.get(name)

    if Fn is None:
        return None
        pass

    Args = params.get(args, ())
    Kwds = params.get(kwds, {})

    return FunctorStore(Fn, Args, Kwds)
    pass

def is_valid_functor_args(Fn, Count):
    if Fn is None:
        return False
        pass

    if isinstance(Fn, FunctorStore) is False:
        return False
        pass

    if callable(Fn.fn) is False:
        return False
        pass

    return Utils.is_valid_function_args(Fn.fn, len(Fn.args) + len(Fn.kwargs) + Count)
    pass

def is_valid_function_args(Fn, Count):
    import types

    if isinstance(Fn, types.MethodType) is True:
        if Fn.func_code.co_flags & 4:
            return True
            pass

        if Fn.func_code.co_flags & 8:
            return True
            pass

        fn_argcount = Fn.func_code.co_argcount
        fn_argtake = Count + 1
        fn_default = len(Fn.func_defaults or ())

        if fn_argtake > fn_argcount or fn_argcount - fn_argtake > fn_default:
            return False
            pass
        pass
    elif isinstance(Fn, types.UnboundMethodType) is True or isinstance(Fn, types.FunctionType) is True:
        if Fn.func_code.co_flags & 4:
            return True
            pass

        if Fn.func_code.co_flags & 8:
            return True
            pass

        fn_argcount = Fn.func_code.co_argcount
        fn_argtake = Count
        fn_default = len(Fn.func_defaults or ())

        if fn_argtake > fn_argcount or fn_argcount - fn_argtake > fn_default:
            return False
            pass
        pass

    return True
    pass

def id_maker(count):
    """
    :param count: integer > 1
    :return:
    random eternal sequence made from chunks of length count
    1. last element of chunk and first element of next chunk always different
    2. chunk consists of unique elements from 0 to count-1
    3. returns None-sequence if input is shit

    example:
    input: count=5
    output: 5 different numbers, with last number for example, 3; then 5 another numbers, but first of them is not 3

    usage:
    ids = Utils.id_maker(4)
    rand_id = ids.next()
    """
    if count == 1:
        while True:
            yield 0
    elif count > 1:
        ids = rand_list(range(count))
        while True:
            for index in ids:
                yield index
                pass
            last = ids[-1]
            ids = rand_list(ids)
            if ids[0] == last:
                rand_index = Mengine.range_rand(1, count)
                ids[0], ids[rand_index] = ids[rand_index], ids[0]
                pass
            pass
        pass
    else:
        while True:
            yield None
    pass

def importType(module, type):
    ModuleName = None

    if module == "":
        ModuleName = type
    else:
        ModuleName = "%s.%s" % (module, type)
        pass

    Module = None

    try:
        if module == "":
            Module = __import__(ModuleName)
        else:
            Module = __import__(ModuleName, fromlist=[module])
            pass
    except ImportError as se:
        traceback.print_exc()

        Trace.log("Manager", 0, "Utils.importType %s:%s import error: '%s'" % (module, type, se))

        return None
    except Exception as se:
        traceback.print_exc()

        Trace.log("Manager", 0, "Utils.importType %s:%s some error: '%s'" % (module, type, se))

        return None
        pass

    Type = None

    try:
        Type = getattr(Module, type)
    except AttributeError as ex:
        Trace.log("Manager", 0, "Utils.importType %s:%s module not found type: '%s'" % (module, type, ex))
        pass

    return Type
    pass

def debug_print(msg, object):
    print('-' * 30 + '] %s' % msg)
    print('Value =', object)
    print('type(Value) =', type(object))
    try:
        print('Value.__name__', object.__name__)
    except AttributeError:
        pass

def debug_dir(object):
    print('-' * 30 + '] dir(%s)' % str(object))

    for name in dir(object):
        print(name)

    print('-' * 30 + '] End of dir')

class DebugPrinter(object):
    def __init__(self, msg='-' * 10):
        self.msg = msg

    def __enter__(self):
        print('-' * 10 + self.msg + '-' * 10 + ']Deeeeebug Begin')

    def __exit__(self, *args):
        print('-' * 10 + self.msg + '-' * 10 + ']Deeeeebug End')

def make_text_node(name, text_id, font=None, v_align=None, h_align=None, *args):
    # create node
    text_field = Mengine.createNode('TextField')
    text_field.setName(name)
    # setup aligning
    if v_align is not None:
        if v_align == 'Bottom':
            text_field.setVerticalBotomAlign()
        elif v_align == 'Center':
            text_field.setVerticalCenterAlign()
        elif v_align == 'Top':
            text_field.setVerticalTopAlign()
        else:
            Trace.log("Entity", 0, "Utils.make_text_node invalid vertical align mode '{}'".format(v_align))
    if h_align is not None:
        if h_align == 'Left':
            text_field.setHorizontalLeftAlign()
        elif h_align == 'Center':
            text_field.setHorizontalCenterAlign()
        elif h_align == 'Right':
            text_field.setHorizontalRightAlign()
        else:
            Trace.log("Entity", 0, "Utils.make_text_node invalid horizontal align mode '{}'".format(h_align))
    # setup font
    if font is not None:
        text_field.setFontName(font)
    # setup text format args
    if args is None:
        text_field.removeTextFormatArgs()
    elif isinstance(args, tuple) is True:
        text_field.setTextFormatArgs(*args)
    else:
        text_field.setTextFormatArgs(args)

def getCurrentPlatformParams():
    """ :returns: dict where keys are 'Android', 'IOS', 'WINDOWS' and values is bool """
    # todo: return to 'platform' when crushes disappear
    option = "platforma"

    platforms = {
        "Android": _ANDROID is True or Mengine.getOptionValue(option) == "android",
        "IOS": _IOS is True or Mengine.getOptionValue(option) == "ios",
        "WINDOWS": (_WINDOWS is True or Mengine.getOptionValue(option) == "windows") and Mengine.hasTouchpad() is False,
        "MAC": (_MACOS is True or Mengine.getOptionValue(option) == "mac") and Mengine.hasTouchpad() is False
    }
    if True not in platforms.values():
        Trace.msg("!!!! Utils.getCurrentPlatformParams: remove -touchpad or add -{}:android|ios".format(option))
        Trace.msg("!!!! Utils.getCurrentPlatformParams: set Platform to 'WINDOWS' until you fix the conflict")
        platforms["WINDOWS"] = True
    return platforms

def getCurrentPlatform():
    """ :returns: 'Android' or 'IOS' or 'WINDOWS' """
    platforms = getCurrentPlatformParams()
    __active_platforms = [p for (p, v) in platforms.items() if v is True]
    cur_platform = __active_platforms[0]
    return cur_platform

def getCurrentPublisher():
    """ :returns: publisher name from Config or -pub param """
    publisher = Mengine.getOptionValue("pub") or Mengine.getGameParamUnicode("Publisher") or None
    return publisher

def getCurrentBusinessModel():
    """ :returns: 'Free' or 'Premium' """
    possible_models = ["Free", "Premium"]

    def _fit(value):
        val = str(value).title()
        if val not in possible_models:
            return None
        return val

    business_model = _fit(Mengine.getConfigString("Monetization", "Model", "undefined"))
    test_model = _fit(Mengine.getOptionValue("monetization"))

    return test_model or business_model or possible_models[0]

def getCurrentBuildMode():
    """ :returns: build mode name from Configs.json or -buildmode param """
    buildmode = Mengine.getOptionValue("buildmode") or Mengine.getGameParamUnicode("BuildMode") or None
    return buildmode

def getCurrentBuildVersion():
    """ :returns: _BUILD_VERSION from Mengine or -version param or None """
    build_version = _BUILD_VERSION

    if Mengine.getOptionValue("version") != "":
        build_version = Mengine.getOptionValue("version")

    return build_version

def getCurrentBuildVersionNumber():
    """ :returns: _BUILD_VERSION_NUMBER from Mengine or -version param converted to number or None """
    build_version_number = _BUILD_VERSION_NUMBER

    custom_version = Mengine.getOptionValue("version")
    if custom_version != "":
        if custom_version == "0":
            build_version_number = int(custom_version)
        else:
            build_version_number = getNumberFromVersion(custom_version)

    return build_version_number

def getNumberFromVersion(version):
    """ :returns: int(hex-string) version from string version type *.*.* or None """
    import re

    if type(version) == str and "." in version and not re.search("[a-zA-Z]", version):
        split_in = version.split(".")
        split_out = []

        for char in split_in:
            split_out.append(format(int(char), "0{}".format(4 if char == split_in[0] else 2)))

        version_number = int("0x" + "".join(char for char in split_out), 0)
        return version_number

    return None

class SimpleLogger(object):
    """ Usage example:

        >> _Log = SimpleLogger("Utils")
        >> _Log("test error message!!!", err=True)
        >> # output in log (red color):
        <Utils> test error message!!!
    """

    def __init__(self, title, **kwargs):
        """
            Parameters:
                title (str): what title will be in square brackets (i.e. <Utils>);
                debug (bool): (default=True) messages will be printed only in _DEVELOPMENT if True;
                enable (bool): (default=True) enable logger or not;
                option (str): logs only if with call kwarg `optional=True` and -debug:<option>
        """
        self.title = title

        self._debug = kwargs.get("debug", True)
        self._enable = kwargs.get("enable", True)
        self._optional = False

        option = kwargs.get("option")
        if option is not None and option in Mengine.getOptionValues("debug"):
            self._optional = True

    def __call__(self, msg, err=False, force=False, optional=False):
        if self._enable is False:
            return
        if force is False:
            if self._debug is True:
                if _DEVELOPMENT is False:
                    return
                if optional is True and self._optional is False:
                    return

        f_message = " <%s> %s" % (self.title, msg)
        if err is True:
            Trace.msg_err(f_message)
        else:
            Trace.msg(f_message)

def isCollectorEdition():
    if Mengine.getGameParamUnicode("BuildModeCheckVersion") == u"2.0":
        from Foundation.BuildModeManager import BuildModeManager

        current_build_mode = Mengine.getGameParamUnicode("BuildMode")
        resources_tags = BuildModeManager.getBuildResourceConfig(current_build_mode)
        return "CE" in resources_tags
    else:
        return Mengine.getGameParamBool("CollectorEdition", False)

def isSurvey():
    if Mengine.getGameParamUnicode("BuildModeCheckVersion") == u"2.0":
        from Foundation.BuildModeManager import BuildModeManager

        current_build_mode = Mengine.getGameParamUnicode("BuildMode")
        resources_tags = BuildModeManager.getBuildResourceConfig(current_build_mode)
        return all(["Survey" in resources_tags, "CE" not in resources_tags, "SE" not in resources_tags])
    else:
        return Mengine.getGameParamBool("Survey", False)

def setEnableLayer(state, layer_name, parent_obj):
    disable_layers = parent_obj.getParam("DisableLayers")
    if state is True and layer_name in disable_layers:
        parent_obj.delParam("DisableLayers", layer_name)
    elif state is False and layer_name not in disable_layers:
        parent_obj.appendParam("DisableLayers", layer_name)

def calcTime(time_in_sec):
    """ :returns: days, hours, min, sec """

    sec = time_in_sec % 60
    min = time_in_sec // 60
    hours = min // 60
    min = min % 60
    days = hours // 24
    hours = hours % 24

    return days, hours, min, sec

def calcTime2(time_in_sec):
    """ Python 2 returns: hours, min, sec """

    hours = time_in_sec / 3600
    min = (time_in_sec % 3600) / 60
    sec = (time_in_sec % 3600) % 60

    return hours, min, sec

def benchmark(func):
    def wrapper(*args, **kwargs):
        start = Mengine.getTimeMs()
        return_value = func(*args, **kwargs)
        end = Mengine.getTimeMs()
        Trace.msg('[*] Runtime: {} ms.'.format(end - start))
        return return_value
    return wrapper

def replace_last(string, old, new, n, already_reverted_substrings=False):
    """ replaces last `n` substrings `old` to `new` in input `string`
        Example:
            >>> before = "I want two first args: %s %s %s and %s"
            >>> after = replace_last(before, "%s", "_", 2)
            >>> print(after)    # "I want two first args: %s %s _ and _"
    """
    if already_reverted_substrings is True:
        _old, _new = old, new
    else:
        _old, _new = old[::-1], new[::-1]

    replaced = string[::-1].replace(_old, _new, n)[::-1]
    return replaced

def getWeightedRandomIndex(weights):
    if len(weights) == 0:
        return None
    if len(weights) == 1:
        return 0

    total_weight = sum(weights)
    random_weight = Mengine.range_randf(0, total_weight)

    for i, weight in enumerate(weights):
        random_weight -= weight
        if random_weight <= 0:
            return i

def getWeightedRandomByKey(records, key):
    if len(records) == 0:
        return None

    elements, weights = [], []
    for record in records:
        if hasattr(record, key) is False:
            continue
        elements.append(record)
        weights.append(getattr(record, key))

    lookup_index = getWeightedRandomIndex(weights)

    if lookup_index is None:
        return None

    element = elements[lookup_index]

    return element
