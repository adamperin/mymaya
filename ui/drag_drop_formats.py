from PySide2 import QtCore, QtWidgets, QtGui
import pylib.paths
import pymel.core as pm
import maya.OpenMayaUI as omui
import pylib.config_core
import pylib.ui.qt
# hold the drag drop manager so that qt doesnt grabage collect it. Could possibly be parented to maya
drag_drop_manager = None

class DragDropManager(QtCore.QObject):
    '''
    Adds functionlity to maya to allow for arch model formats to be drag and dropped into view panes in maya.
    '''
    
    ArchIcon = QtGui.QIcon(pylib.config_core.toolsroot().join('resource', 'img', 'arch_icon.svg'))
    
    def __init__(self):
        super(DragDropManager, self).__init__()
        global drag_drop_manager
        drag_drop_manager = self
        self._qt_model_editors = []
        self._parent_qt = [qt_object for qt_object in pm.uitypes.toQtObject('MainPane|viewPanes').children() if qt_object.objectName() == 'mayaLayoutInternalWidget']
        for qt_object in self._parent_qt:
            qt_object.installEventFilter(self)
        pm.uitypes.toQtObject('MayaWindow').installEventFilter(self)
        
        self._menu = pm.popupMenu(p='MayaWindow')
        self._qt_menu = pm.uitypes.toQtControl(self._menu)

        self.update()
        
    def update(self):
        '''
        install event filter on all new model editors
        :return:
        '''
        
        for ui in pm.getPanel(type='modelPanel'):
            qt_model_editor_parent = pm.uitypes.toQtObject(ui)
            if qt_model_editor_parent:
                mixin_ptr = omui.MQtUtil.findControl(qt_model_editor_parent.objectName())
                full_name = omui.MQtUtil.fullName(long(mixin_ptr))
                qt_model_editor = pm.uitypes.toQtObject('{0}|{1}|{1}'.format(full_name, ui.shortName()))
                if qt_model_editor:
                    if qt_model_editor not in self._qt_model_editors:
                        qt_model_editor.installEventFilter(self)
                        self._qt_model_editors.append(qt_model_editor)
                elif qt_model_editor_parent not in self._qt_model_editors:
                    qt_model_editor_parent.installEventFilter(self)
                    self._qt_model_editors.append(qt_model_editor_parent)

    def eventFilter(self, obj, event):
        '''
        Event filter to watch for drop events on model editors as well as new qt children being added to mayaWindow or model editors parent
        :param obj:
        :param event:
        :return:
        '''
        
        if obj in self._parent_qt or obj.objectName() == 'MayaWindow':
            if event.type() == QtCore.QEvent.ChildAdded:
                pm.evalDeferred('{0}.{1}.update()'.format(self.__module__, 'drag_drop_manager'))
        else:
            if event.type() == QtCore.QEvent.Drop:
                mime_data = event.mimeData()
                if mime_data.hasUrls:



                    for url in mime_data.urls()
                        if any( for )
                        if url.toLocalFile().endsWith()

                    maya_paths = [url.toLocalFile() for url in mime_data.urls() if url.toLocalFile().ext == '.ma' or pylib.paths.Path(url.toLocalFile()).ext == '.mb']
                    model_paths = [pylib.paths.Path(url.toLocalFile()) for url in mime_data.urls() if pylib.paths.Path(url.toLocalFile()).ext == '.model']
                    if model_paths or maya_paths:
                        
                        pm.uitypes.PopupMenu(self._menu).deleteAllItems()
                        
                        maya_paths.extend(self.getMayaFilePathsFromArchFormat(model_paths))
                        
                        modelImportAction = QtWidgets.QAction('import arch formats', self)
                        self._qt_menu.addAction(modelImportAction)
                        modelImportAction.setIcon(self.ArchIcon)
                        modelImportAction.triggered.connect(lambda: self.importArchFormats(model_paths))
                        
                        modelOpenAction = QtWidgets.QAction('open arch formats', self)
                        modelOpenAction.setIcon(self.ArchIcon)
                        self._qt_menu.addAction(modelOpenAction)
                        modelOpenAction.triggered.connect(lambda: self.openModels(model_paths))
                        
                        if not model_paths:
                            modelImportAction.setEnabled(False)
                            modelOpenAction.setEnabled(False)
                    
                        maya_paths = list(set(maya_paths))
                        maFromModelImportAction = QtWidgets.QAction('import maya files', self)
                        self._qt_menu.addAction(maFromModelImportAction)
                        maFromModelImportAction.setIcon(QtGui.QIcon(':/mayaIcon.png'))
                        maFromModelImportAction.triggered.connect(lambda: self.importMayaFile(maya_paths))
                        
                        if not maya_paths:
                            maFromModelImportAction.setEnabled(False)
                        
                        for mayaPath in maya_paths:
                            maFromModelOpenAction = QtWidgets.QAction('open maya file: {0}'.format(mayaPath.name), self)
                            self._qt_menu.addAction(maFromModelOpenAction)
                            maFromModelOpenAction.setIcon(QtGui.QIcon(':/mayaIcon.png'))
                            maFromModelOpenAction.triggered.connect(lambda path=mayaPath: self.openMayaFile(path))
                            
                        self._qt_menu.popup(QtGui.QCursor.pos())
                        return True
                        
            if event.type() == QtCore.QEvent.DeferredDelete:
                self._qt_model_editors.remove(obj)
        return False

    def openMayaFile(self, path):
        '''
        open a single maya file
        :param path:
        :return:
        '''
        
        if path.exists():
            if path.ext == '.ma':
                pm.mel.eval('openRecentFile("{0}", "mayaAscii")'.format(path))
            elif path.ext == '.mb':
                pm.mel.eval('openRecentFile("{0}", "mayaBinary")'.format(path))
        else:
            msgBox = pylib.ui.qt.ArchMessageBox(iconType='warning', buttons=['Ok'])
            msgBox.setWindowTitle('Open Maya File')
            msgBox.setText('Maya Scene does not exist:\n\n{0}'.format(path))
            msgBox.exec_()
        
    def importMayaFile(self, paths):
        '''
        Imports maya files
        :param list paths: pylib.paths.Path maya files paths
        :return:
        '''
        
        invalidPaths = ''
        for path in paths:
            
            if path.exists():
                pm.mel.eval('performFileDropAction ("{0}")'.format(path))
            else:
                
                invalidPaths += str(path) + '\n'
        
        if invalidPaths:
            msgBox = pylib.ui.qt.ArchMessageBox(iconType='warning', buttons=['Ok'])
            msgBox.setWindowTitle('Import Maya Files')
            msgBox.setText('Maya Scene(s) do not exist and could not be imported:\n\n{0}'.format(invalidPaths))
            msgBox.exec_()
