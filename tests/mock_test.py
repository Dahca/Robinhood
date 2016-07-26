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

def assert_account_empty(account, filename=None):
  assert isinstance(account, Account)
  assert account.cash == float(0)
  assert account.holdings == {}
  assert account.history == {}
  assert account.file == filename

##############################
# Test Methods
##############################

def test_account_init_0():
  assert_account_empty(Account())

def test_account_init_1():
  filename = get_res_name("res/empty.json")
  account = Account(filename)
  assert_account_empty(account, filename)

def test_mock_init_0():
  assert_account_empty(Mock().account)

def test_mock_init_1():
  filename = get_res_name("res/empty.json")
  mock = Mock(filename)
  assert_account_empty(mock.account, filename)
