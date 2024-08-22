import unittest
import numpy as np
from app import calculate_historical_var, calculate_var_cov_var, calculate_monte_carlo_var

class TestVaRCalculations(unittest.TestCase):
    
    def setUp(self):
        # Set up some dummy portfolio returns data
        self.returns = np.array([0.01, 0.02, -0.01, -0.03, 0.04, -0.02])
        self.confidence_level = 0.95

    def test_historical_var(self):
        # Calculate historical VaR
        var = calculate_historical_var(self.returns, self.confidence_level)
        # Expected output should be around the 5th percentile
        expected_var = np.percentile(self.returns, (1 - self.confidence_level) * 100)
        self.assertAlmostEqual(var, expected_var, places=6, msg="Historical VaR calculation failed.")

    def test_var_cov_var(self):
        # Calculate Variance-Covariance VaR
        var = calculate_var_cov_var(self.returns, self.confidence_level)
        # Calculate expected values
        mean_return = np.mean(self.returns)
        std_dev = np.std(self.returns)
        z_score = np.abs(np.percentile(np.random.randn(100000), self.confidence_level * 100))
        expected_var = mean_return - z_score * std_dev
        self.assertAlmostEqual(var, expected_var, places=6, msg="Variance-Covariance VaR calculation failed.")
    
    def test_monte_carlo_var(self):
        # Calculate Monte Carlo VaR
        var = calculate_monte_carlo_var(self.returns, self.confidence_level, simulations=10000)
        # Calculate expected values using Monte Carlo (generate same dummy data)
        mean_return = np.mean(self.returns)
        std_dev = np.std(self.returns)
        simulated_returns = np.random.normal(mean_return, std_dev, 10000)
        expected_var = np.percentile(simulated_returns, (1 - self.confidence_level) * 100)
        self.assertAlmostEqual(var, expected_var, places=6, msg="Monte Carlo VaR calculation failed.")

if __name__ == '__main__':
    unittest.main()
