"""
Main entry point for the Portfolio Rebalancing Application.

This application helps users rebalance their custom Basket portfolios
by comparing current allocations with target weights and providing
actionable recommendations for buying/selling shares.
"""

import logging
from app.portfolio_app import PortfolioRebalancerApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main application entry point."""
    try:
        # Create and run the application
        app = PortfolioRebalancerApp()
        app.run()
        
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        raise

if __name__ == "__main__":
    main() 