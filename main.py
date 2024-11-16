import sqlite3
con=sqlite3.connect("expense_tracker.db")
if con:
    print("Connected Successfully")
