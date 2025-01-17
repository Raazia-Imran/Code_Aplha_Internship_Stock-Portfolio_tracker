import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import json
import os
import matplotlib.pyplot as plt

# Placeholder function for real stock data fetching
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period="1d")
        if not stock_info.empty:
            data = {
                "currentPrice": stock_info["Close"].iloc[0],
                "companyName": stock.info["longName"],
                "sector": stock.info.get("sector", "N/A"),
                "industry": stock.info.get("industry", "N/A"),
                "exchange": stock.info.get("exchange", "N/A"),
                "52_week_high": stock.info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": stock.info.get("fiftyTwoWeekLow", "N/A"),
                "market_cap": stock.info.get("marketCap", "N/A"),
                "dividend_yield": stock.info.get("dividendYield", "N/A"),
                "PE_ratio": stock.info.get("trailingPE", "N/A")
            }
            return data
        else:
            raise ValueError("No stock data found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {ticker}: {e}")
        return None

# Functions for portfolio management
def add_stock(portfolio, ticker, shares):
    try:
        shares = float(shares)
        if ticker in portfolio:
            portfolio[ticker]["shares"] += shares
        else:
            stock_data = get_stock_data(ticker)
            if stock_data:
                portfolio[ticker] = {
                    "ticker": ticker,
                    "company_name": stock_data["companyName"],
                    "sector": stock_data["sector"],
                    "industry": stock_data["industry"],
                    "exchange": stock_data["exchange"],
                    "shares": shares,
                    "price": stock_data["currentPrice"],
                    "value": shares * stock_data["currentPrice"],
                    "52_week_high": stock_data["52_week_high"],
                    "52_week_low": stock_data["52_week_low"],
                    "market_cap": stock_data["market_cap"],
                    "dividend_yield": stock_data["dividend_yield"],
                    "PE_ratio": stock_data["PE_ratio"]
                }
        update_table()
    except ValueError:
        messagebox.showerror("Error", "Shares must be a numeric value.")

def remove_stock(portfolio, ticker):
    if ticker in portfolio:
        del portfolio[ticker]
        update_table()
    else:
        messagebox.showerror("Error", f"Stock '{ticker}' not found in portfolio.")

def update_portfolio():
    for ticker, stock in portfolio.items():
        stock_data = get_stock_data(ticker)
        if stock_data:
            stock["price"] = stock_data["currentPrice"]
            stock["value"] = stock["shares"] * stock["price"]
    update_table()

def save_portfolio_to_file():
    with open("portfolio.json", "w") as file:
        json.dump(portfolio, file)
    messagebox.showinfo("Saved", "Portfolio saved to 'portfolio.json'.")

def load_portfolio_from_file():
    global portfolio
    if os.path.exists("portfolio.json"):
        with open("portfolio.json", "r") as file:
            portfolio = json.load(file)
        update_table()

# GUI Functions
def update_table():
    for row in portfolio_table.get_children():
        portfolio_table.delete(row)
    for stock in portfolio.values():
        profit_loss = stock["value"] - (stock["shares"] * 100)  # Assuming initial price is 100
        portfolio_table.insert("", "end", values=(
            stock["ticker"], stock["company_name"], stock["sector"], stock["shares"], f"${stock['price']:.2f}",
            f"${stock['value']:.2f}", f"${profit_loss:.2f}"
        ))
        # Alternate row colors
        for index, item in enumerate(portfolio_table.get_children()):
            if index % 2 == 0:
                portfolio_table.item(item, tags="even")
            else:
                portfolio_table.item(item, tags="odd")
        portfolio_table.tag_configure("even", background="#f0f0f0")
        portfolio_table.tag_configure("odd", background="#ffffff")

def add_stock_gui():
    ticker = ticker_entry.get().upper()
    shares = shares_entry.get()
    if ticker:
        add_stock(portfolio, ticker, shares)
    else:
        messagebox.showerror("Error", "Please enter a valid stock ticker.")

def remove_stock_gui():
    ticker = ticker_entry.get().upper()
    if ticker:
        remove_stock(portfolio, ticker)
    else:
        messagebox.showerror("Error", "Please enter a valid stock ticker.")

# Function to show "How it Works"
def how_it_works():
    how_it_works_message = (
        "How it Works:\n\n"
        "1. Add Stock: Enter the ticker symbol of a company (e.g., AAPL for Apple) and the number of shares you own. Click 'Add Stock'.\n"
        "2. Remove Stock: Enter the ticker symbol of a company you wish to remove from your portfolio. Click 'Remove Stock'.\n"
        "3. Update Portfolio: Updates the stock prices and portfolio value.\n"
        "4. Save Portfolio: Save your portfolio data to a JSON file for future reference.\n"
        "5. View Allocation: View a pie chart of the portfolio allocation based on stock values.\n\n"
        "Sample Companies and Ticker Symbols:\n"
        "1. Apple Inc. - AAPL\n"
        "2. Microsoft Corp. - MSFT\n"
        "3. Tesla Inc. - TSLA\n"
        "4. Amazon.com - AMZN\n"
        "5. Google (Alphabet) - GOOGL\n"
        "6. Meta Platforms - META\n"
        "7. NVIDIA - NVDA\n"
        "8. Coca-Cola - KO\n"
        "9. Walmart - WMT\n"
        "10. Home Depot - HD"
    )
    messagebox.showinfo("How it Works", how_it_works_message)

# Function to view allocation pie chart
def view_allocation():
    if portfolio:
        labels = []
        sizes = []
        for stock in portfolio.values():
            labels.append(stock["company_name"])
            sizes.append(stock["value"])

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Portfolio Allocation')
        plt.axis('equal')
        plt.show()
    else:
        messagebox.showerror("Error", "Portfolio is empty. Please add some stocks first.")

# Initialize Portfolio
portfolio = {}

# GUI Setup
root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.geometry("900x600")
root.configure(bg="#2c3e50")

# Widgets with a modern style
frame = tk.Frame(root, bg="#34495e")
frame.pack(pady=20)

tk.Label(frame, text="Stock Ticker:", fg="white", bg="#34495e", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
ticker_entry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="sunken")
ticker_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Shares:", fg="white", bg="#34495e", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
shares_entry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="sunken")
shares_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Stock", command=add_stock_gui, bg="#27ae60", fg="white", font=("Arial", 12), relief="raised")
add_button.grid(row=2, column=0, pady=10)

remove_button = tk.Button(frame, text="Remove Stock", command=remove_stock_gui, bg="#e74c3c", fg="white", font=("Arial", 12), relief="raised")
remove_button.grid(row=2, column=1, pady=10)

update_button = tk.Button(frame, text="Update Portfolio", command=update_portfolio, bg="#f39c12", fg="white", font=("Arial", 12), relief="raised")
update_button.grid(row=2, column=2, pady=10)

save_button = tk.Button(frame, text="Save Portfolio", command=save_portfolio_to_file, bg="#3498db", fg="white", font=("Arial", 12), relief="raised")
save_button.grid(row=2, column=3, pady=10)

# How it works button
how_it_works_button = tk.Button(frame, text="How it Works", command=how_it_works, bg="#9b59b6", fg="white", font=("Arial", 12), relief="raised")
how_it_works_button.grid(row=3, column=0, pady=10)

# View Allocation button
view_allocation_button = tk.Button(frame, text="View Allocation", command=view_allocation, bg="#16a085", fg="white", font=("Arial", 12), relief="raised")
view_allocation_button.grid(row=3, column=1, pady=10)

# Treeview Table
columns = ("Ticker", "Company Name", "Sector", "Shares", "Current Price", "Value", "Profit/Loss")
portfolio_table = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    portfolio_table.heading(col, text=col)
    portfolio_table.column(col, width=120)

portfolio_table.pack(pady=20)

# Load portfolio from file if it exists
load_portfolio_from_file()

# Run the GUI
root.mainloop()

