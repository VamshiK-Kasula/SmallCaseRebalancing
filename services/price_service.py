"""
Price service for fetching stock prices using yfinance.
"""
import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List
import logging
import numpy as np

logger = logging.getLogger(__name__)


class PriceService:
    """Service for fetching and managing stock prices."""
    
    def get_stock_price(self, ticker: str) -> Optional[float]:
        """
        Fetch current stock price for a given ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'TCS.NS')
            
        Returns:
            Current stock price or None if failed to fetch
        """

        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")
            
            if not history.empty:
                price = history["Close"].iloc[-1]
                return round(price, 2)
            else:
                logger.warning(f"No price data found for ticker: {ticker}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching price for {ticker}: {e}")
            return None
    
    def get_portfolio_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        Update prices for all tickers in a portfolio DataFrame.
        
        Args:
            df: DataFrame with 'Ticker' column and optionally 'Current Price (per share)'
            
        Returns:
            Updated DataFrame with current prices
        """

        prices = {}

        # Fetch live prices for all tickers
        for ticker in tickers:
            new_price = self.get_stock_price(ticker)
            if new_price is not None:
                prices[ticker] = new_price
                logger.info(f"Updated price for {ticker}: {new_price}")
            else:
                logger.warning(f"Could not fetch price for {ticker}, keeping existing value")
        
        return prices
