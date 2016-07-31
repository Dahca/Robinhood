# Robinhood

[![Build Status][]][Travis CI] [![Coverage Status][]][Coveralls]

Python Framework to make trades with Robinhood Private API.
See this [blog post][].

## Current Features
- Placing buy orders (`Robinhood.place_buy_order`)
- Placing sell order (`Robinhood.place_sell_order`)
- Quote information (`Robinhood.quote_data`)
- User portfolio data (`Robinhood.portfolios`)
- User positions data (`Robinhood.positions`)
- Supports python2 and python3
- More coming soon

### How To Install Dependencies:
    [sudo -H] pip install [--upgrade] -r requirements.txt

### How to Use (see [example.py][])

    from Robinhood import Robinhood
    my_trader = Robinhood()
    logged_in = my_trader.login(username="USERNAME", password="PASSWORD")
    stock_instrument = my_trader.instruments("GEVO")[0]
    quote_info = my_trader.quote_data("GEVO")
    buy_order = my_trader.place_buy_order(stock_instrument, 1)
    sell_order = my_trader.place_sell_order(stock_instrument, 1)

### Data Returned
- Quote data
  - Ask Price
  - Ask Size
  - Bid Price
  - Bid Size
  - Last trade price
  - Previous close
  - Previous close date
  - Adjusted previous close
  - Trading halted
  - Updated at
- User portfolio data
  - Adjusted equity previous close
  - Equity
  - Equity previous close
  - Excess margin
  - Extended hours equity
  - Extended hours market value
  - Last core equity
  - Last core market value
  - Market value
- User positions data
  - Securities owned

[blog post]: https://medium.com/@rohanpai25/reversing-robinhood-free-accessible-automated-stock-trading-f40fba1e7d8b
[Build Status]: https://travis-ci.org/Dahca/Robinhood.svg?branch=master
[Coverage Status]: https://coveralls.io/repos/github/Dahca/Robinhood/badge.svg?branch=master
[Coveralls]: https://coveralls.io/github/Dahca/Robinhood?branch=master
[example.py]: https://github.com/Jamonek/Robinhood/blob/master/example.py
[Travis CI]: https://travis-ci.org/Dahca/Robinhood
