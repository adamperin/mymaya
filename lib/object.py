import pymel.core as pm
import maya.api.OpenMaya as om2

NEW_PRIM_EVENT = 'new_prim'
if not om2.MUserEventMessage.isUserEvent(NEW_PRIM_EVENT):
    om2.MUserEventMessage.registerUserEvent(NEW_PRIM_EVENT)

def new_prim(type):
    prim = None
    if type == 'cube':
        prim = pm.polyCube()
    elif type == 'sphere':
        prim = pm.polySphere()
    elif type == 'circle':
        prim = pm.circle()
    om2.MUserEventMessage.postUserEvent('new_prim', prim)

