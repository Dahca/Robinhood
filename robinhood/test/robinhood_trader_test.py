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

def test_investment_profile_0():
  assert Robinhood().investment_profile() is not None

def test_instruments_0():
  assert Robinhood().instruments("GOOG") is not None

@patch(input_fn, lambda _: "GOOG")
def test_investment_profile_1():
  assert Robinhood().instruments() is not None

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

def test_get_quote_0():
  assert Robinhood().get_quote("GOOG") is not None

def test_print_quote_0():
  Robinhood().print_quote("GOOG")

def test_print_quotes_0():
  Robinhood().print_quotes(["GOOG", "F"])

def test_ask_price_0():
  assert Robinhood().ask_price("GOOG") is not None

def test_ask_size_0():
  assert Robinhood().ask_size("GOOG") is not None

def test_bid_price_0():
  assert Robinhood().bid_price("GOOG") is not None

def test_bid_size_0():
  assert Robinhood().bid_size("GOOG") is not None

def test_last_trade_price_0():
  assert Robinhood().last_trade_price("GOOG") is not None

def test_previous_close_0():
  assert Robinhood().previous_close("GOOG") is not None

def test_previous_close_date_0():
  assert Robinhood().previous_close_date("GOOG") is not None

def test_adjusted_previous_close_0():
  assert Robinhood().adjusted_previous_close("GOOG") is not None

def test_symbol_0():
  assert Robinhood().symbol("GOOG") == "GOOG"

def test_last_updated_at_0():
  assert Robinhood().last_updated_at("GOOG") is not None

# Things we can't really test well without an actual account to log into

@raises(KeyError)
def test_get_account_0():
  Robinhood().get_account()

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

@raises(KeyError)
def test_securities_owned_0():
  Robinhood().securities_owned()

@raises(KeyError)
def test_market_value_0():
  Robinhood().market_value()

@raises(KeyError)
def test_adjusted_equity_previous_close_0():
  Robinhood().adjusted_equity_previous_close()

@raises(KeyError)
def test_equity_0():
  Robinhood().equity()

@raises(KeyError)
def test_equity_previous_close_0():
  Robinhood().equity_previous_close()

@raises(KeyError)
def test_excess_margin_0():
  Robinhood().excess_margin()

@raises(KeyError)
def test_extended_hours_equity_0():
  Robinhood().extended_hours_equity()

@raises(KeyError)
def test_extended_hours_market_value_0():
  Robinhood().extended_hours_market_value()

@raises(KeyError)
def test_last_core_equity_0():
  Robinhood().last_core_equity()

@raises(KeyError)
def test_last_core_market_value_0():
  Robinhood().last_core_market_value()

