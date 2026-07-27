_DRAGGING_MODES = {
    'none': Mengine.EVADM_NONE,
    'free': Mengine.EVADM_FREE,
    'horizontal': Mengine.EVADM_HORIZONTAL,
    'vertical': Mengine.EVADM_VERTICAL,
}

DUNGEON_VIRTUAL_AREA_FRICTION_BASE = 0.001
DUNGEON_VIRTUAL_AREA_FRICTION_FACTOR = 0.009


def createVirtualArea(name='VirtualArea', enable_scale=True, scale_factor=0.375,
                      content_size=(0.0, 0.0, 2736.0, 1536.0), friction=0.5,
                      friction_base=DUNGEON_VIRTUAL_AREA_FRICTION_BASE,
                      friction_factor=DUNGEON_VIRTUAL_AREA_FRICTION_FACTOR,
                      rigidity=0.5, dragging_mode='free', max_scale=6.0,
                      disable_drag_if_invalid=True, drag_start_threshold=2.0,
                      allow_out_of_bounds=True):
    mode = _DRAGGING_MODES.get(dragging_mode)
    if mode is None:
        raise TypeError('"%s" dragging mode is not supported' % dragging_mode)

    virtual_area = Mengine.createNode('VirtualArea')
    virtual_area.setName(name)
    virtual_area.setVirtualAreaScaleEnable(enable_scale)
    virtual_area.setVirtualAreaWheelScaleFactor(scale_factor)
    virtual_area.setVirtualAreaContentSize(*content_size)
    virtual_area.setVirtualAreaFriction(friction)
    virtual_area.setVirtualAreaFrictionBase(friction_base)
    virtual_area.setVirtualAreaFrictionFactor(friction_factor)
    virtual_area.setVirtualAreaRigidity(rigidity)
    virtual_area.setVirtualAreaDraggingMode(mode)
    virtual_area.setVirtualAreaMaxScaleFactor(max_scale)
    virtual_area.setVirtualAreaDisableDragIfInvalid(disable_drag_if_invalid)
    virtual_area.setVirtualAreaDragStartThreshold(drag_start_threshold)
    virtual_area.setVirtualAreaAllowOutOfBounds(allow_out_of_bounds)

    return virtual_area


def setupVirtualAreaWithMovie(virtual_area, movie, socket_name, slot_name=None, default_handle=None):
    socket = movie.getSocket(socket_name)
    virtual_area.setVirtualAreaViewportFromHotSpot(socket)

    attach_to_node = movie.getEntityNode()
    if slot_name is not None:
        slot = movie.getMovieSlot(slot_name)
        if slot is not None:
            attach_to_node = slot

    attach_to_node.addChild(virtual_area)

    if default_handle is not None:
        socket.setDefaultHandle(default_handle)
        virtual_area.setVirtualAreaDefaultHandle(default_handle)

    return socket


def destroyVirtualArea(virtual_area):
    virtual_area.removeFromParent()
    Mengine.destroyNode(virtual_area)
