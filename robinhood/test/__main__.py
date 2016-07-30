import __init__
import nose
for mod in __init__.__all__:
  nose.runmodule(name=mod)
