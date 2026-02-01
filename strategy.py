from event import Event, SignalEvent
from datetime import datetime
import numpy as np
import pandas as pd
import queue  

from abc import ABC, ABCMeta, abstractmethod

from event import SignalEvent

class Strategy(ABC):
    """
    Strategy is an abstract base class providing an interface for
    all subsequent (inherited) trading strategy handling objects.
    The goal of a Strategy object is to generate SignalEvents
    based on market data.
    """


    @abstractmethod
    def calculate_signals(self, event):
        """
        Provides the mechanism to calculate signals.
        Must be overridden by all Strategy subclasses.

        Parameters:
        event - A MarketEvent object.
        """
        raise NotImplementedError("Should implement calculate_signals()")
class BuyAndHoldStrategy(Strategy):
    """
    This is an extremely simple strategy that goes LONG all of the 
    symbols as soon as a bar is received. It will never exit a position.

    It is primarily used as a testing mechanism for the Strategy class
    as well as a benchmark upon which to compare other strategies.
    """
    def __init__(self, bars, events):
        """
        Initialises the BuyAndHoldStrategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        #Once buy & hold is given, these are set to true
        self.bought = self.calculate_initial_bought()

    def calculate_initial_bought(self):
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to False.
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] = False
        return bought
    
    def calculate_signals(self, event):
        """
        For "BUY AND HOLD" strategy, we generate a single signal per symbol
        and then no additional signals. This means we are 
        constantly long the market from date of strategy
        initialisation.
        
        Parameters:
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            for s in self.symbol_list:
               bars = self.bars.get_latest_bars(s, N=1)
               if bars is not None and bars != []:
                   if self.bought[s] == False:
                       signal = SignalEvent(bars[0][0],bars[0][1], 'LONG')
                       self.events.put(signal)
                       self.bought[s] = True