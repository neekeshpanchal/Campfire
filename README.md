🌟 Campfire Trading Platform (CTP) 🌟
Overview
Welcome to the Campfire Trading Platform (CTP)—your premier Python-based application for trading with confidence and precision! Built with PyQt5 and Matplotlib, CTP offers a comprehensive suite of tools for monitoring stocks, executing trades, and analyzing your trading strategies.

Key Features
Secure Wealthsimple Login 🔐: Easy and secure login with OTP verification to access your Wealthsimple account.
Real-Time Trading Dashboard 📈: Monitor live stock data and execute trades based on a sophisticated moving average strategy.
Backtesting Engine 📊: Evaluate historical data to fine-tune your trading strategies and optimize performance.
Interactive Graphs 🎨: Visualize stock prices and moving averages with clear and engaging graphical representations.
Account Information 💳: Access detailed information about your Wealthsimple accounts and balances.
Installation
Prerequisites
Python 3.7 or higher
PyQt5
Matplotlib
yfinance
wsimple
Install the required packages using pip:

bash
Copy code
pip install PyQt5 matplotlib yfinance wsimple
Running the Application
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/campfire-trading-platform.git
cd campfire-trading-platform
Start the Application

bash
Copy code
python main.py
Usage
Login: Enter your Wealthsimple email and password, and provide OTP when prompted.
Dashboard: Access the main dashboard to:
View real-time stock data for SOXL and VFV.
Analyze backtesting results to refine your trading strategies.
Review your Wealthsimple account details.
Code Structure
main.py: The entry point for the application.
WealthsimpleAPI: Handles Wealthsimple API interactions, including login and account details retrieval.
Backtester: Implements and runs the moving average trading strategy for backtesting.
Dashboard: The core interface displaying graphs, results, and account information.
LoginWindow: The login interface for accessing the application.
Contributing
We welcome contributions to make CTP even better! Please open an issue or submit a pull request with your improvements.

How to Contribute
Fork the Repository
Create a New Branch: git checkout -b feature/your-feature
Commit Your Changes: git commit -am 'Add new feature'
Push to the Branch: git push origin feature/your-feature
Open a Pull Request
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
PyQt5 Documentation
Matplotlib Documentation
yfinance Documentation
wsimple Documentation
