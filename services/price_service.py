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
    
    def __init__(self):
        self._price_cache: Dict[str, float] = {}
    
    def get_stock_price(self, ticker: str) -> Optional[float]:
        """
        Fetch current stock price for a given ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'TCS.NS')
            
        Returns:
            Current stock price or None if failed to fetch
        """
        # Check cache first
        if ticker in self._price_cache:
            return self._price_cache[ticker]
        
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")
            
            if not history.empty:
                price = history["Close"].iloc[-1]
                self._price_cache[ticker] = round(price, 2)
                return self._price_cache[ticker]
            else:
                logger.warning(f"No price data found for ticker: {ticker}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching price for {ticker}: {e}")
            return None
    
    def update_portfolio_prices(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Update prices for all tickers in a portfolio DataFrame.
        
        Args:
            df: DataFrame with 'Ticker' column and optionally 'Current Price (per share)'
            
        Returns:
            Updated DataFrame with current prices
        """
        df_copy = df.copy()
        
        # Ensure the "Current Price (per share)" column exists
        if "Current Price (per share)" not in df_copy.columns:
            df_copy["Current Price (per share)"] = np.nan
        
        # Calculate current prices from existing data if available
        if "Current Value" in df_copy.columns and "Shares Held" in df_copy.columns:
            # Calculate current price from Current Value / Shares Held
            calculated_prices = df_copy["Current Value"] / df_copy["Shares Held"]
            df_copy["Current Price (per share)"] = calculated_prices
        
        # Fetch live prices for all tickers
        for idx, ticker in enumerate(df_copy["Ticker"]):
            new_price = self.get_stock_price(ticker)
            if new_price is not None:
                df_copy.loc[idx, "Current Price (per share)"] = new_price
                logger.info(f"Updated price for {ticker}: {new_price}")
            else:
                logger.warning(f"Could not fetch price for {ticker}, keeping existing value")
        
        return df_copy
    
    def clear_cache(self) -> None:
        """Clear the price cache."""
        self._price_cache.clear()
    
    def get_batch_prices(self, tickers: List[str]) -> Dict[str, Optional[float]]:
        """
        Fetch prices for multiple tickers in batch.
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            Dictionary mapping tickers to their prices
        """
        prices = {}
        for ticker in tickers:
            prices[ticker] = self.get_stock_price(ticker)
        return prices 