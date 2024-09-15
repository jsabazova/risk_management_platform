import time
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import norm
import os

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask
import matplotlib.pyplot as plt



app = Flask(__name__)

def calculate_historical_var(returns, confidence_level):
    if returns.size == 0:
        return None
    if confidence_level == 1.0:
        return np.max(returns)
    if confidence_level == 0.0:
        return np.min(returns)
    var = np.percentile(returns, (1 - confidence_level) * 100)
    return var

def calculate_variance_covariance_var(returns, confidence_level):
    if returns.size == 0:
        return None
    if confidence_level == 1.0:
        return np.max(returns)
    if confidence_level == 0.0:
        return np.min(returns)

    mean = returns.mean()
    std_dev = returns.std()
    z_score = norm.ppf(1 - confidence_level)
    var = mean - z_score * std_dev
    return var

def calculate_monte_carlo_var(returns, confidence_level, num_simulations=10000):
    if returns.size == 0:
        return None
    if confidence_level == 1.0:
        return np.max(returns)
    if confidence_level == 0.0:
        return np.min(returns)

    mean = returns.mean()
    std_dev = returns.std()
    simulated_returns = np.random.normal(mean, std_dev, num_simulations)
    var = np.percentile(simulated_returns, (1 - confidence_level) * 100)
    return var

def calculate_cvar(returns, var_threshold):
    losses_beyond_var = returns[returns <= var_threshold]
    if losses_beyond_var.size == 0:
        return None
    cvar = losses_beyond_var.mean()
    return cvar

@app.route('/', methods=['GET', 'POST'])
def index():
    var = None
    cvar = None  # To store the CVaR value
    error = None
    if request.method == 'POST':
        print("Form submitted")
        tickers = [ticker.strip() for ticker in request.form['tickers'].split(',')]
        print(f"Tickers: {tickers}")
        weights_input = request.form['weights']
        print(f"Weights entered: {weights_input}")

        weights = list(map(float, weights_input.split(',')))
        print(f"Parsed weights: {weights}")

        # Validation for tickers and weights
        if len(tickers) != len(weights):
            error = "The number of tickers must match the number of weights."
            return render_template('index.html', error=error)

        # Normalize the weights
        weights = [w / sum(weights) for w in weights]
        print(f"Normalized weights: {weights}")
        
        print(f"Weights: {weights}")
        confidence_level = float(request.form['confidence_level'])
        print(f"Confidence Level: {confidence_level}")
        start_date = request.form['start_date']
        print(f"Start Date: {start_date}")
        method = request.form['method']
        print(f"Method: {method}")

        # Validation for tickers and weights
        if len(tickers) != len(weights):
            error = "The number of tickers must match the number of weights."
            return render_template('index.html', error=error)

        if sum(weights) != 1.0:
            error = "The weights must sum up to 1."
            return render_template('index.html', error=error)

        try:
            data = yf.download(tickers, start=start_date)['Adj Close']
            print("Downloaded data")

            if data.empty:
                error = "No data available for the given tickers and date range."
                return render_template('index.html', error=error)

            returns = data.pct_change().dropna()
            print("Calculated returns")

            if returns.empty:
                error = "No returns data available after processing. Check the tickers and date range."
                return render_template('index.html', error=error)

            portfolio_returns = returns.dot(weights)
            print(f"Portfolio Returns: {portfolio_returns}")

            # Call the appropriate VaR function and generate the plot
            if method == 'historical':
                print("Generating historical VaR plot")
                var = calculate_historical_var(portfolio_returns, confidence_level)
                var = round(var,4)
                try:
                    plot_historical_var(portfolio_returns, var)
                    print("Historical VaR plot generated and saved")
                except Exception as e:
                    print(f"Error while generating Historical VaR plot: {e}")
                cvar = calculate_cvar(portfolio_returns, var)
                cvar = round(cvar, 4) 
    
            elif method == 'variance_covariance':
                print("Generating variance-covariance VaR plot")
                var = calculate_variance_covariance_var(portfolio_returns, confidence_level)
                var = round(var,4)
                try:
                    plot_var_covariance(portfolio_returns.mean(), portfolio_returns.std(), var)
                    print("Variance-Covariance VaR plot generated and saved")
                except Exception as e:
                    print(f"Error while generating Variance-Covariance VaR plot: {e}")
                cvar = calculate_cvar(portfolio_returns, var)
                cvar = round(cvar, 4) 
    
            elif method == 'monte_carlo':
                print("Generating Monte Carlo VaR plot")
                var = calculate_monte_carlo_var(portfolio_returns, confidence_level)
                var = round(var,4)
                try:
                    plot_monte_carlo(np.random.normal(portfolio_returns.mean(), portfolio_returns.std(), 10000), var)
                    print("Monte Carlo VaR plot generated and saved")
                except Exception as e:
                    print(f"Error while generating Monte Carlo VaR plot: {e}")
                cvar = calculate_cvar(np.random.normal(portfolio_returns.mean(), portfolio_returns.std(), 10000), var)
                cvar = round(cvar, 4) 

            print(f"VaR: {var}, CVaR: {cvar}")
            return render_template('index.html', var=var, cvar=cvar, tickers=tickers, weights=weights, method=method, time=time)

        except Exception as e:
            error = str(e)
            print(f"Error: {error}")

    return render_template('index.html', error=error, time = time)


### Plotting the graphs
def plot_historical_var(losses, var_threshold):
    plt.figure(figsize=(10, 5))
    plt.plot(losses, label="Historical Losses")
    plt.axhline(y=var_threshold, color='r', linestyle='--', label="VaR Threshold")
    plt.legend()
    plt.title("Historical Losses vs VaR Threshold")
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/historical_var.png')
    plt.savefig(output_path)
    print(f"Saved Historical VaR plot to {output_path}")
    plt.close()

def plot_var_covariance(mean, std_dev, var_threshold):
    x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
    plt.plot(x, 1/(std_dev * np.sqrt(2 * np.pi)) * np.exp(- (x - mean)**2 / (2 * std_dev**2)))
    plt.axvline(x=var_threshold, color='r', linestyle='--', label="VaR")
    plt.title("Normal Distribution with VaR")
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/var_covariance.png')
    plt.savefig(output_path)
    print(f"Saved Variance-Covariance VaR plot to {output_path}")
    plt.close()

def plot_monte_carlo(simulated_returns, var_threshold):
    plt.hist(simulated_returns, bins=50, alpha=0.7)
    plt.axvline(x=var_threshold, color='r', linestyle='--', label="VaR Threshold")
    plt.title("Monte Carlo Simulation of Portfolio Returns")
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/monte_carlo.png')
    plt.savefig(output_path)
    print(f"Saved Monte Carlo VaR plot to {output_path}")
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)



## need to write out what the output means, include the x and y axis varibale names