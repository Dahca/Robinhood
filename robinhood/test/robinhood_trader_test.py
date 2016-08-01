###############################################################################
# Tests for the Robinhood class
#
# Note that this will only be able to test methods that do not require a user
# login.
###############################################################################

import sys
from nose import with_setup
from nose.tools import *

try:
  from unittest.mock import patch
except ImportError:
  from mock import patch

if sys.version_info[0] < 3:
  input_fn = "__builtin__.raw_input"
else:
  input_fn = "builtins.input"

from .. import Robinhood

##############################
# Utility Methods
##############################


##############################
# Test Methods
##############################

def test_init_0():
  Robinhood()

def test_login_0():
  assert Robinhood().login("foo", "bar", False) is False

@patch(input_fn, lambda _: "not a username")
@patch("getpass.getpass",  lambda: "not a password")
def test_login_1():
  assert Robinhood().login(retry=False) is False

def test_endpoints_0():
  assert Robinhood().investment_profile() is not None

def test_endpoints_1():
  assert Robinhood().instruments("GOOG") is not None

def test_quote_data_0():
  assert Robinhood().quote_data("GOOG") is not None

def test_quote_data_1():
  try:
    Robinhood().quote_data("Not a stock")
    assert False
  except NameError as ne:
    assert str(ne) == "Invalid Symbol: Not a stock"
