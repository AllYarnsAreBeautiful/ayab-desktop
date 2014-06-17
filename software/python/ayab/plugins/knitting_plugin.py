from yapsy.IPlugin import IPlugin
from fysom import Fysom


class KnittingPlugin(IPlugin):

  def __init__(self):
    """
    Args:
        _fsm: The internal finite state machine.
    """
    # callbacks_dict = {
    #          'onknit': onknit,
    #          'onknitting': onknitting,
    #          'onconfigure': onconfigure,
    #          'onfinish': onfinish
    #         }
    callbacks_dict = {}
    #self.fysom = False
    self._fsm = Fysom(
        {'initial': 'activated',
         'events': [
             {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
             {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
             {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
         ],
         'callbacks':  callbacks_dict
         })
