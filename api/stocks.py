import logging
import requests
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .exceptions import InvalidSymbolError, AlphaVantageApiError

logger = logging.getLogger(__name__)

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_DATE_FORMAT = "%Y-%m-%d"


@dataclass(frozen=True)
class StockPrice:

    symbol: str
    open: str
    lower: str
    higher: str
    close_variation: str

    def get_data(self):
        return {
            "symbol": self.symbol,
            "open": self.open,
            "lower": self.lower,
            "higher": self.higher,
            "close_variation": self.close_variation,
        }


class StocksClient:
    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def calculate_stocks_price(symbol: str, stocks_data: dict):
        sorted_data = sorted(stocks_data.items(),
                             key=lambda item: datetime.strptime(item[0], ALPHA_VANTAGE_DATE_FORMAT), reverse=True)
        last_value = sorted_data[0][1]
        previous_value = sorted_data[1][1]
        open_price = Decimal(last_value['1. open'])
        lower_price = Decimal(last_value['3. low'])
        higher_price = Decimal(last_value['2. high'])
        close_price = Decimal(last_value['4. close'])
        previous_close_price = Decimal(previous_value['4. close'])
        variation = abs(close_price - previous_close_price)
        logger.info(f"Symbol: {symbol} - Data: Open {open_price}/Lower {lower_price}/Higher {higher_price}"
                    f"/Close {close_price}/Previous close {previous_close_price}/Close variation {variation}")
        return StockPrice(
            symbol=symbol,
            open=open_price,
            lower=lower_price,
            higher=higher_price,
            close_variation=variation,
        )

    def get_stocks_price(self, symbol):
        logger.info("Get stock prices for symbol: %s", symbol)
        response = requests.get(ALPHA_VANTAGE_URL, params={'function': 'TIME_SERIES_DAILY', 'symbol': symbol,
                                                           'apikey': self.api_key})
        if response.status_code == 200:
            stocks_json = response.json()
            if 'Error Message' in stocks_json:
                logger.error("Invalid symbol required: %s", symbol)
                raise InvalidSymbolError(symbol)
            else:
                logger.info("Alpha Vantage api response OK")
                stock_price = self.calculate_stocks_price(symbol, stocks_json['Time Series (Daily)'])
                return stock_price

        else:
            logger.error("Invalid Alpha Vantage response: %s", response.status_code)
            raise AlphaVantageApiError

