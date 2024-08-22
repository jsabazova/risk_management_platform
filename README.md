### **Risk Management Platform**

This is a simple Flask app that calculates the Value at Risk (VaR) for a portfolio of stocks. You can input your stocks and their weights, and it will give you an idea of how much you might lose on a bad day. There are three ways to calculate VaR: Historical Method, Variance-Covariance Method, and Monte Carlo Simulation.

### **Features**
- **Calculate VaR**: Get the potential loss amount using three different methods.
- **Input Stocks and Weights**: Just enter the stock tickers and how much of each you have
- **Basic Web Interface**: Ugly looking react form, but it works.

### **How to Use**
1. **Clone the Repo and set up env**:
   ```bash
   git clone https://github.com/yourusername/risk-management-platform.git
   cd risk-management-platform
   ```

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000/` in your browser.

3. **Enter Your Portfolio**:
   - **Tickers**: Type the stock symbols (e.g., AAPL, MSFT).
   - **Weights**: How much of each stock (e.g., 0.4, 0.6).
   - **Confidence Level**: Default is 95%, but you can change it.
   - **Start Date**: Historical data start date (e.g., 2020-01-01).

4. **Calculate VaR**: Choose a method and hit the button.

### **VaR Calculation Methods**
1. **Historical Method**: Uses actual past returns to calculate potential loss. Good for seeing what might happen if the future looks like the past (which it sometimes doesnt).
   
2. **Variance-Covariance Method**: Assumes returns follow a normal distribution. It’s quick but might not be super accurate.
   
3. **Monte Carlo Simulation**: Runs a bunch of random scenarios to see what could happen. It’s more flexible but takes more time to run.

### **Comparing the Methods**
- **Historical**: Real data, but only works if history repeats itself.
- **Variance-Covariance**: Fast, but may miss out on weird market moves.
- **Monte Carlo**: More thorough but slower.

### **Future Development**
- **More Risk Metrics**: Maybe will add CVaR or other calculations.
- **Graphs**: Could be cool to visualize the data.
- **Save Portfolios**: Let users save their stock portfolios for later.
- **Backtesting**: Compare the VaR results with actual past losses to see how well each method works.

