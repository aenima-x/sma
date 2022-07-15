
class InvalidSymbolError(Exception):
    """Raised when an invalid symbol is required"""

    def __init__(self, symbol):
        self.symbol = symbol
        self.message = f"Invalid symbol {symbol}"
        super().__init__(self.message)


class AlphaVantageApiError(Exception):
    pass
