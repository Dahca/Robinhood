from __future__ import print_function

import json
import urllib

from os.path import isfile

# Resolve compatibility issues between python2 and python3
try:
  from robinhood_trader import RobinhoodTrader
except ImportError:
  from .robinhood_trader import RobinhoodTrader

# A simulated account for use by the Mock class
class Account:

  # Used to calculate the value of an account
  quotes_url = RobinhoodTrader.endpoints["quotes"]

  def __init__(self, file=None):
    self.file = file
    if isfile(str(file)):
      json_data = open(self.file).read()
      json_obj = json.loads(json_data)
      self.fill(json_obj)
    elif file is None:
      self.fill({"cash": float(0), "holdings": {}, "history": {}})
    else:
      raise NameError("No such file: " + file)

  def __del__(self):
    if self.file is not None:
      with open(self.file, "w+") as f:
        json.dump(self.raw(), f, sort_keys=True, indent=4, ensure_ascii=False,
            separators=(",", ": "))

  def fill(self, obj):
    self.cash = float(obj["cash"])
    self.holdings = obj["holdings"]
    self.history = obj["history"]

  def sell(self, tag, amount, price):
    if self.holdings[tag] < amount:
      raise ValueError("Sell amount larger than current holdings")
    self.holdings[tag] -= amount
    self.cash += (float(amount) * float(price))

  def buy(self, tag, amount, price):
    if self.cash < float(amount) * float(price):
      raise ValueError("Buy amount larger than available cash")
    self.holdings[tag] += amount
    self.cash -= (float(amount) * float(price))

  def current_price(tag):
    url = str(quotes_url) + str(tag) + "/"
    # Check for validity of symbol
    try:
      res = json.loads((urllib.urlopen(url)).read());
      if len(res) > 0:
        return res["symbol"];
      else:
        raise NameError("Invalid Symbol: " + tag);
    except ValueError:
      raise NameError("Invalid Symbol: " + tag);

  def market_value(self):
    amount = float(0)
    for tag, num in self.holdings:
      amount += (float(num) * float(current_price(tag)))
    return amount

  def value(self):
    return self.cash + self.market_value()

  def holdings(self):
    return self.holdings

  def num(self, tag):
    return self.holdings[tag]

  def cash(self):
    return self.cash

  def deposit(self, dollars):
    self.cash += float(dollars)

  def withdraw(self, dollars):
    if self.cash < dollars:
      raise ValueError("Trying to withdraw too much money")
    self.cash -= float(dollars)

  def raw(self):
    return {
        "cash": self.cash,
        "holdings": self.holdings,
        "history": self.history
    }


# This class is for simulating trades based on real market data retrieved from
# Robinhood
class MockTrader(RobinhoodTrader):

  ##############################
  # Logging in and initializing
  ##############################

  def __init__(self, account_file=None):
    RobinhoodTrader.__init__(self)
    self.account = Account(account_file)

  ##############################
  # Get data
  ##############################

  def investment_profile(self):
    raise NotImplementedError("No mock method for investment_profile()")
    #self.session.get(self.endpoints['investment_profile'])

  def get_account(self):
    return self.account.raw()

  ##############################
  # Portfolios data
  ##############################

  def portfolios(self):
    # Returns the user's portfolio data.
    mock_portfolio = {
      "equity": self.equity(),
      "market_value": self.market_value()
    }
    return mock_portfolio

  def adjusted_equity_previous_close(self):
    raise NotImplementedError(
        "No mock method for adjusted_equity_previous_close()")
    #return float(self.portfolios()['adjusted_equity_previous_close'])

  def equity(self):
    return self.account.value()

  def equity_previous_close(self):
    raise NotImplementedError("No mock method for equity_previous_close()")
    #return float(self.portfolios()['equity_previous_close'])

  def excess_margin(self):
    raise NotImplementedError("No mock method for excess_margin()")
    #return float(self.portfolios()['excess_margin'])

  def extended_hours_equity(self):
    raise NotImplementedError(
        "No mock method for extended_hours_equity()")
    #return float(self.portfolios()['extended_hours_equity'])

  def extended_hours_market_value(self):
    raise NotImplementedError(
        "No mock method for extended_hours_market_value()")
    #return float(self.portfolios()['extended_hours_market_value'])

  def last_core_equity(self):
    raise NotImplementedError("No mock method for last_core_equity()")
    #return float(self.portfolios()['last_core_equity'])

  def last_core_market_value(self):
    raise NotImplementedError("No mock method for last_core_market_value()")
    #return float(self.portfolios()['last_core_market_value'])

  def market_value(self):
    return self.account.market_value()

  ##############################
  # Positions data
  ##############################

  def positions(self):
    # Returns the user's positions data.
    raise NotImplementedError("No mock method for positions()")
    #return self.session.get(self.endpoints['positions']).json()['results']

  def securities_owned(self):
    # Returns a list of symbols of securities of which there are more
    # than zero shares in user's portfolio.
    securities = []
    for key in self.account.holdings:
      securities += [key]
    return securities

  ##############################
  # Place order
  ##############################

  def place_buy_order(self, tag, quantity, bid_price=None):
    self.account.buy(tag, quantity)

  def place_sell_order(self, tag, quantity, bid_price=None):
    self.account.sell(tag, quantity)

