import getpass
import json
import requests
import urllib

from os.path import isfile

from Robinhood import Robinhood

# A simulated account for use by the Mock class
class Account:

  # Used to calculate the value of an account
  quotes_url = Robinhood.endpoints["quotes"]

  def __init__(self, file=None):
    if file is not None and not isfile(file):
      self.file = file
      self.fill({"cash": float(0), "holdings": {}, "history": {}})
    elif file is None:
      self.file = None
      self.fill({"cash": float(0), "holdings": {}, "history": {}})
    else:
      self.file = file
      json_data = open(self.file).read()
      json_obj = json.loads(json_data)
      self.fill(json_obj)

  def __del__(self):
    if self.file is not None:
      with open(self.file, "w+") as f:
        json.dump(self.raw(), f, sort_keys=True, indent=4, ensure_ascii=False)

  def fill(self, obj):
    self.cash = obj["cash"]
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
    except (ValueError):
      raise NameError("Invalid Symbol: " + tag);

  def value(self):
    amount = self.cash
    for tag, amount in self.holdings:
      amount += (float(amount) * float(current_price(tag)))
    return amount

  def holdings(self):
    return self.holdings

  def num(self, tag):
    return self.holdings[tag]

  def cash(self):
    return self.cash

  def deposit(self, dollars):
    self.cash += float(dollars)

  def raw(self):
    return {"cash": self.cash,
        "holdings": self.holdings,
        "history": self.history}


# This class is for simulating trades based on real market data retrieved from
# Robinhood
class Mock(Robinhood):

  ##############################
  # Logging in and initializing
  ##############################

  def __init__(self, account_file=None):
    Robinhood.__init__(self)
    self.account = Account(account_file)

  ##############################
  # Get data
  ##############################

  def investment_profile(self):
    self.session.get(self.endpoints['investment_profile'])

  def instruments(self, stock=None):
    res = self.session.get(self.endpoints['instruments'],
                           params={'query' : stock.upper()}).json()
    return res['results']

  def get_account(self):
    return self.session.get(self.endpoints['accounts']).json()['results'][0]

  ##############################
  # Portfolios data
  ##############################

  def portfolios(self):
    # Returns the user's portfolio data.
    return self.session.get(self.endpoints['portfolios']).json()['results'][0]

  def adjusted_equity_previous_close(self):
    return float(self.portfolios()['adjusted_equity_previous_close'])

  def equity(self):
    return float(self.portfolios()['equity'])

  def equity_previous_close(self):
    return float(self.portfolios()['equity_previous_close'])

  def excess_margin(self):
    return float(self.portfolios()['excess_margin'])

  def extended_hours_equity(self):
    return float(self.portfolios()['extended_hours_equity'])

  def extended_hours_market_value(self):
    return float(self.portfolios()['extended_hours_market_value'])

  def last_core_equity(self):
    return float(self.portfolios()['last_core_equity'])

  def last_core_market_value(self):
    return float(self.portfolios()['last_core_market_value'])

  def market_value(self):
    return float(self.portfolios()['market_value'])

  ##############################
  # Positions data
  ##############################

  def positions(self):
    # Returns the user's positions data.
    return self.session.get(self.endpoints['positions']).json()['results']

  def securities_owned(self):
    # Returns a list of symbols of securities of which there are more
    # than zero shares in user's portfolio.
    securities = []
    for key, val in self.account.holdings():
      securities += [key]
    return securities

  ##############################
  # Place order
  ##############################

  place_order = None

  def place_buy_order(self, tag, quantity, bid_price=None):
    self.account.buy(tag, quantity)

  def place_sell_order(self, tag, quantity, bid_price=None):
    self.account.sell(tag, quantity)
