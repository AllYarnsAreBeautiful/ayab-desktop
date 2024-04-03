from . import engine
from . import lowercase_e_rc, lowercase_e_reversed_rc

# This adds the engine to the upper namespace of the module.
Engine = engine.Engine

# We also add the resources for proper loading.
lowercase_e_rc = lowercase_e_rc
lowercase_e_reversed_rc = lowercase_e_reversed_rc
