

class Event(object):
    pass

class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with
    corresponding bars.
    """
    def __init__(self):
        self.type = 'MARKET'

class SignalEvent(Event):
    """
    Handles the event of sending a signal from the strategy
    object. This is received by the portfolio object and acted upon.
    """
    def __init__(self, symbol, signal_type):
        self.type = 'SIGNAL'
        self.symbol = symbol # Crypto symbol, e.g., 'BTCUSDT' 'ETHUSDT'
        self.signal_type = signal_type # 'BUY' or 'SELL' 
        
class OrderEvent(Event):
    """
    Handles the event of sending an order to the execution system.
    The order contains a symbol (e.g., 'BTCUSDT'), a type (market
    or limit), quantity and a direction.
    """
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the values within the OrderEvent.
        """
        print(f"Order: Symbol={self.symbol}, Type={self.order_type}, "
              f"Quantity={self.quantity}, Direction={self.direction}")
        
class FillEvent(Event):
    """
    Encapsulates the notion of a filled order, as returned
    from a brokerage. Stores the quantity of an instrument
    actually filled and at what price. In addition, stores
    the commission of the trade from the brokerage.
    """
    def __init__(self, timeindex, symbol, exchange,
                 quantity, direction, fill_cost, commission=None):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculate commission
        if commission is None:
            self.commission = self.calculate_commission()
        else:
            self.commission = commission
    def calculate_commission(self):
        """
        Calculates the fees of the trade based on the Binance fee structure.
        For simplicity, we will assume a flat fee of 0.1% per trade.
        """
        commission_rate = 0.001  # 0.1%
        return abs(self.fill_cost * commission_rate)