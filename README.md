# Retail Inventory Management System

## Overview
This is my project for the Flipped Course. I created a system to manage a retail shop's inventory. 
It has two parts:
1. **Desktop App (Tkinter):** Used by the shopkeeper to add, delete, and manage items.
2. **Web Dashboard (Streamlit):** Used to see graphs and analyze the stock.

Both apps share the same database (`store_data.db`), so if you add an item in the desktop app, it shows up on the website immediately.

## Problems Solved
* Manual record-keeping is slow and error-prone.
* Shop owners need to know their total stock value quickly.
* Visualizing data helps in deciding what to buy next.

## How to Run the Project

### Prerequisites
You need Python installed. You also need to install these libraries:
`pip install streamlit pandas plotly`
*(Note: Tkinter and sqlite3 come pre-installed with Python)*

### Step 1: Add Data
Run the desktop application first to create the database and add items.
`python manager_gui.py`

### Step 2: View Dashboard
Run the analytics dashboard to see the charts.
`streamlit run dashboard.py`

## Project Structure
* `manager_gui.py`: The main GUI code for data entry.
* `dashboard.py`: The web-based visualization tool.
* `db_helper.py`: Contains all the SQL commands to keep the main code clean.
* `store_data.db`: The database file (created automatically).