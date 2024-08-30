import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QInputDialog
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import yfinance as yf
from wsimple.api import Wsimple
import pandas as pd

class WealthsimpleAPI:
    def __init__(self):
        self.client = None

    def get_otp(self):
        otp, ok = QInputDialog.getText(None, "OTP Required", "Enter OTP:")
        if ok:
            return otp
        else:
            return None

    def login(self, email, password):
        try:
            for attempt in range(3):  # Retry up to 3 times
                print(f"Attempt {attempt + 1} to log in...")
                self.client = Wsimple(email, password, otp_callback=self.get_otp)
                if self.client.is_operational():
                    print("Login successful!")
                    return True
                else:
                    print(f"Login attempt {attempt + 1} failed.")
            return False
        except Exception as e:
            print(f"Login failed: {e}")
            return False
        
    def get_account_details(self):
        if self.client:
            try:
                return self.client.get_accounts()
            except AttributeError as e:
                print(f"Error fetching account details: {e}")
                # Attempt to set the 'box' attribute manually
                if not hasattr(self.client, 'box'):
                    self.client.box = None
                return None
        return None

class Backtester:
    def __init__(self, data, moving_average_window=20):
        self.data = data
        self.moving_average_window = moving_average_window

    def run(self):
        # Ensure the 'Signal' column exists
        self.data['Signal'] = 0
        
        # Calculate the Moving Average
        self.data['Moving Average'] = self.data['Close'].rolling(window=self.moving_average_window).mean()
        
        # Generate buy/sell signals
        signals = (self.data['Close'].iloc[self.moving_average_window:] > self.data['Moving Average'].iloc[self.moving_average_window:]).astype(int)
        self.data.iloc[self.moving_average_window:, self.data.columns.get_loc('Signal')] = signals.values
        
        # Determine position changes
        self.data['Position'] = self.data['Signal'].diff()

        # Define Buy/Sell actions
        self.data['Buy'] = self.data['Position'] == 1
        self.data['Sell'] = self.data['Position'] == -1

        # Calculate returns
        self.data['Market Return'] = self.data['Close'].pct_change()
        self.data['Strategy Return'] = self.data['Market Return'] * self.data['Position'].shift(1)

        return self.data

class Dashboard(QMainWindow):
    def __init__(self, api: WealthsimpleAPI):
        super().__init__()
        self.setWindowTitle("Wealthsimple Trading Dashboard")
        self.setGeometry(100, 100, 1000, 700)
        
        self.api = api
        self.initUI()

        # Set up a timer for real-time data simulation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_real_time_data)
        self.timer.start(5000)  # Update every 5 seconds

        # Placeholder for real-time data
        self.real_time_data = yf.download('SOXL', period='1d', interval='1m')[-1:]

    def initUI(self):
        layout = QGridLayout()

        # Create panels
        self.soxl_graph = self.create_graph_panel("SOXL", "SOXL")
        self.vfv_graph = self.create_graph_panel("VFV.TO", "VFV.TO")
        self.backtesting_panel = self.create_backtesting_panel()
        self.real_time_trading_panel = self.create_real_time_trading_panel()
        self.account_info_panel = self.create_account_info_panel()

        # Add panels to the layout
        layout.addWidget(self.soxl_graph, 0, 0)
        layout.addWidget(self.vfv_graph, 0, 1)
        layout.addWidget(self.backtesting_panel, 1, 0)
        layout.addWidget(self.real_time_trading_panel, 1, 1)
        layout.addWidget(self.account_info_panel, 0, 2, 2, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_real_time_data(self):
        # Simulate real-time data by fetching the latest minute's data
        latest_data = yf.download('SOXL', period='1d', interval='1m')[-1:]
        self.real_time_data = pd.concat([self.real_time_data, latest_data])

        # Update the trading logic with the latest data
        self.run_real_time_trading()

    def run_real_time_trading(self):
        # Run the trading strategy on the latest data
        backtester = Backtester(self.real_time_data, moving_average_window=20)
        results = backtester.run()

        # Check for buy/sell signals
        if results['Buy'].iloc[-1]:
            self.display_trade("BUY", results.index[-1])
        elif results['Sell'].iloc[-1]:
            self.display_trade("SELL", results.index[-1])

    def display_trade(self, action, time):
        # Display the trade in the real-time trading panel
        trade_label = QLabel(f"{action} at {time}")
        self.real_time_trading_panel.layout().addWidget(trade_label)

    def create_graph_panel(self, title, ticker):
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel(title)
        layout.addWidget(label)

        canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(canvas)

        ax = canvas.figure.subplots()
        ax.set_title(f"{title} Price and Moving Average")

        # Fetching historical data
        try:
            data = yf.download(ticker, period='1y', interval='1d')
            if data.empty:
                raise ValueError(f"No data available for ticker: {ticker}")

            ax.plot(data.index, data['Close'], label='Close Price')
            data['Moving Average'] = data['Close'].rolling(window=20).mean()
            ax.plot(data.index, data['Moving Average'], label='20-Day Moving Average')
            ax.legend()
        except ValueError as e:
            ax.text(0.5, 0.5, str(e), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

        widget.setLayout(layout)
        return widget

    def create_backtesting_panel(self):
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Backtesting Results")
        layout.addWidget(label)

        # Example backtesting on SOXL data
        data = yf.download('SOXL', period='1y', interval='1d')
        backtester = Backtester(data)
        results = backtester.run()

        results_label = QLabel(f"Total Strategy Return: {results['Strategy Return'].cumsum().iloc[-1]:.2%}")
        layout.addWidget(results_label)

        widget.setLayout(layout)
        return widget

    def create_real_time_trading_panel(self):
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Real-time Trading")
        layout.addWidget(label)

        # Placeholder for real-time trading data display
        layout.addWidget(QLabel("Real-time trading information will be displayed here."))

        widget.setLayout(layout)
        return widget

    def create_account_info_panel(self):
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Account Information")
        layout.addWidget(label)

        # Fetch account details from the API
        account_info = self.api.get_account_details()

        if account_info:
            for account in account_info:
                balance_info = f"Account: {account['id']}, Balance: {account['current_balance']}"
                layout.addWidget(QLabel(balance_info))
        else:
            layout.addWidget(QLabel("Failed to retrieve account information."))

        widget.setLayout(layout)
        return widget

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wealthsimple Login")
        self.setGeometry(100, 100, 300, 200)
        
        self.api = WealthsimpleAPI()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Email")
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_login(self):
        email = self.username_input.text()
        password = self.password_input.text()
        
        if self.api.login(email, password):
            self.status_label.setText("Login Successful!")
            self.status_label.setStyleSheet("color: green;")
            self.load_dashboard()
        else:
            self.status_label.setText("Invalid Credentials")
            self.status_label.setStyleSheet("color: red;")

    def load_dashboard(self):
        self.dashboard = Dashboard(self.api)
        self.dashboard.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
