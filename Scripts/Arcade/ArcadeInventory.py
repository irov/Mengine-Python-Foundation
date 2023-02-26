from Foundation.Initializer import Initializer
from Foundation.Task.TaskGenerator import TaskSource
from Foundation.TaskManager import TaskManager

class ArcadeInventorySlot(Initializer):
    def __init__(self):
        super(ArcadeInventorySlot, self).__init__()
        self.node = None
        self.item = None

        self.socket_node = None
        self.item_node = None
        pass

    def _onInitialize(self, slot, **props):
        super(ArcadeInventorySlot, self)._onInitialize(slot)

        node = slot.createChild("Interender")
        node.enable()

        self.socket_node = node

        node = slot.createChild("Interender")
        node.enable()

        self.item_node = node

        self.parentInventory = props.get("parentInventory")
        pass

    def _onFinalize(self):
        super(ArcadeInventorySlot, self)._onFinalize()
        if self.socket_node is not None:
            Mengine.destroyNode(self.socket_node)
            self.socket_node = None
            pass

        if self.item_node is not None:
            Mengine.destroyNode(self.item_node)
            self.item_node = None
            pass
        pass

    def getSocket(self):
        return None
        pass

    def setSocket(self, socket):
        self.socket_node.addChild(socket)
        pass

    def enableSocket(self, value):
        if value is True:
            self.socket_node.enable()
            pass
        else:
            self.socket_node.disable()
            pass
        pass

    def hasItem(self):
        return self.item is not None
        pass

    def setItem(self, item):
        self.item = item
        if item:
            item.slot = self
            pass
        pass

    def getItem(self):
        return self.item
        pass

    def onSlotCheckDrag(self, source_effect, item):
        return True
        pass

    def onSlotPickEnter(self):
        pass

    def onSlotPickLeave(self):
        pass

    def onSlotUseEnter(self, slot):
        pass

    def onSlotUseLeave(self, slot):
        pass

    def onSlotItemPop(self, source):
        item = self.item
        self.setItem(None)
        self._onSlotItemPop(source, item)
        pass

    def onSlotItemPush(self, source, item):
        self.setItem(item)
        self.item_node.addChild(item.node)
        self._onSlotItemPush(source, item)
        pass

    def _onSlotItemPush(self, source, item):
        pass

    def _onSlotItemPop(self, source, item):
        pass

    pass

class ArcadeInventoryItem(Initializer):
    def __init__(self):
        super(ArcadeInventoryItem, self).__init__()
        self.node = None
        self.slot = None
        pass

    def _onInitialize(self, slot):
        super(ArcadeInventoryItem, self)._onInitialize(slot)

        node = Mengine.createNode("Interender")
        node.enable()

        if slot is not None:
            slot.item_node.addChild(node)
            pass

        self.node = node
        self.slot = slot
        pass

    def _onFinalize(self):
        super(ArcadeInventoryItem, self)._onFinalize()
        if self.node is not None:
            Mengine.destroyNode(self.node)
            pass

        self.node = None
        self.slot = None
        pass

    def onPrepareDragBegin(self, slot):
        pass

    def onDragBegin(self, pos):
        pass

    def onDragTracker(self, pos, delta):
        pass

    def onDragComplete(self, source, pos):
        pass

    def onDragCompleteEnd(self, source, slot_from, slot_to):
        pass

    def onDragSwitchItem(self, source, pos, item):
        return True
        pass

    def onDragReturn(self, source):
        pass
    pass

class ArcadeInventory(Initializer):
    def __init__(self):
        super(ArcadeInventory, self).__init__()
        self.node = None

        self.GroupName = None
        self.MovieName = None

        self.inventorySlots = []
        self.inventoryItems = []

        self.InventorySlotType = None

        self.friends = []
        pass

    def setGroupName(self, GroupName):
        self.GroupName = GroupName
        pass

    def setMovieName(self, MovieName):
        self.MovieName = MovieName
        pass

    def setInventorySlotType(self, InventorySlotType):
        self.InventorySlotType = InventorySlotType
        pass

    def _onInitialize(self):
        super(ArcadeInventory, self)._onInitialize()

        MovieNode = Utils.makeMovieNode(self.GroupName, self.MovieName, Important=True)

        MovieNodeSlots = MovieNode.getSlots()

        for movie, name, slot in MovieNodeSlots:
            inventorySlot = self.InventorySlotType()
            inventorySlot.onInitialize(slot, parentInventory=self)

            self.inventorySlots.append(inventorySlot)
            pass

        self.node = MovieNode
        pass

    def _onFinalize(self):
        super(ArcadeInventory, self)._onFinalize()
        pass

    def addInventoryItem(self, item):
        for slot in self.inventorySlots:
            if slot.hasItem() is True:
                continue
                pass

            item.onInitialize(slot)

            slot.setItem(item)

            return True
            pass

        return False
        pass

    def addFriendInventory(self, friend):
        self.friends.append(friend)
        pass

    def getTotalInventorySlots(self):
        inventorySlots = []
        inventorySlots.extend(self.inventorySlots)
        for friend in self.friends:
            inventorySlots.extend(friend.inventorySlots)
            pass

        return inventorySlots
        pass

    def onInventoryCheckDrag(self, source, item):
        # empty
        return True
        pass

    def onActivate(self):
        def __removeChain(isSkip):
            self.chain = None
            pass

        self.chain = TaskManager.createTaskChain(Repeat=True, Cb=__removeChain)

        totalInventorySlots = self.getTotalInventorySlots()

        with self.chain as source:
            slot_click_holder = Holder()

            with source.addRaceTask(2) as (source_over, source_click):
                with source_over.addWhileTask() as source_over_process:
                    slot_over_holder = Holder()

                    for slot, source_slot in source_over_process.addRaceTaskList(totalInventorySlots):
                        Socket = slot.getSocket()
                        source_slot.addTask("TaskNodeSocketEnter", Socket=Socket)
                        source_slot.addFunction(slot.onSlotPickEnter)
                        source_slot.addFunction(slot_over_holder.set, slot)
                        pass

                    def __leave(source, holder):
                        slot = holder.get()
                        Socket = slot.getSocket()
                        source.addTask("TaskNodeSocketLeave", Socket=Socket, Skiped=True)
                        source.addFunction(slot.onSlotPickLeave)
                        pass

                    source_over_process.addScope(__leave, slot_over_holder)
                    pass

                for slot, source_slot in source_click.addRaceTaskList(totalInventorySlots):
                    Socket = slot.getSocket()

                    def __filter(touchId, x, y, button, isDown, isPressed, slot):
                        if slot.hasItem() is False:
                            return False
                            pass

                        item = slot.getItem()

                        item.onPrepareDragBegin(slot)

                        item.onDragBegin((x, y))

                        return True
                        pass

                    source_slot.addTask("TaskNodeSocketClick", Socket=Socket, isDown=True, Filter=__filter, Args=(slot,))
                    source_slot.addFunction(slot_click_holder.set, slot)
                    pass
                pass

            source_effect_holder = Holder()

            def __init_effect_source(source_effect_holder):
                source_effect_holder.set(TaskSource([]))
                pass

            source.addFunction(__init_effect_source, source_effect_holder)

            with source.addRaceTask(4) as (source_move_up, source_over_up, source_click_up, source_click_miss):
                def __tracker(touchId, x, y, dx, dy, slot_click_holder):
                    slot = slot_click_holder.get()

                    item = slot.getItem()

                    item.onDragTracker((x, y), (dx, dy))

                    return False
                    pass

                source_move_up.addTask("TaskMouseMove", Tracker=__tracker, Args=(slot_click_holder,))

                with source_over_up.addWhileTask() as source_over_up_process:
                    slot_over_up_holder = Holder()

                    def __enter(source, slot_over_holder, slot_over_up_holder):
                        slot_over = slot_over_holder.get()

                        for slot, source_slot in source.addRaceTaskList(totalInventorySlots):
                            Socket = slot.getSocket()
                            source_slot.addTask("TaskNodeSocketEnter", Socket=Socket)
                            source_slot.addFunction(slot.onSlotUseEnter, slot_over)
                            source_slot.addFunction(slot_over_up_holder.set, slot)
                            pass
                        pass

                    source_over_up_process.addScope(__enter, slot_over_holder, slot_over_up_holder)

                    def __leave(source, slot_over_holder, slot_over_up_holder):
                        slot_over = slot_over_holder.get()
                        slot = slot_over_up_holder.get()

                        Socket = slot.getSocket()
                        source.addTask("TaskNodeSocketLeave", Socket=Socket, Skiped=True)
                        source.addFunction(slot.onSlotUseLeave, slot_over)
                        pass

                    source_over_up_process.addScope(__leave, slot_over_holder, slot_over_up_holder)
                    pass

                for slot, source_slot in source_click_up.addRaceTaskList(totalInventorySlots):
                    Socket = slot.getSocket()

                    def __filter(touchId, x, y, button, isDown, isPressed, slot, slot_click_holder, source_effect_holder):
                        slot_over = slot_click_holder.get()
                        source_effect = source_effect_holder.get()
                        slot_over_item = slot_over.getItem()

                        if self.onInventoryCheckDrag(source_effect, slot_over_item) is False:
                            return False
                            pass

                        if slot.onSlotCheckDrag(source_effect, slot_over_item) is False:
                            return False
                            pass

                        if slot.hasItem() is False:
                            slot_over_item.onDragComplete(source_effect, (x, y))

                            slot_over.onSlotItemPop(source_effect)

                            slot.onSlotItemPush(source_effect, slot_over_item)

                            slot_over_item.onDragCompleteEnd(source_effect, slot_over, slot)
                            return True
                            pass

                        slot_item = slot.getItem()

                        if slot_over.onSlotCheckDrag(source_effect, slot_item) is False:
                            return False
                            pass

                        if slot_over_item.onDragSwitchItem(source_effect, (x, y), slot_item) is False:
                            return False
                            pass

                        slot.onSlotItemPop(source_effect)
                        if slot_over != slot:
                            slot_over.onSlotItemPop(source_effect)

                        slot.onSlotItemPush(source_effect, slot_over_item)
                        if slot_over != slot:
                            slot_over.onSlotItemPush(source_effect, slot_item)

                        return True
                        pass

                    source_slot.addTask("TaskNodeSocketClick", Socket=Socket, isDown=False, isPressed=None, Filter=__filter, Args=(slot, slot_click_holder, source_effect_holder))
                    pass

                def __filter_miss(touchId, x, y, button, isDown, slot_click_holder):
                    slot = slot_click_holder.get()
                    slot_item = slot.getItem()

                    source_effect = source_effect_holder.get()
                    slot_item.onDragReturn(source_effect, (x, y))

                    return True
                    pass

                source_click_miss.addTask("TaskMouseButtonClickEnd", isDown=False, Filter=__filter_miss, Args=(slot_click_holder,))
                pass

            def __effect(source, source_effect_holder):
                source_effect = source_effect_holder.get()
                source_effect_source = source_effect.getSource()
                source.extendSource(source_effect_source)
                pass

            source.addScope(__effect, source_effect_holder)
            pass
        pass
    pass