###############################################################################
# Tests for the Mock and Account classes
###############################################################################

from nose.tools import *

from .. import MockTrader, Account

##############################
# Utility Methods
##############################

dne = "this_file_does_not_exist.jpeg"

def dne_setup():
  from os.path import isfile
  from os import remove
  if isfile(dne):
    remove(dne)

def dne_teardown():
  from os.path import isfile
  assert not isfile(dne)

def get_res_name(name):
  from os.path import dirname, abspath, join, isfile
  res_path = join(dirname(abspath(__file__)), name)
  if isfile(res_path):
    return res_path
  raise NameError("No such resource: " + name)

def assert_account_equals(account, cash=float(0), history={}, holdings={},
                          filename=None):
  assert isinstance(account, Account)
  assert abs(account.cash - cash) <= 0.001
  assert account.holdings == holdings
  assert account.history == history
  assert account.file == filename

def assert_account_empty(account, filename=None):
  assert_account_equals(account, filename=filename)

##############################
# Test Methods
##############################

def test_account_init_0():
  assert_account_empty(Account())

def test_account_init_1():
  filename = get_res_name("res/empty.json")
  account = Account(filename)
  assert_account_empty(account, filename)

def test_account_init_2():
  filename = get_res_name("res/init_test.json")
  account = Account(filename)
  assert_account_equals(account, 3.7, {"foo": "bar"}, {"GOOG": 3}, filename)
  
@raises(NameError)
@with_setup(dne_setup, dne_teardown)
def test_account_init_3():
  Account(file=dne)

def test_account_setup_0():
  account = Account()
  account.deposit(100)
  assert_account_equals(account, cash=float(100))
  account.withdraw(50)
  assert_account_equals(account, cash=float(50))

def test_mock_init_0():
  assert_account_empty(MockTrader().account)

def test_mock_init_1():
  filename = get_res_name("res/empty.json")
  mock = MockTrader(filename)
  assert_account_empty(mock.account, filename)

def test_mock_init_2():
  assert MockTrader().portfolios() == { "equity": 0.0, "market_value": 0.0 }

def test_mock_init_3():
  filename = get_res_name("res/init_test.json")
  mock = MockTrader(filename)
  assert mock.securities_owned() == ["GOOG"]

def test_mock_portfolios_0():
  assert MockTrader().portfolios() == {"equity": float(0), 
                                       "market_value": float(0)}

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

