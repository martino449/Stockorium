# Stockorium
The program simulates a stock market with user accounts, portfolios, and trading capabilities. It also includes features such as encrypted data storage to protect user information and market data. Here's a breakdown of the main components and their functions:

### 1. Encryption and Data Persistence
Key Management: The program generates and manages a secret key for encryption. This key is used to encrypt and decrypt data files to ensure that sensitive information remains secure.
Data Storage: User information, portfolios, and market data are saved to and loaded from encrypted files. The files include:
users_data.pkl for storing user credentials and portfolio references.
{username}_portfolio.pkl for storing individual user portfolios.
market_data.pkl for storing market stock information.
### 2. Classes
Stock
Represents a stock in the market. Each stock has:

Symbol: A unique identifier for the stock (e.g., "AAPL").
Price: The current trading price of the stock.
Quantity: The number of shares available in the market.
History: A record of price changes over time.
Portfolio
Represents a user's collection of stocks and their financial balance. It includes:

Stocks: A dictionary of stocks owned by the user, with quantities.
Balance: The amount of money available for trading.
Transaction Fee: A fixed fee applied to each transaction (buy or sell).
Methods include:

buy_stock: Allows the user to buy a specified quantity of a stock if sufficient balance and quantity are available.
sell_stock: Allows the user to sell a specified quantity of a stock if sufficient shares are owned.
get_portfolio_value: Calculates the total value of the portfolio, including the balance and the current value of owned stocks.
Market
Represents the stock market. It contains:

Stocks: A dictionary of available stocks in the market.
Methods include:

add_stock: Adds a new stock to the market with an initial price and quantity.
get_stock: Retrieves information about a specific stock.
update_market: Updates stock prices based on simulated market fluctuations.
User
Represents an individual user, including their credentials and portfolio.

UserManager
Manages user registration and login. It provides:

register: Registers a new user.
login: Authenticates a user and retrieves their portfolio.
### 3. User Interaction
Main Menu: Users can view the market, register, log in, or exit the program.
User Menu: After logging in, users can:
View their portfolio.
Buy or sell stocks.
Add new stocks to the market.
Update market prices.
Check the transaction fee.
### 4. Serialization and Deserialization
Serialization: Converts Stock, Portfolio, and Market objects into a format suitable for saving to a file (using pickle).
Deserialization: Converts saved data back into objects when loading from a file.
### 5. Exception Handling
The program includes basic error handling for scenarios such as insufficient balance, insufficient stock quantity, and invalid user actions.
