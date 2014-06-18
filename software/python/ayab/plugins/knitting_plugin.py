from yapsy.IPlugin import IPlugin
from fysom import Fysom


class KnittingPlugin(IPlugin, Fysom):

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
