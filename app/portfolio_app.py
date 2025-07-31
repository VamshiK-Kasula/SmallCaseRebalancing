"""
Main application class for portfolio rebalancing.
"""
import pandas as pd
import logging
import streamlit as st
from typing import Optional

from services.price_service import PriceService
from services.data_service import DataService
from ui.components import PortfolioUIComponents
from utils.portfolio_utils import calculate_portfolio_metrics, calculate_rebalancing_metrics, validate_portfolio_data
from config.settings import app_config

logger = logging.getLogger(__name__)


class PortfolioRebalancerApp:
    """Main application class for portfolio rebalancing."""
    
    def __init__(self):
        """Initialize the application with all required services."""
        self.price_service = PriceService()
        self.data_service = DataService(app_config.SAVE_FILE)
        self.ui = PortfolioUIComponents()
    
    def run(self) -> None:
        try:
            print("Running application")

            # 1. Load user data from session state or file
            if 'portfolio_df' not in st.session_state:
                st.session_state['portfolio_df'] = self.data_service.load_portfolio_data()
            user_df = st.session_state['portfolio_df']

            # 2. Show editable table (user_df is always the user's last edit)
            edited_df = self.ui.render_portfolio_table(user_df)

            # 3. If user made changes, update session state
            if not edited_df.equals(user_df):
                st.session_state['portfolio_df'] = edited_df
                st.success("✅ Changes saved to session!")

            # 4. For calculations and display, create a copy and update prices
            display_df = self.price_service.update_portfolio_prices(edited_df.copy())

            # 5. Show metrics, charts, etc. using display_df
            self._display_portfolio_metrics(display_df)
            self._handle_rebalancing(display_df)
            self.ui.render_footer()

        except Exception as e:
            logger.error(f"Application error: {e}")
            self.ui.render_error_message(str(e))
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Update prices and calculate metrics.
        
        Args:
            df: DataFrame to process
            
        Returns:
            Processed DataFrame with current prices and metrics
        """
        # Update prices
        df = self.price_service.update_portfolio_prices(df)
        
        # Calculate metrics
        total_value, _, _ = calculate_portfolio_metrics(df)
        
        return df
    
    def _save_user_data_to_file(self, df: pd.DataFrame) -> None:
        """
        Save user data to file (only user-editable columns).
        
        Args:
            df: DataFrame with user edits
        """
        try:
            # Only save user-editable columns
            user_columns = ["Ticker", "Shares Held", "Target Weight (%)"]
            user_data = df[user_columns].copy()
            
            # Preserve original prices from session state
            if "Current Price (per share)" in st.session_state['portfolio_df'].columns:
                user_data["Current Price (per share)"] = st.session_state['portfolio_df']["Current Price (per share)"]
            
            self.data_service.save_portfolio_data(user_data)
            st.success("💾 Changes saved permanently to file!")
            
        except Exception as e:
            st.error(f"❌ Error saving to file: {e}")
            logger.error(f"Error saving user data: {e}")
    
    def _display_portfolio_metrics(self, df: pd.DataFrame) -> None:
        """
        Display portfolio metrics and summary.
        
        Args:
            df: Portfolio DataFrame
        """
        # Calculate metrics
        total_value, total_current_weight, total_target_weight = calculate_portfolio_metrics(df)
        
        # Display weight summary
        self.ui.render_weight_summary(df)
        
        # Display total value
        self.ui.render_total_value(total_value)
    
    def _handle_rebalancing(self, df: pd.DataFrame) -> None:
        """
        Handle the rebalancing process.
        
        Args:
            df: Portfolio DataFrame
        """
        # Get additional capital input
        additional_amount = self.ui.render_additional_capital_input()
        
        # Check if rebalance button is clicked
        if self.ui.render_rebalance_button():
            self._perform_rebalancing(df, additional_amount)
    
    def _perform_rebalancing(self, df: pd.DataFrame, additional_amount: float) -> None:
        """
        Perform the rebalancing calculations and display results.
        
        Args:
            df: Portfolio DataFrame
            additional_amount: Additional capital to invest
        """
        try:
            # Validate data
            errors = validate_portfolio_data(df)
            if errors:
                for error in errors:
                    self.ui.render_error_message(error)
                return
            
            # Save current user data to file (only user-editable columns)
            user_columns = ["Ticker", "Shares Held", "Target Weight (%)"]
            user_data = df[user_columns].copy()
            
            # Add current prices from session state (preserve user-set prices)
            if "Current Price (per share)" in st.session_state['portfolio_df'].columns:
                user_data["Current Price (per share)"] = st.session_state['portfolio_df']["Current Price (per share)"]
            
            self.data_service.save_portfolio_data(user_data)
            st.success("💾 Portfolio data saved to file!")
            
            # Calculate rebalancing metrics
            rebalanced_df = calculate_rebalancing_metrics(df, additional_amount)
            
            # Display results
            self.ui.render_rebalanced_portfolio(rebalanced_df)
            
            # Provide download option
            self.ui.render_download_button(rebalanced_df)
            
            # Show suggestion for additional investment
            suggested_amount = self.data_service.get_suggested_additional_amount(
                rebalanced_df["Target Value"], 
                df["Current Value"].sum()
            )
            self.ui.render_suggestion_message(suggested_amount, additional_amount)
            
        except Exception as e:
            logger.error(f"Rebalancing error: {e}")
            self.ui.render_error_message(str(e))
    
    def get_portfolio_summary(self, df: pd.DataFrame) -> dict:
        """
        Get a summary of portfolio metrics.
        
        Args:
            df: Portfolio DataFrame
            
        Returns:
            Dictionary with portfolio summary
        """
        total_value, total_current_weight, total_target_weight = calculate_portfolio_metrics(df)
        
        return {
            "total_value": total_value,
            "total_current_weight": total_current_weight,
            "total_target_weight": total_target_weight,
            "holdings_count": len(df),
            "additional_capital": 0.0  # This would be set by the UI
        } 