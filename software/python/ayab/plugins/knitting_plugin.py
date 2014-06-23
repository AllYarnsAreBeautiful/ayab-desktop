from yapsy.IPlugin import IPlugin
from fysom import Fysom


__NOT_IMPLEMENTED_ERROR = "Classes that inherit from KnittingPlugin should implment {0}"


class KnittingPlugin(IPlugin, Fysom):
  '''A generic plugin implementing a state machine for knitting.'''

  def onknit(self, e):
    """Callback when state machine executes knit()"""
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("onknit is used for the main 'knitting loop'."))

  def onfinish(self, e):
    """Callback when state machine executes finish()"""
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("onfinish is a callback that is called when knitting is over."))

  def onconfigure(self, e):
    """Callback when state machine executes configure(parent_ui = parent, options={})"""
    assert e.parent_ui
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("onconfigure is used to configure the knitting plugin before starting."))

  def setup_ui(self, ui):
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("setup_ui is used to load the knitting_options_dock panel ui for the plugin."))

  def get_configuration_from_ui(self, ui):
    """Loads options dict with a given parent QtGui object."""
    raise NotImplementedError(__NOT_IMPLEMENTED_ERROR.format("get_configuration_from_ui loads options with a given parent ui object."))

  def __init__(self, callbacks_dict):
    """
    Args:
        _fsm: The internal finite state machine.
    """
    callbacks_dict = {
        'onknit': self.onknit,
       # 'onknitting': self.onknitting,
        'onconfigure': self.onconfigure,
        'onfinish': self.onfinish,
        }
    Fysom.__init__(self,
        {'initial': 'activated',
         'events': [
             {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
             {'name': 'configure', 'src': 'configured', 'dst': 'configured'},
             {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
             {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
         ],
         'callbacks':  callbacks_dict
         })
