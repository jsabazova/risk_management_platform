import unittest
import numpy as np
from app import calculate_historical_var, calculate_variance_covariance_var, calculate_monte_carlo_var
from scipy.stats import norm

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

    def test_variance_covariance_var(self):
        # Calculate Variance-Covariance VaR
        var = calculate_variance_covariance_var(self.returns, self.confidence_level)
        # Calculate expected values
        mean_return = np.mean(self.returns)
        std_dev = np.std(self.returns)
        z_score = norm.ppf(1 - self.confidence_level)
        expected_var = mean_return - z_score * std_dev
        self.assertAlmostEqual(var, expected_var, places=6, msg="Variance-Covariance VaR calculation failed.")
    
    def test_monte_carlo_var(self):
        # Calculate Monte Carlo VaR
        var = calculate_monte_carlo_var(self.returns, self.confidence_level, num_simulations=10000)
        # Calculate expected values using Monte Carlo (generate same dummy data)
        mean_return = np.mean(self.returns)
        std_dev = np.std(self.returns)
        simulated_returns = np.random.normal(mean_return, std_dev, 10000)
        expected_var = np.percentile(simulated_returns, (1 - self.confidence_level) * 100)

        self.assertAlmostEqual(var, expected_var, places=3, msg="Monte Carlo VaR calculation failed.") 
        #calculation cant be more accurate than 3 places because each time its random and 5% has high tail sensitivity


    def test_empty_returns(self):
        # Test with empty returns array
        empty_returns = np.array([])
        var_historical = calculate_historical_var(empty_returns, self.confidence_level)
        var_var_cov = calculate_variance_covariance_var(empty_returns, self.confidence_level)
        var_monte_carlo = calculate_monte_carlo_var(empty_returns, self.confidence_level, num_simulations=10000)
        
        self.assertIsNone(var_historical, msg="Historical VaR should return None for empty returns.")
        self.assertIsNone(var_var_cov, msg="Variance-Covariance VaR should return None for empty returns.")
        self.assertIsNone(var_monte_carlo, msg="Monte Carlo VaR should return None for empty returns.")

    def test_single_return_value(self):
        # Test with a single return value
        single_return = np.array([0.01])
        var_historical = calculate_historical_var(single_return, self.confidence_level)
        var_var_cov = calculate_variance_covariance_var(single_return, self.confidence_level)
        var_monte_carlo = calculate_monte_carlo_var(single_return, self.confidence_level, num_simulations=10000)

        self.assertEqual(var_historical, 0.01, msg="Historical VaR should equal the single return value.")
        self.assertEqual(var_var_cov, 0.01, msg="Variance-Covariance VaR should equal the single return value.")
        self.assertEqual(var_monte_carlo, 0.01, msg="Monte Carlo VaR should equal the single return value.")
    
    def test_zero_confidence_level(self):
        zero_confidence = 0.0
        var_historical = calculate_historical_var(self.returns, zero_confidence)
        var_var_cov = calculate_variance_covariance_var(self.returns, zero_confidence)
        var_monte_carlo = calculate_monte_carlo_var(self.returns, zero_confidence, num_simulations=10000)

        self.assertEqual(var_historical, np.min(self.returns), msg="Historical VaR should be the minimum return at 0% confidence.")
        self.assertEqual(var_var_cov, np.min(self.returns), msg="Variance-Covariance VaR should be the minimum return at 0% confidence.")
        self.assertEqual(var_monte_carlo, np.min(self.returns), msg="Monte Carlo VaR should be the minimum return at 0% confidence.")
        
    def test_full_confidence_level(self):
        full_confidence = 1.0
        var_historical = calculate_historical_var(self.returns, full_confidence)
        var_var_cov = calculate_variance_covariance_var(self.returns, full_confidence)
        var_monte_carlo = calculate_monte_carlo_var(self.returns, full_confidence, num_simulations=10000)

        self.assertEqual(var_historical, np.max(self.returns), msg="Historical VaR should be the maximum return at 100% confidence.")
        self.assertEqual(var_var_cov, np.max(self.returns), msg="Variance-Covariance VaR should be the maximum return at 100% confidence.")
        self.assertEqual(var_monte_carlo, np.max(self.returns), msg="Monte Carlo VaR should be the maximum return at 100% confidence.")

if __name__ == '__main__':
    unittest.main()
