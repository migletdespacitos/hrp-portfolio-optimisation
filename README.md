# HRP Portfolio Optimisation

A Python-based implementation of the Hierarchical Risk Parity (HRP) algorithm for portfolio optimisation.

## Overview

Hierarchical Risk Parity (HRP) is an advanced portfolio optimisation technique that addresses some of the limitations of traditional methods like Mean-Variance Optimisation. HRP leverages hierarchical clustering to allocate portfolio weights, aiming to create a more robust and diversified portfolio.

## Features

- **Data Fetching**: Retrieves historical stock data using Yahoo Finance.
- **HRP Algorithm**: Implements the HRP algorithm for portfolio weight optimisation using the [PyPortfolioOpt](https://pypi.org/project/PyPortfolioOpt/) library.
- **Portfolio Metrics**: Calculates expected annual return and portfolio volatility.
- **Capital Allocation**: Allocates initial capital based on the latest stock prices.
- **User Interaction**: Interactive prompts for inputting stock tickers, date ranges, and initial capital.

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed. You can download it from the [official website](https://www.python.org/downloads/).
- **GitHub Account**: If you haven't already, [create a GitHub account](https://github.com/join).

## Usage

1. **Clone the Repository:**
   - Go to the GitHub repository page: `https://github.com/migletdespacitos/hrp-portfolio-optimisation`.
   - Click on the green **"Code"** button and copy the repository URL.

2. **Download the Files:**
   - Since you're using the web interface, you'll upload the files directly without cloning.

3. **Run the Script:**
   - Open your terminal or command prompt.
   - Navigate to the directory containing `hrp.py`.
   - Run the script using:
     ```bash
     python hrp.py
     ```

## Dependencies

The project relies on the following Python libraries:

- [yfinance](https://pypi.org/project/yfinance/): For fetching historical stock data.
- [pandas](https://pypi.org/project/pandas/): Data manipulation and analysis.
- [numpy](https://pypi.org/project/numpy/): Numerical computing.
- [PyPortfolioOpt](https://pypi.org/project/PyPortfolioOpt/): Portfolio optimization library.


## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) by Robert Martin for the portfolio optimization library.
- [yfinance](https://github.com/ranaroussi/yfinance) by Ran Aroussi for fetching financial data.
- Inspired by the work on Hierarchical Risk Parity by Marcos López de Prado.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**
   ```bash
   git checkout -b feature/YourFeatureName
