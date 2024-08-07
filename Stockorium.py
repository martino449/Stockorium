import random
import pickle
import os
from cryptography.fernet import Fernet

# Genera una chiave segreta per la crittografia
def generate_key():
    return Fernet.generate_key()

# Carica la chiave segreta
def load_key():
    if os.path.exists('secret.key'):
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key

# Funzioni per la crittografia e decriptazione
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)

# Funzioni per la persistenza dei dati
def save_data(users, key):
    with open('users_data.pkl', 'wb') as f:
        encrypted_data = encrypt_data(pickle.dumps(users), key)
        f.write(encrypted_data)

def load_data(key):
    try:
        with open('users_data.pkl', 'rb') as f:
            encrypted_data = f.read()
            data = decrypt_data(encrypted_data, key)
            return pickle.loads(data)
    except FileNotFoundError:
        return {}

def save_portfolio(username, portfolio, key):
    with open(f'{username}_portfolio.pkl', 'wb') as f:
        encrypted_data = encrypt_data(pickle.dumps(portfolio), key)
        f.write(encrypted_data)

def load_portfolio(username, key):
    try:
        with open(f'{username}_portfolio.pkl', 'rb') as f:
            encrypted_data = f.read()
            data = decrypt_data(encrypted_data, key)
            return pickle.loads(data)
    except FileNotFoundError:
        return Portfolio()

def save_market(market, key):
    with open('market_data.pkl', 'wb') as f:
        encrypted_data = encrypt_data(pickle.dumps(market), key)
        f.write(encrypted_data)

def load_market(key):
    try:
        with open('market_data.pkl', 'rb') as f:
            encrypted_data = f.read()
            data = decrypt_data(encrypted_data, key)
            return pickle.loads(data)
    except FileNotFoundError:
        return Market()

class Stock:
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.history = [price]

    def update_price(self):
        # Simula la variazione del prezzo basata su una distribuzione normale
        self.price += random.gauss(0, 1) * (self.price * 0.01)
        self.price = max(0, self.price)
        self.history.append(self.price)

    def __str__(self):
        return f"{self.symbol}: ${self.price:.2f} (Disponibile: {self.quantity} azioni)"

class Portfolio:
    def __init__(self):
        self.stocks = {}
        self.balance = 10000
        self.transaction_fee = 10.0  # Commissione fissa per transazione

    def buy_stock(self, stock, quantity):
        cost = stock.price * quantity
        total_cost = cost + self.transaction_fee
        if total_cost > self.balance:
            print("Saldo insufficiente per acquistare l'azione.")
            return False
        if quantity > stock.quantity:
            print(f"Non ci sono abbastanza azioni disponibili per {stock.symbol}.")
            return False
        else:
            if stock.symbol in self.stocks:
                self.stocks[stock.symbol] += quantity
            else:
                self.stocks[stock.symbol] = quantity
            stock.quantity -= quantity
            self.balance -= total_cost
            print(f"Acquistati {quantity} di {stock.symbol}. Commissione applicata: ${self.transaction_fee:.2f}.")
            return True

    def sell_stock(self, stock, quantity):
        if stock.symbol not in self.stocks or self.stocks[stock.symbol] < quantity:
            print("Non hai abbastanza azioni per vendere.")
            return False
        else:
            self.stocks[stock.symbol] -= quantity
            earnings = stock.price * quantity - self.transaction_fee
            self.balance += earnings
            stock.quantity += quantity
            print(f"Venduti {quantity} di {stock.symbol}. Commissione applicata: ${self.transaction_fee:.2f}.")
            return True

    def get_portfolio_value(self, market):
        total_value = self.balance
        for symbol, quantity in self.stocks.items():
            stock = market.get_stock(symbol)
            if stock:
                total_value += stock.price * quantity
        return total_value

    def __str__(self):
        portfolio_str = "Portafoglio:\n"
        for symbol, quantity in self.stocks.items():
            portfolio_str += f"{symbol}: {quantity} azioni\n"
        portfolio_str += f"Saldo disponibile: ${self.balance:.2f}\n"
        portfolio_str += f"Commissione per transazione: ${self.transaction_fee:.2f}"
        return portfolio_str

class Market:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, price, quantity):
        if symbol in self.stocks:
            print("Azione già esistente nel mercato.")
        else:
            self.stocks[symbol] = Stock(symbol, price, quantity)
            print(f"Azione {symbol} aggiunta al mercato con {quantity} azioni disponibili.")

    def get_stock(self, symbol):
        return self.stocks.get(symbol, None)

    def update_market(self):
        for stock in self.stocks.values():
            stock.update_price()

    def __str__(self):
        market_str = "Mercato:\n"
        for stock in self.stocks.values():
            market_str += str(stock) + "\n"
        return market_str

    def __getstate__(self):
        state = self.__dict__.copy()
        # Convert Stock objects to a serializable format
        state['stocks'] = {symbol: (stock.symbol, stock.price, stock.quantity, stock.history) for symbol, stock in self.stocks.items()}
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Convert the serializable format back to Stock objects
        self.stocks = {symbol: Stock(symbol, price, quantity) for symbol, (symbol, price, quantity, history) in self.stocks.items()}
        for stock in self.stocks.values():
            stock.history = history

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.portfolio = load_portfolio(username, key)

class UserManager:
    def __init__(self, key):
        self.users = load_data(key)
        self.key = key

    def register(self, username, password):
        if username in self.users:
            print("Nome utente già esistente.")
        else:
            self.users[username] = User(username, password)
            save_data(self.users, self.key)
            print("Registrazione avvenuta con successo.")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        else:
            print("Nome utente o password errati.")
            return None

def display_market(market):
    print("\n--- Mercato ---")
    print(market)

def main():
    global key
    key = load_key()
    market = load_market(key)
    user_manager = UserManager(key)

    while True:
        print("\n--- Menu Principale ---")
        print("1. Visualizza mercato")
        print("2. Registrati")
        print("3. Accedi")
        print("4. Esci")
        choice = input("Scegli un'opzione: ")

        if choice == '1':
            display_market(market)

        elif choice == '2':
            username = input("Nome utente: ")
            password = input("Password: ")
            user_manager.register(username, password)

        elif choice == '3':
            username = input("Nome utente: ")
            password = input("Password: ")
            current_user = user_manager.login(username, password)

            if current_user:
                while True:
                    print("\n--- Menu Utente ---")
                    print("1. Visualizza portafoglio")
                    print("2. Acquista azioni")
                    print("3. Vendi azioni")
                    print("4. Aggiungi azione al mercato")
                    print("5. Aggiorna mercato")
                    print("6. Mostra commissione di transazione")
                    print("7. Logout")
                    user_choice = input("Scegli un'opzione: ")

                    if user_choice == '1':
                        print("\nStato del portafoglio:")
                        print(current_user.portfolio)

                    elif user_choice == '2':
                        symbol = input("Simbolo azione: ")
                        quantity = int(input("Quantità: "))
                        stock = market.get_stock(symbol)
                        if stock:
                            if current_user.portfolio.buy_stock(stock, quantity):
                                market.update_market()
                                save_portfolio(current_user.username, current_user.portfolio, key)
                                save_market(market, key)
                        else:
                            print("Azione non trovata.")

                    elif user_choice == '3':
                        symbol = input("Simbolo azione: ")
                        quantity = int(input("Quantità: "))
                        stock = market.get_stock(symbol)
                        if stock:
                            if current_user.portfolio.sell_stock(stock, quantity):
                                market.update_market()
                                save_portfolio(current_user.username, current_user.portfolio, key)
                                save_market(market, key)
                        else:
                            print("Azione non trovata.")

                    elif user_choice == '4':
                        symbol = input("Simbolo azione: ")
                        price = float(input("Prezzo iniziale: "))
                        quantity = int(input("Quantità iniziale: "))
                        market.add_stock(symbol, price, quantity)
                        save_market(market, key)

                    elif user_choice == '5':
                        market.update_market()
                        print("\nMercato aggiornato:")
                        display_market(market)
                        save_market(market, key)

                    elif user_choice == '6':
                        print(f"\nCommissione per transazione: ${current_user.portfolio.transaction_fee:.2f}")

                    elif user_choice == '7':
                        break

                    else:
                        print("Opzione non valida.")

        elif choice == '4':
            break

        else:
            print("Opzione non valida.")

if __name__ == "__main__":
    main()
