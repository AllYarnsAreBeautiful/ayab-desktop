from yapsy.IPlugin import IPlugin
from fysom import Fysom


class KnittingPlugin(IPlugin, Fysom):
  '''A generic plugin implementing a state machine for knitting.'''

  def onknit(self, e):
    """Callback when state machine executes knit()"""
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("onknit. It is used for the main 'knitting loop'."))

  def onfinish(self, e):
    """Callback when state machine executes finish()"""
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("onfinish. It is a callback that is called when knitting is over."))

  def onconfigure(self, e):
    """Callback when state machine executes configure(parent_ui = parent, options={})

    This state gets called to configure the plugin for knitting. It can either
    be called when first configuring the plugin, when an error had happened and
    reset is necessary. The parent ui is expected to hold an object with
    properties.

    Args:
      parent_ui: An object holding the parent_ui.pil_image property.

    Returns:
      dict: A dict with configuration.

    """
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("onconfigure. It is used to configure the knitting plugin before starting."))

  def setup_ui(self, ui):
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("setup_ui. It loads the knitting_options_dock panel ui for the plugin."))

  def cleanup_ui(self, ui):
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("cleanup_ui. It cleans up the knitting_options_dock panel ui for the plugin."))

  def get_configuration_from_ui(self, ui):
    """Loads options dict with a given parent QtGui object."""
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("get_configuration_from_ui. It loads options with a given parent ui object."))

  def __init__(self, callbacks_dict):
    """
    Args:
        _fsm: The internal finite state machine.
    """
    self.__NOT_IMPLEMENTED_ERROR = "Classes that inherit from KnittingPlugin should implment {0}"

    callbacks_dict = {
        'onknit': self.onknit,
        #'onknitting': self.onknitting,
        'onconfigure': self.onconfigure,
        'onfinish': self.onfinish,
        }
    Fysom.__init__(self,
        {'initial': 'activated',
         'events': [
             ## TODO: add more states for handling error management.
             {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
             {'name': 'configure', 'src': 'configured', 'dst': 'configured'},
             {'name': 'configure', 'src': 'finished', 'dst': 'configured'},
             {'name': 'configure', 'src': 'error', 'dst': 'configured'},
             {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
             {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
             {'name': 'fail', 'src': 'knittng', 'dst': 'error'}
         ],
         'callbacks':  callbacks_dict
         })
