from decimal import Decimal
from django.test import SimpleTestCase
from django.conf import settings
from api.stocks import StocksClient
from api.exceptions import AlphaVantageApiError, InvalidSymbolError


class TestStocks(SimpleTestCase):

    # def test_alpha_vantage_invalid_api_key(self):
    #     api_key = "invalid"
    #     stocks_client = StocksClient(api_key)
    #     with self.assertRaises(AlphaVantageApiError):
    #         stocks_client.get_stocks_price("AAPL")

    def test_alpha_vantage_invalid_symbol(self):
        stocks_client = StocksClient(settings.ALPHA_VANTAGE_API_KEY)
        with self.assertRaises(InvalidSymbolError):
            stocks_client.get_stocks_price("APL")

    def test_calculate_stocks_price(self):
        mocked_symbol = "AAPL"
        mocked_data = {
            "2022-07-12": {
                "1. open": "140.8400",
                "2. high": "141.5500",
                "3. low": "138.5650",
                "4. close": "139.1800",
                "5. volume": "3235571"
            },
            "2022-07-11": {
                "1. open": "140.6200",
                "2. high": "141.8700",
                "3. low": "140.1300",
                "4. close": "141.0000",
                "5. volume": "3912773"
            },
            "2022-07-08": {
                "1. open": "140.7600",
                "2. high": "141.3203",
                "3. low": "139.8200",
                "4. close": "140.4700",
                "5. volume": "2820928"
            },
            "2022-07-07": {
                "1. open": "138.9100",
                "2. high": "141.3250",
                "3. low": "138.8300",
                "4. close": "140.8300",
                "5. volume": "3897077"
            }
        }
        stocks_client = StocksClient(settings.ALPHA_VANTAGE_API_KEY)
        stock_price = stocks_client.calculate_stocks_price(mocked_symbol, mocked_data)
        assert stock_price.symbol == mocked_symbol
        assert stock_price.open == Decimal(mocked_data["2022-07-12"]["1. open"])
        assert stock_price.higher == Decimal(mocked_data["2022-07-12"]["2. high"])
        assert stock_price.lower == Decimal(mocked_data["2022-07-12"]["3. low"])
        assert stock_price.close_variation == abs(Decimal(mocked_data["2022-07-12"]["4. close"]) -
                                                  Decimal(mocked_data["2022-07-11"]["4. close"]))
