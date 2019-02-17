import mymaya.lib.dock as dock
import mymaya.lib.object as object
from PySide2 import QtGui, QtCore, QtWidgets
import maya.api.OpenMaya as om2

def new_obj():
    '''
    Entry point to call ui from maya.
    '''
    NewObjDockManager.show()

class NewObjDockManager(dock.DockManager):
    '''
    overridden
    '''
    def __init__(self):
        super(NewObjDockManager, self).__init__()
        self.window_name = 'new_obj_window'
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                           main_widget_cls=NewObjMainWidget,
                                                           title='New Obj')

class NewObjMainWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        Main widget
        '''
        super(NewObjMainWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.obj_list = QtWidgets.QListWidget()
        layout.addWidget(self.obj_list)
        btn_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(btn_layout)
        create_cube_btn = QtWidgets.QPushButton('Create Cube')
        create_sphere_btn = QtWidgets.QPushButton('Create Sphere')
        create_circle_btn = QtWidgets.QPushButton('Create Circle')
        btn_layout.addWidget(create_cube_btn)
        btn_layout.addWidget(create_sphere_btn)
        btn_layout.addWidget(create_circle_btn)

        # signal
        create_cube_btn.pressed.connect(self.request_create_cube)
        create_sphere_btn.pressed.connect(self.request_create_sphere)
        create_circle_btn.pressed.connect(self.request_create_circle)

        om2.MUserEventMessage.addUserEventCallback(object.NEW_PRIM_EVENT, self.received_create)

    def received_create(self, obj):
        if obj:
            obj = obj[0]
            self.obj_list.addItem(obj.name())

    def request_create_cube(self):
        object.new_prim('cube')

    def request_create_sphere(self):
        object.new_prim('sphere')

    def request_create_circle(self):
        object.new_prim('circle')


def new_type():
    '''
    Entry point to call ui from maya.
    '''
    NewTypeDockManager.show()

class NewTypeDockManager(dock.DockManager):
    '''
    overridden
    '''

    def __init__(self):
        super(NewTypeDockManager, self).__init__()
        self.window_name = 'new_type_window'
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                main_widget_cls=NewTypeMainWidget,
                                                title='New Type')

class NewTypeMainWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        Main widget
        '''
        super(NewTypeMainWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.type_list = QtWidgets.QListWidget()
        layout.addWidget(self.type_list)

        om2.MUserEventMessage.addUserEventCallback(object.NEW_PRIM_EVENT, self.received_create)

    def received_create(self, obj):
        if obj:
            shape = obj[1]
            self.type_list.addItem(shape.type())