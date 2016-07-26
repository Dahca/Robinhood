############################################################
# Tests for the Mock and Account classes
############################################################

from Robinhood.mock import Mock, Account

##############################
# Utility Methods
##############################

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

def test_account_setup_0():
  account = Account()
  account.deposit(100)
  assert_account_equals(account, cash=float(100))
  account.withdraw(50)
  assert_account_equals(account, cash=float(50))

def test_mock_init_0():
  assert_account_empty(Mock().account)

def test_mock_init_1():
  filename = get_res_name("res/empty.json")
  mock = Mock(filename)
  assert_account_empty(mock.account, filename)

def test_mock_init_2():
  assert Mock().portfolios() == { "equity": 0.0, "market_value": 0.0 }

def test_mock_init_3():
  filename = get_res_name("res/init_test.json")
  mock = Mock(filename)
  assert mock.securities_owned() == ["GOOG"]

