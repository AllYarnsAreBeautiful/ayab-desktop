from fysom import Fysom

## Plugins should be class based but expose the fysom object events as a public inteface.


def onconfigure(e):
    '''Sets configuration for knitting session.'''
    assert e.options
    pass


def onknit(e):
    '''Handles transition to knitting stage. Sets up callbacks for control.'''
    pass


def onknitting(e):
    """Handles the automated knitting process."""
    ## For AYAB, add here the knittting loop currently inside ayab_control.knitImage
    pass


def onfinish(e):
    #TODO: do cleanup.
    pass

fsm = Fysom(
    {'initial': 'activated',
     'events': [
         {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
         {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
         {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
     ],
     'callbacks': {
         'onknit': onknit,
         'onknitting': onknitting,
         'onconfigure': onconfigure,
         'onfinish': onfinish
     }})

fsm.configure(image=None, options={})
fsm.knit()
fsm.finish()
