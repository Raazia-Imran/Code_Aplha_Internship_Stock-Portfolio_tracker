# Stock Portfolio Tracker

This is a Python-based stock portfolio tracker that allows users to track their investments, view portfolio allocation, and manage stock information.


## Features

- Add and remove stocks from your portfolio.
- View your portfolio with current stock prices, value, and profit/loss.
- Save and load your portfolio data to/from a JSON file.
- View portfolio allocation with a pie chart.
- Learn how the app works with an easy-to-use interface.

##Requirements:
- Python 3.x
- yfinance (for fetching live stock data)
- matplotlib (for visualizing portfolio allocation)
- tkinter (for GUI)

## How to Use

1. **Add Stock**: Enter the ticker symbol and the number of shares.
2. **Remove Stock**: Enter the ticker symbol of the stock you want to remove.
3. **Update Portfolio**: Fetch the latest stock prices and update your portfolio.
4. **Save Portfolio**: Save your portfolio to a JSON file.
5. **View Allocation**: View a pie chart of your portfolio allocation.

## How to Contribute

1. Fork the repository.
2. Create your branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

##Necessary Imports:

- import tkinter as tk
- from tkinter import ttk, messagebox
- import yfinance as yf
- import json
- import os
- import matplotlib.pyplot as plt


## License

This project is licensed under the MIT License
