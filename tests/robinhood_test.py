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

def test_login_0():
  assert Robinhood().login("foo", "bar", False) is False

def test_endpoints_0():
  assert Robinhood().investment_profile() is not None

def test_quote_data_0():
  assert Robinhood().quote_data("GOOG") is not None

def test_quote_data_1():
  try:
    Robinhood().quote_data("Not a stock")
    assert False
  except NameError as ne:
    assert str(ne) == "Invalid Symbol: Not a stock"
