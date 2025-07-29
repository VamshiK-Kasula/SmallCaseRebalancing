# Deployment Guide

This guide covers different ways to deploy your Smallcase Portfolio Rebalancer application.

## 🚀 Quick Start: Streamlit Cloud (Easiest)

### Step 1: Prepare Your Repository
1. Ensure your code is in a GitHub repository
2. Make sure `main.py` is in the root directory
3. Verify `requirements.txt` exists and is up to date

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the details:
   - **Repository**: Select your repository
   - **Branch**: `main` or `master`
   - **Main file path**: `main.py`
   - **App URL**: Choose a unique name for your app
5. Click "Deploy"

### Step 3: Access Your App
- Your app will be available at: `https://your-app-name.streamlit.app`
- It will automatically redeploy when you push changes to your repository

## 🌐 Alternative Deployment Options

### Option 1: Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy using Heroku CLI:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 2: Railway
1. Connect your GitHub repository to Railway
2. Set the start command: `streamlit run main.py --server.port=$PORT`
3. Deploy automatically

### Option 3: Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```
3. Deploy: `vercel`

### Option 4: DigitalOcean App Platform
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0`

## 🔧 Configuration

### Environment Variables
Set these in your deployment platform:

```bash
# Optional: Custom port
STREAMLIT_SERVER_PORT=8501

# Optional: Server address
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Optional: Enable debug mode
STREAMLIT_DEBUG=false
```

### Streamlit Configuration
The `.streamlit/config.toml` file is already configured for production:

```toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## 📊 Monitoring and Logs

### Streamlit Cloud
- Logs are available in the Streamlit Cloud dashboard
- Monitor app performance and errors
- Set up alerts for deployment failures

### Custom Hosting
- Check your hosting platform's logging system
- Monitor application performance
- Set up error tracking (e.g., Sentry)

## 🔒 Security Considerations

### Data Privacy
- The app doesn't store sensitive data
- All calculations are done in memory
- Portfolio data is only stored locally in the user's session

### API Rate Limits
- yfinance has rate limits for price fetching
- Consider implementing caching for production use
- Monitor API usage and implement fallbacks

## 🚨 Troubleshooting

### Common Deployment Issues

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Port Issues**
   - Use `$PORT` environment variable for cloud platforms
   - Set `--server.address=0.0.0.0` for external access

3. **Memory Issues**
   - Streamlit apps have memory limits
   - Optimize data processing for large portfolios

4. **API Failures**
   - Implement retry logic for price fetching
   - Add fallback data sources

### Debug Commands
```bash
# Test locally with production settings
streamlit run main.py --server.headless true

# Check dependencies
pip list

# Test imports
python -c "import streamlit; import pandas; import yfinance; print('All imports successful')"
```

## 📈 Performance Optimization

### For Production
1. **Caching**: Implement price caching to reduce API calls
2. **Lazy Loading**: Load data only when needed
3. **Error Handling**: Graceful degradation when services fail
4. **Monitoring**: Track app performance and user behavior

### Scaling Considerations
- Streamlit Cloud handles scaling automatically
- For custom hosting, consider load balancing
- Implement connection pooling for database operations

## 🔄 Continuous Deployment

### GitHub Actions
The included workflow automatically:
- Tests the application on every push
- Ensures code quality
- Can be extended for automatic deployment

### Manual Deployment
For manual deployments:
1. Test locally first
2. Push to staging branch
3. Deploy to staging environment
4. Test thoroughly
5. Deploy to production

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review platform-specific documentation
3. Check Streamlit Cloud status page
4. Create an issue in the repository 