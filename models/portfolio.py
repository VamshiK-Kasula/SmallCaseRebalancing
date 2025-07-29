"""
Portfolio model for managing portfolio data and calculations.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np


@dataclass
class PortfolioHolding:
    """Represents a single holding in a portfolio."""
    ticker: str
    shares_held: int
    target_weight: float
    current_price: Optional[float] = None
    
    @property
    def current_value(self) -> float:
        """Calculate current value of the holding."""
        if self.current_price is None:
            return 0.0
        return self.shares_held * self.current_price
    
    @property
    def current_weight(self) -> float:
        """Calculate current weight percentage."""
        return 0.0  # Will be calculated by Portfolio class


@dataclass
class Portfolio:
    """Represents a complete portfolio with holdings and calculations."""
    holdings: List[PortfolioHolding] = field(default_factory=list)
    additional_capital: float = 0.0
    
    def add_holding(self, holding: PortfolioHolding) -> None:
        """Add a holding to the portfolio."""
        self.holdings.append(holding)
    
    def get_total_value(self) -> float:
        """Calculate total current value of the portfolio."""
        return sum(holding.current_value for holding in self.holdings)
    
    def get_total_value_with_additional(self) -> float:
        """Calculate total value including additional capital."""
        return self.get_total_value() + self.additional_capital
    
    def calculate_weights(self) -> None:
        """Calculate current weights for all holdings."""
        total_value = self.get_total_value()
        if total_value == 0:
            return
            
        for holding in self.holdings:
            holding.current_weight = (holding.current_value / total_value) * 100
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert portfolio to pandas DataFrame."""
        data = []
        for holding in self.holdings:
            data.append({
                "Ticker": holding.ticker,
                "Shares Held": holding.shares_held,
                "Target Weight (%)": holding.target_weight,
                "Current Price (per share)": holding.current_price,
                "Current Value": holding.current_value,
                "Current Weight (%)": getattr(holding, 'current_weight', 0.0)
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            # Reorder columns
            columns_order = [
                "Ticker", "Current Price (per share)", "Shares Held",
                "Current Value", "Current Weight (%)", "Target Weight (%)"
            ]
            df = df[columns_order]
        
        return df
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, additional_capital: float = 0.0) -> 'Portfolio':
        """Create portfolio from pandas DataFrame."""
        portfolio = cls(additional_capital=additional_capital)
        
        for _, row in df.iterrows():
            holding = PortfolioHolding(
                ticker=row["Ticker"],
                shares_held=int(row["Shares Held"]),
                target_weight=float(row["Target Weight (%)"]),
                current_price=row.get("Current Price (per share)")
            )
            portfolio.add_holding(holding)
        
        portfolio.calculate_weights()
        return portfolio
    
    def get_rebalancing_data(self) -> pd.DataFrame:
        """Generate rebalancing calculations and return as DataFrame."""
        total_value = self.get_total_value_with_additional()
        
        rebalancing_data = []
        for holding in self.holdings:
            target_value = (holding.target_weight / 100.0) * total_value
            target_shares = int(round(target_value / holding.current_price)) if holding.current_price and holding.current_price > 0 else 0
            target_value_actual = target_shares * (holding.current_price or 0)
            difference = target_value_actual - holding.current_value
            action = "Buy" if difference > 0 else ("Sell" if difference < 0 else "Hold")
            shares_to_trade = target_shares - holding.shares_held
            
            rebalancing_data.append({
                "Ticker": holding.ticker,
                "Current Price (per share)": holding.current_price,
                "Shares Held": holding.shares_held,
                "Current Value": holding.current_value,
                "Current Weight (%)": getattr(holding, 'current_weight', 0.0),
                "Target Weight (%)": holding.target_weight,
                "Target Value": target_value,
                "Target Shares": target_shares,
                "Target Value (Actual)": target_value_actual,
                "Difference": difference,
                "Action": action,
                "Shares to Buy/Sell": shares_to_trade
            })
        
        df = pd.DataFrame(rebalancing_data)
        
        # Calculate real weights
        total_rebalanced_value = df["Target Value (Actual)"].sum()
        if total_rebalanced_value > 0:
            df["Real Weight (%)"] = (df["Target Value (Actual)"] / total_rebalanced_value * 100).round(2)
        else:
            df["Real Weight (%)"] = 0.0
        
        return df 