import mymaya.lib.dock as dock
import mymaya.lib.message as lib_msg
from PySide2 import QtWidgets
import maya.api.OpenMaya as om2

def message_list():
    '''
    Entry point to call ui from maya.
    '''
    MessageListDockManager.show()

class MessageListDockManager(dock.DockManager):
    '''
    overridden
    '''
    def __init__(self):
        super(MessageListDockManager, self).__init__()
        self.window_name = 'message_list_window'
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                           main_widget_cls=MessageListMainWidget,
                                                           title='Message')

class MessageListMainWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MessageListMainWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.msg_list = QtWidgets.QListWidget()
        layout.addWidget(self.msg_list)

        om2.MUserEventMessage.addUserEventCallback(lib_msg.MESSAGE_EVENT, self.receive_msg)

    def receive_msg(self, msg):
        self.msg_list.addItem(msg)

def message_status():
    '''
    Entry point to call ui from maya.
    '''
    MessageStatusDockManager.show()

class MessageStatusDockManager(dock.DockManager):
    '''
    overridden
    '''

    def __init__(self):
        super(MessageStatusDockManager, self).__init__()
        self.window_name = 'message_status_window'
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                main_widget_cls=MessageStatusMainWidget,
                                                title='Message')

class MessageStatusMainWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MessageStatusMainWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.msg_status = QtWidgets.QStatusBar()
        self.msg_status.setStyleSheet('color:red')
        layout.addWidget(self.msg_status)

        om2.MUserEventMessage.addUserEventCallback(lib_msg.MESSAGE_EVENT, self.receive_msg)

    def receive_msg(self, msg):
        self.msg_status.showMessage(msg, 5000)

def  messenger():
    '''
    Entry point to call ui from maya.
    '''
    MessengerDockManager.show()

class MessengerDockManager(dock.DockManager):
    '''
    overridden
    '''

    def __init__(self):
        super(MessengerDockManager, self).__init__()
        self.window_name = 'messenger_window'
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                main_widget_cls=MessengerMainWidget,
                                                title='Messenger')

class MessengerMainWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MessengerMainWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.msg_text_edit = QtWidgets.QTextEdit()
        send_btn = QtWidgets.QPushButton('send')
        layout.addWidget(self.msg_text_edit)
        layout.addWidget(send_btn)
        send_btn.clicked.connect(self.request_msg)
        om2.MUserEventMessage.addUserEventCallback(lib_msg.MESSAGE_EVENT, self.receive_msg)

    def receive_msg(self, msg):
        self.msg_text_edit.clear()

    def request_msg(self):
        msg = self.msg_text_edit.toPlainText()
        lib_msg.send_message(msg)
