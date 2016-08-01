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
  from urllib2 import HTTPError
  input_fn = "__builtin__.raw_input"
else:
  from urllib.error import HTTPError
  input_fn = "builtins.input"

from .. import Robinhood

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

@raises(NameError)
def test_quote_data_1():
  Robinhood().quote_data("Not a stock")

@patch(input_fn, lambda _: "GOOG")
def test_quote_data_2():
  assert Robinhood().quote_data() is not None

@raises(NameError)
@patch(input_fn, lambda _: "Not a stock")
def test_quote_data_3():
  Robinhood().quote_data()

@raises(KeyError)
def test_place_order_0():
  Robinhood().place_order(instrument=Robinhood().instruments("GOOG"),
                          bid_price=0.0, transaction="not a transaction")

@raises(KeyError)
def test_place_buy_order_0():
  Robinhood().place_buy_order(Robinhood().instruments("GOOG"), 1, 1)

@raises(KeyError)
def test_place_sell_order_0():
  Robinhood().place_sell_order(Robinhood().instruments("GOOG"), 1, 1)

