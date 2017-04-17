# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/


from yapsy.IPlugin import IPlugin
from fysom import Fysom


class KnittingPlugin(IPlugin, Fysom):
  '''A generic plugin implementing a state machine for knitting.

  Subclasses inherit the basic State Machine defined in __init__.
  '''

  def onknit(self, e):
    """Callback when state machine executes knit().

    Starts the knitting process, this is the only function call that can block indefinitely, as it is called from an instance
    of QThread, allowing for processes that require timing and/or blocking behaviour.
    """
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("onknit. It is used for the main 'knitting loop'."))

  def onfinish(self, e):
    """Callback when state machine executes finish().

    When finish() gets called, the plugin is expected to be able to restore it's state back when configure() gets called.
    Finish should trigger a Process Completed notification so the user can operate accordingly.
    """
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("onfinish. It is a callback that is called when knitting is over."))

  def onconfigure(self, e):
    """Callback when state machine executes configure(parent_ui = parent, options={})

    This state gets called to configure the plugin for knitting. It can either
    be called when first configuring the plugin, when an error had happened and
    reset is necessary. The parent ui is expected to hold an object with
    properties.

    Args:
      parent_ui: An object having already been set up by setup_ui.
    """
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("onconfigure. It is used to configure the knitting plugin before starting."))

  def setup_ui(self, parent_ui):
    '''Sets up UI, usually as a child of parent_ui.ui.knitting_options_dock.

    While the whole parent_ui object is available for the plugin to modify, plugins authors are **strongly** encouraged to
    only manipulate the knitting_options_dock, plugins have full access to the parent UI as a way to fully customize the GUI experience.

    Args:
        parent_ui: A PyQt.QMainWindow with the property parent_ui.ui.knitting_options_dock, an instance of QDockWidget to hold the plugin's UI.
    '''
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("setup_ui. It loads the knitting_options_dock panel ui for the plugin."))

  def cleanup_ui(self, ui):
    '''Cleans up and reverts changes to ui done by setup_ui.'''
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("cleanup_ui. It cleans up the knitting_options_dock panel ui for the plugin."))

  def get_configuration_from_ui(self, ui):
    """Loads options dict with a given parent QtGui object. Required for save-load functionality.

    Returns:
      dict: A dict with configuration.
    
    """
    raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format("get_configuration_from_ui. It loads options with a given parent ui object."))

  def __init__(self, callbacks_dict):
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
