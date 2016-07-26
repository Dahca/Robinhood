from __future__ import print_function

import getpass
import json
import requests
import urllib
import sys

try:
  from urllib import urlopen
except ImportError:
  from urllib.request import urlopen

class Robinhood:

  endpoints = {
      "login": "https://api.robinhood.com/api-token-auth/",
      "investment_profile":
          "https://api.robinhood.com/user/investment_profile/",
      "accounts": "https://api.robinhood.com/accounts/",
      "ach_iav_auth": "https://api.robinhood.com/ach/iav/auth/",
      "ach_relationships": "https://api.robinhood.com/ach/relationships/",
      "ach_transfers": "https://api.robinhood.com/ach/transfers/",
      "applications": "https://api.robinhood.com/applications/",
      "dividends": "https://api.robinhood.com/dividends/",
      "edocuments": "https://api.robinhood.com/documents/",
      "instruments": "https://api.robinhood.com/instruments/",
      "margin_upgrades": "https://api.robinhood.com/margin/upgrades/",
      "markets": "https://api.robinhood.com/markets/",
      "notifications": "https://api.robinhood.com/notifications/",
      "orders": "https://api.robinhood.com/orders/",
      "password_reset": "https://api.robinhood.com/password_reset/request/",
      "portfolios": "https://api.robinhood.com/portfolios/",
      "positions": "https://api.robinhood.com/positions/",
      "quotes": "https://api.robinhood.com/quotes/",
      "document_requests":
          "https://api.robinhood.com/upload/document_requests/",
      "user": "https://api.robinhood.com/user/",
      "watchlists": "https://api.robinhood.com/watchlists/"
  }
  headers = {
      "Accept": "*/*",
      "Accept-Encoding": "gzip, deflate",
      "Accept-Language":
          "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      "X-Robinhood-API-Version": "1.0.0",
      "Connection": "keep-alive",
      "User-Agent": "Robinhood/823 (iPhone iOS 9.3.3 Scale/2.00)"
  }
  session = None
  username = None
  password = None
  headers = None
  auth_token = None

  ##############################
  # Logging in and initializing
  ##############################

  def __init__(self):
    self.session = requests.session()
    if sys.version_info[0] < 3:
      self.session.proxies = urllib.getproxies()
    else:
      self.session.proxies = urllib.request.getproxies()
    self.session.headers = self.headers

  def login(self, username=None, password=None, retry=True):
    if username is None:
      username = raw_input("Username: ")
    if password is None:
      password = getpass.getpass()
    self.username = username
    self.password = password
    data = "password=%s&username=%s" % (self.password, self.username)
    res = self.session.post(self.endpoints["login"], data=data).json()
    try:
      self.auth_token = res["token"]
    except KeyError:
      if retry:
        print("Incorrect login, please try again\nReason: ", end="")
        try:
          print(res["detail"])
        except:
          pass
        return self.login()
      return False
    self.headers["Authorization"] = "Token " + self.auth_token
    return True

  ##############################
  # Get data
  ##############################

  def investment_profile(self):
    return self.session.get(self.endpoints["investment_profile"]).json()

  def instruments(self, stock=None):
    # Prompt for stock if not entered
    if stock is None:
      stock = raw_input("Symbol: ")
    params = {"query": stock.upper()}
    res = self.session.get(self.endpoints["instruments"], params=params).json()
    return res["results"]

  def quote_data(self, stock=None):
    try:
      from urllib.error import HTTPError
    except ImportError:
      from urllib2 import HTTPError
    # Prompt for stock if not entered
    if stock is None:
      stock = raw_input("Symbol: ")
    url = str(self.endpoints["quotes"]) + str(stock) + "/"
    # Check for validity of symbol
    try:
      res = json.loads(urlopen(url).read().decode("utf-8"))
      if len(res) > 0:
        return res
      raise NameError("Invalid Symbol: " + stock)
    except ValueError:
      raise NameError("Invalid Symbol: " + stock)
    except HTTPError as err:
      if err.code != 400:
        raise
      raise NameError("Invalid Symbol: " + stock)

  def get_quote(self, stock=None):
    return self.quote_data(stock)["symbol"]

  def print_quote(self, stock=None):
    print(self.quote_data(stock)["symbol"] + ": $" + data["last_trade_price"])

  def print_quotes(self, stocks):
    for stock in stocks:
      self.print_quote(stock)

  def ask_price(self, stock=None):
    return self.quote_data(stock)["ask_price"]

  def ask_size(self, stock=None):
    return self.quote_data(stock)["ask_size"]

  def bid_price(self, stock=None):
    return self.quote_data(stock)["bid_price"]

  def bid_size(self, stock=None):
    return self.quote_data(stock)["bid_size"]

  def last_trade_price(self, stock=None):
    return self.quote_data(stock)["last_trade_price"]

  def previous_close(self, stock=None):
    return self.quote_data(stock)["previous_close"]

  def previous_close_date(self, stock=None):
    return self.quote_data(stock)["previous_close_date"]

  def adjusted_previous_close(self, stock=None):
    return self.quote_data(stock)["adjusted_previous_close"]

  def symbol(self, stock=None):
    return self.quote_data(stock)["symbol"]

  def last_updated_at(self, stock=None):
    return self.quote_data(stock)["updated_at"]

  def get_account(self):
    return self.session.get(self.endpoints["accounts"]).json()["results"][0]

  ##############################
  # Portfolios data
  ##############################

  # Returns the user's portfolio data.
  def portfolios(self):
    return self.session.get(self.endpoints["portfolios"]).json()["results"][0]

  def adjusted_equity_previous_close(self):
    return float(self.portfolios()["adjusted_equity_previous_close"])

  def equity(self):
    return float(self.portfolios()["equity"])

  def equity_previous_close(self):
    return float(self.portfolios()["equity_previous_close"])

  def excess_margin(self):
    return float(self.portfolios()["excess_margin"])

  def extended_hours_equity(self):
    return float(self.portfolios()["extended_hours_equity"])

  def extended_hours_market_value(self):
    return float(self.portfolios()["extended_hours_market_value"])

  def last_core_equity(self):
    return float(self.portfolios()["last_core_equity"])

  def last_core_market_value(self):
    return float(self.portfolios()["last_core_market_value"])

  def market_value(self):
    return float(self.portfolios()["market_value"])

  ##############################
  # Positions data
  ##############################

  # Returns the user's positions data.
  def positions(self):
    return self.session.get(self.endpoints["positions"]).json()["results"]

  # Returns a list of symbols of securities of which there are more
  # than zero shares in user's portfolio.
  def securities_owned(self):
    positions = self.positions()
    securities = []
    for position in positions:
      quantity = float(position["quantity"])
      if quantity > 0:
        res = self.session.get(position["instrument"])
        securities.append(res.json()["symbol"])
    return securities

  ##############################
  # Place order
  ##############################

  def place_order(self, instrument, quantity=1, bid_price=None,
                  transaction=None):
    if bid_price is None:
      bid_price = self.quote_data(instrument["symbol"])["bid_price"]
    data = ("account=%s&instrument=%s&price=%f&quantity=%d&side=%s&"
        "symbol=%s&time_in_force=gfd&trigger=immediate&type=market") % (
        self.get_account()["url"],
        urllib.unquote(instrument["url"]),
        float(bid_price),
        quantity,
        transaction,
        instrument["symbol"]
    )
    res = self.session.post(self.endpoints["orders"], data=data)
    return res

  def place_buy_order(self, instrument, quantity, bid_price=None):
    return self.place_order(instrument, quantity, bid_price, "buy")

  def place_sell_order(self, instrument, quantity, bid_price=None):
    return self.place_order(instrument, quantity, bid_price, "sell")
