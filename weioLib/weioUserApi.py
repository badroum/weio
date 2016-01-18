from __future__ import print_function
from threading import Lock, RLock
import sys, os

#####################
# WeIO User Classes
#####################
###
# LockProxy is used to lock methods of inherited class
# Example of usage:
# lockedset = LockProxy(set([1,2,3]))
###
class LockProxy(object):
    def __init__(self, obj):
        self.__obj = obj
        self.__lock = RLock()
        # RLock because object methods may call own methods
    def __getattr__(self, name):
        def wrapped(*a, **k):
            with self.__lock:
                getattr(self.__obj, name)(*a, **k)
        return wrapped

###
# Locking can be done with class decorators
###
def lockedMethod(method):
    """Method decorator. Requires a lock object at self._lock"""
    def newmethod(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return newmethod

###
# Thread-safe (locaked) print
###
class WeioPrint():
    def __init__(self, *args, **kwargs):
        self._lock = Lock()

    @lockedMethod
    def output(self, *args, **kwargs):
        print(*args, **kwargs)

        # Flush the file or stdout
        if (kwargs.get('file') != None):
            kwargs['file'].flush()
        else:
            sys.stdout.flush()


class WeioSharedVar(object):
    def __init__ (self, procFnc, procArgs) :
        self.dict = None
        self.Val = None
        self.Array = None
    pass

class WeioApiProcess():
    def __init__ (self, procFnc, procArgs) :
        self.procFnc = procFnc
        self.procArgs = procArgs

class WeioApiEvent():
    def __init__ (self, event, handler) :
        self.event = event
        self.handler = handler

class WeioApiInterrupt():
    def __init__ (self, pin, edge, handler) :
        self.pin = pin
        self.edge = edge
        self.handler = handler

class WeioAttach():
    def __init__(self):
        self.procs = {}
        self.events = {}
        self.ints = {}

    def process(self, procFnc, procArgs=()):
        proc = WeioApiProcess(procFnc, procArgs)
        procId = procFnc.__name__
        self.procs[procId] = proc

    def event(self, event, handler):
        e = WeioApiEvent(event, handler)
        self.events[event] = e

    def interrupt(self, pin, edge, handler):
        intr = WeioApiInterrupt(pin, edge, handler)
        self.ints[pin] = intr

class WeioClient():
    def __init__(self, info, connection):
        self.info = info
        self.connection = connection

class WeioServerMsg():
    def __init__(self, qout, msg):
        # Create userAgentMessage and send it to the launcher process
        self.qout = qout
        self.msg = msg

    def send(self, callback, data, connUuid):
        self.msg.connUuid = connUuid
        self.msg.req = "serverPush"
        self.msg.res = data
        self.msg.callbackJS = callback

        # Send message to launcher process
        self.qout.put(self.msg)

    def broadcast(self, callback, data):
        self.msg.connUuid = "all"
        self.msg.req = "serverPush"
        self.msg.res = data
        self.msg.callbackJS = callback

        # Send message to launcher process
        self.qout.put(self.msg)

def serverPush(callback, data):
    weioServerMsg.broadcast(callback, data)


###
# Global instances
###
attach = None
console = None

# Global shared dict
sharedVar = None

# Global connections
weioConns = None

# Global WeIO gpio object
gpio = None

# serverPush variable
weioServerMsg = None
