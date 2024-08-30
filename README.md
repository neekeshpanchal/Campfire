# 🌟 **Campfire Trading Platform (CTP)** 🌟

## Overview

Welcome to the **Campfire Trading Platform (CTP)**—your premier Python-based application for trading with confidence and precision! Built with PyQt5 and Matplotlib, CTP offers a comprehensive suite of tools for monitoring stocks, executing trades, and analyzing your trading strategies.

### Key Features

- **Secure Wealthsimple Login** 🔐: Easy and secure login with OTP verification to access your Wealthsimple account.
- **Real-Time Trading Dashboard** 📈: Monitor live stock data and execute trades based on a sophisticated moving average strategy.
- **Backtesting Engine** 📊: Evaluate historical data to fine-tune your trading strategies and optimize performance.
- **Interactive Graphs** 🎨: Visualize stock prices and moving averages with clear and engaging graphical representations.
- **Account Information** 💳: Access detailed information about your Wealthsimple accounts and balances.

## Installation

### Prerequisites

- Python 3.7 or higher
- PyQt5
- Matplotlib
- yfinance
- wsimple

Install the required packages using pip:

```bash
pip install PyQt5 matplotlib yfinance wsimple
```

### Running the Application

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/campfire-trading-platform.git
   cd campfire-trading-platform
   ```

2. **Start the Application**

   ```bash
   python main.py
   ```

## Usage

1. **Login**: Enter your Wealthsimple email and password, and provide OTP when prompted.
2. **Dashboard**: Access the main dashboard to:
   - View real-time stock data for SOXL and VFV.
   - Analyze backtesting results to refine your trading strategies.
   - Review your Wealthsimple account details.

## Code Structure

- **`main.py`**: The entry point for the application.
- **`WealthsimpleAPI`**: Handles Wealthsimple API interactions, including login and account details retrieval.
- **`Backtester`**: Implements and runs the moving average trading strategy for backtesting.
- **`Dashboard`**: The core interface displaying graphs, results, and account information.
- **`LoginWindow`**: The login interface for accessing the application.

## Contributing

We welcome contributions to make CTP even better! Please open an issue or submit a pull request with your improvements.

### How to Contribute

1. **Fork the Repository**
2. **Create a New Branch**: `git checkout -b feature/your-feature`
3. **Commit Your Changes**: `git commit -am 'Add new feature'`
4. **Push to the Branch**: `git push origin feature/your-feature`
5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyQt5 Documentation](https://www.riverbankcomputing.com/software/pyqt/intro)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [wsimple Documentation](https://github.com/wsimple/wsimple)

Enjoy trading with CTP! 🚀📈
