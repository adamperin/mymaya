from PySide2 import QtCore, QtWidgets, QtGui
import pymel.core as pm
# hold the drag drop manager so that qt doesnt grabage collect it. Could possibly be parented to maya
drag_drop_manager = None

class NewChildManager(QtCore.QObject):
    '''

    '''
    def __init__(self):
        super(NewChildManager, self).__init__()
        global drag_drop_manager
        drag_drop_manager = self
        self.app = QtWidgets.QApplication.instance()
        self.app.installEventFilter(self)

    def eventFilter(self, obj, event):
        '''
        Event filter to watch for new qt children being added to application
        :param obj:
        :param event:
        :return:
        '''
        if event.type() == QtCore.QEvent.ChildAdded:
            pass
            # for widget in self.app.topLevelWidgets():
            #     widget.show()
        return False