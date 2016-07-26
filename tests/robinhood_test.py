############################################################
# Tests for the Robinhood class
#
# Note that this will only be able to test methods that do
# not require a user login.
############################################################

from Robinhood.robinhood import Robinhood

##############################
# Test Methods
##############################

def test_init_0():
  Robinhood()

def test_endpoints_0():
  r = Robinhood()
  assert r.quote_data("GOOG") is not None
