import maya.api.OpenMaya as om2

MESSAGE_EVENT = 'message'
if not om2.MUserEventMessage.isUserEvent(MESSAGE_EVENT):
    om2.MUserEventMessage.registerUserEvent(MESSAGE_EVENT)


def send_message(msg):
    if msg:
        om2.MUserEventMessage.postUserEvent(MESSAGE_EVENT, msg)
