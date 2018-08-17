###############################################################################
# Tests for the Mock and Account classes
###############################################################################

import json, os
from os.path import isfile

from nose import with_setup
from nose.tools import *

from .. import MockTrader, Account

##############################
# Utility Methods
##############################

# Setup and teardown methods for file operations

dne_file = "this_file_does_not_exist.jpeg"

def dne_file_setup():
  if isfile(dne_file):
    os.remove(dne_file)

def dne_file_teardown():
  assert not isfile(dne_file)

empty_file = "empty.json"

def empty_file_setup():
  if isfile(empty_file):
    os.remove(empty_file)
  empty_json = {"cash": 0.0, "holdings": {}, "history": {}}
  with open(empty_file, "w+") as f:
    json.dump(empty_json, f)

def empty_file_teardown():
  assert isfile(empty_file)
  os.remove(empty_file)

example_file = "example.json"

def example_file_setup():
  if isfile(example_file):
    os.remove(example_file)
  example_json = {
      "cash": 6006.13, 
      "holdings": {
          "GOOG": 42
      }, 
      "history": {
          "history": "not_implemented"
      }
  }
  with open(example_file, "w+") as f:
    json.dump(example_json, f)

def example_file_teardown():
  assert isfile(example_file)
  os.remove(example_file)

def assert_account_equals(account, cash=float(0), history={}, holdings={}):
  assert isinstance(account, Account)
  assert abs(account.cash - cash) <= 0.001
  assert account.holdings == holdings
  assert account.history == history

def assert_account_empty(account):
  assert_account_equals(account)

##############################
# Test Methods
##############################

def test_account_init_0():
  assert_account_empty(Account())

@with_setup(empty_file_setup, empty_file_teardown)
def test_account_init_1():
  account = Account(empty_file)
  assert_account_empty(account)

@with_setup(example_file_setup, example_file_teardown)
def test_account_init_2():
  account = Account(example_file)
  assert_account_equals(account, 6006.13,
      {"history": "not_implemented"}, {"GOOG": 42})
  
@raises(NameError)
@with_setup(dne_file_setup, dne_file_teardown)
def test_account_init_3():
  Account(file=dne)

def test_account_setup_0():
  account = Account()
  account.deposit(100)
  assert_account_equals(account, cash=float(100))
  account.withdraw(50)
  assert_account_equals(account, cash=float(50))

@with_setup(example_file_setup, example_file_teardown)
def test_account_setup_1():
  account = Account(example_file)
  assert account.num("GOOG") == 42
  assert account.num("Not a stock") == 0
  assert account.current_holdings() == { "GOOG": 42 }

@raises(KeyError)
def test_account_sell_0():
  Account().sell("GOOG", 1, 100)

@with_setup(example_file_setup, example_file_teardown)
def test_account_sell_1():
  account = Account(example_file)
  account.sell("GOOG", 42, 10)
  assert abs(account.available_cash() - 6426.13) < 0.001

@raises(ValueError)
@with_setup(example_file_setup, example_file_teardown)
def test_account_sell_2():
  account = Account(example_file)
  account.sell("GOOG", 10000, 0.1)

@raises(ValueError)
def test_account_buy_0():
  Account().buy("GOOG", 1, 1)

def test_account_buy_1():
  account = Account()
  account.cash = 1000.0
  account.buy("GOOG", 1, 42.0)
  assert abs(account.available_cash() - 958.0) < 0.001

def test_account_current_price_0():
  assert Account().current_price("GOOG") is not None

@raises(NameError)
def test_account_current_price_1():
  Account().current_price("Not a real stock")

def test_account_market_value_0():
  assert Account().market_value() == 0

@with_setup(example_file_setup, example_file_teardown)
def test_account_market_value_1():
  account = Account(example_file)
  assert account.market_value() >= 0.42

# MockTrader tests

def test_mock_init_0():
  assert_account_empty(MockTrader().account)

@with_setup(empty_file_setup, empty_file_teardown)
def test_mock_init_1():
  mock = MockTrader(empty_file)
  assert_account_empty(mock.account)

@with_setup(example_file_setup, example_file_teardown)
def test_mock_securities_owned_0():
  mock = MockTrader(example_file)
  assert mock.securities_owned() == ["GOOG"]

def test_mock_portfolios_0():
  assert MockTrader().portfolios() == { "equity": 0.0, "market_value": 0.0 }

# When/if these get implemented, these tests remind the feature writer to come
# back over here and write some tests!

@raises(NotImplementedError)
def test_investment_profile_0():
  MockTrader().investment_profile()

@raises(NotImplementedError)
def test_equity_previous_close_0():
  MockTrader().equity_previous_close()

@raises(NotImplementedError)
def test_excess_margin_0():
  MockTrader().excess_margin()

@raises(NotImplementedError)
def test_extended_hours_equity_0():
  MockTrader().extended_hours_equity()

@raises(NotImplementedError)
def test_extended_hours_market_value_0():
  MockTrader().extended_hours_market_value()

@raises(NotImplementedError)
def test_last_core_equity_0():
  MockTrader().last_core_equity()

@raises(NotImplementedError)
def test_last_core_market_value_0():
  MockTrader().last_core_market_value()
 
@raises(NotImplementedError)
def test_positions_0():
  MockTrader().positions()

