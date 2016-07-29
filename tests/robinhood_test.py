############################################################
# Tests for the Robinhood class
#
# Note that this will only be able to test methods that do
# not require a user login.
############################################################

<<<<<<< Updated upstream
import Robinhood
from Robinhood.robinhood import Robinhood
=======
from Robinhood.robinhood import RobinhoodTrader
>>>>>>> Stashed changes

##############################
# Test Methods
##############################

def test_init_0():
  RobinhoodTrader()

def test_login_0():
  assert RobinhoodTrader().login("foo", "bar", False) is False

def test_endpoints_0():
  assert RobinhoodTrader().investment_profile() is not None

def test_endpoints_1():
  assert RobinhoodTrader().instruments("GOOG") is not None

def test_quote_data_0():
  assert RobinhoodTrader().quote_data("GOOG") is not None

def test_quote_data_1():
  try:
    RobinhoodTrader().quote_data("Not a stock")
    assert False
  except NameError as ne:
    assert str(ne) == "Invalid Symbol: Not a stock"
