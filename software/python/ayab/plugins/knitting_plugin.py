from yapsy.IPlugin import IPlugin
from fysom import Fysom


__NOT_IMPLEMENTED_ERROR = "Classes that inherit from KnittingPlugin should implment {0}"


class KnittingPlugin(IPlugin, Fysom):
  '''A generic plugin implementing a state machine for knitting.'''

  def onknit(self, e):
    """Called when state machine executes knit()"""
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("onknit is used for the main 'knitting loop'"))

  def onfinish(self, e):
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("onfinish is a callback that is called when knitting is over"))

  def onconfigure(self, e):
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("onconfigure is used to configure the knitting plugin before starting"))

  def __init__(self, callbacks_dict):
    """
    Args:
        _fsm: The internal finite state machine.
    """
    Fysom.__init__(self,
        {'initial': 'activated',
         'events': [
             {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
             {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
             {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
         ],
         'callbacks':  callbacks_dict
         })
    # callbacks_dict = {
    #          'onknit': onknit,
    #          'onknitting': onknitting,
    #          'onconfigure': onconfigure,
    #          'onfinish': onfinish
    #         }
