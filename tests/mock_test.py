# Tests for the Mock and Account classes
from Robinhood.mock import Mock, Account

def test_account_init_0():
  account = Account()
  assert account.cash == float(0)
