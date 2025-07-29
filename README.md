# Basket Portfolio Rebalancer

A Streamlit-based web application for rebalancing custom Basket portfolios. The application automatically fetches live stock prices and provides actionable recommendations for buying/selling shares to achieve target allocations.

## Features

- 📊 **Live Price Fetching**: Automatically fetches current stock prices using yfinance
- 🎯 **Portfolio Rebalancing**: Calculates optimal buy/sell recommendations
- 💰 **Additional Capital Support**: Handles additional investment amounts
- 📈 **Real-time Metrics**: Shows current vs target weights and portfolio value
- 📥 **Export Functionality**: Download rebalanced portfolio as CSV
- 🎨 **Modern UI**: Clean, responsive interface built with Streamlit

## Prerequisites

- Python 3.8 or higher
- pipenv (for virtual environment management)

## Installation & Setup

### Option 1: Local Development

#### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd pythonProject
```

#### Step 2: Install pipenv (if not already installed)
```bash
pip install pipenv
```

#### Step 3: Set up Virtual Environment and Install Dependencies
```bash
# Create virtual environment and install dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

#### Step 4: Verify Installation
```bash
# Test that the application can be imported
python -c "from app.portfolio_app import PortfolioRebalancerApp; print('Setup successful!')"
```

### Option 2: Deploy to Streamlit Cloud (Recommended)

#### Step 1: Fork/Clone the Repository
1. Fork this repository to your GitHub account
2. Or clone it locally and push to your own repository

#### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the path to your app: `main.py`
6. Click "Deploy"

#### Step 3: Access Your App
- Your app will be available at: `https://your-app-name.streamlit.app`
- The app will automatically redeploy when you push changes to your repository

## Usage

### Step 1: Start the Application
```bash
# Make sure you're in the virtual environment
pipenv shell

# Run the Streamlit application
streamlit run main.py
```

### Step 2: Access the Application
- Open your web browser
- Navigate to: `http://localhost:8501`
- The application will load with your portfolio data

### Step 3: Using the Application

1. **View Current Portfolio**: The application loads your portfolio from `data/tornado.json` and automatically fetches live prices
2. **Edit Holdings**: Modify ticker symbols, shares held, or target weights as needed
3. **Add Capital**: Optionally enter additional amount to invest
4. **Rebalance**: Click "🔄 Rebalance Portfolio" to see recommendations
5. **Download Results**: Export the rebalanced portfolio as CSV

## Project Structure

```
pythonProject/
├── app/
│   ├── __init__.py
│   └── portfolio_app.py          # Main application logic
├── config/
│   ├── __init__.py
│   └── settings.py               # Application configuration
├── data/
│   └── tornado.json             # Sample portfolio data
├── models/
│   ├── __init__.py
│   └── portfolio.py             # Portfolio data models
├── services/
│   ├── __init__.py
│   ├── data_service.py          # Data persistence service
│   └── price_service.py         # Live price fetching service
├── ui/
│   ├── __init__.py
│   └── components.py            # Streamlit UI components
├── utils/
│   ├── __init__.py
│   └── portfolio_utils.py       # Portfolio calculation utilities
├── main.py                      # Application entry point
├── Pipfile                      # pipenv dependencies
├── Pipfile.lock                 # Locked dependency versions
└── requirements.txt             # Traditional requirements file
```

## Configuration

### Portfolio Data
- Default portfolio data is stored in `data/tornado.json`
- The application automatically fetches live prices for all tickers
- Supported ticker formats: `SYMBOL.NS` (NSE), `SYMBOL.BO` (BSE), etc.

### Application Settings
- Configuration is managed in `config/settings.py`
- Data file path can be modified in the settings

## Development

### Running in Development Mode
```bash
# Activate virtual environment
pipenv shell

# Run with auto-reload
streamlit run main.py --server.runOnSave true
```

### Testing
```bash
# Run the test script to verify price fetching
python test_price_service.py
```

### Adding New Dependencies
```bash
# Add a new package
pipenv install package-name

# Add a development dependency
pipenv install package-name --dev
```

## Deployment

### Streamlit Cloud (Recommended)
The easiest way to deploy your app:

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Streamlit Cloud**: 
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and set `main.py` as the app path
3. **Deploy**: Click "Deploy" and wait for the build to complete
4. **Access**: Your app will be live at `https://your-app-name.streamlit.app`

### GitHub Actions
The repository includes a GitHub Actions workflow that:
- Tests the application on every push
- Can be configured for automatic deployment
- Ensures code quality and functionality

### Local Deployment
For local deployment or custom hosting:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### Environment Variables
For production deployment, consider setting:
- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Use a different port
   streamlit run main.py --server.port 8502
   ```

2. **Price Fetching Issues**
   - Check internet connection
   - Verify ticker symbols are correct
   - Some stocks may not have live data available

3. **Virtual Environment Issues**
   ```bash
   # Recreate virtual environment
   pipenv --rm
   pipenv install
   ```

### Logs
- Application logs are displayed in the terminal
- Check for error messages related to price fetching or data loading

## Dependencies

### Core Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **yfinance**: Yahoo Finance API for stock prices

### Development Dependencies
- **pipenv**: Virtual environment and dependency management

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Create an issue in the repository 