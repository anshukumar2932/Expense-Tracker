# Expense Tracker

A simple Python-based expense tracker application that allows users to manage their expenses efficiently. The application uses SQLite for data storage and provides features such as adding, updating, deleting, and viewing expenses, as well as generating reports and visualizations.

## Features

- Add, update, and delete expenses.
- Categorize expenses (e.g., Food, Rent, Utilities).
- View expenses filtered by date, category, or amount.
- Generate reports by category, month, or year.
- Export expenses to a CSV file.
- Visualize expenses with graphs.

## Project Structure

```
expense_tracker/
├── main.py                  # Entry point of the application
├── database/
│   └── expense_tracker.db   # SQLite database
├── modules/
│   ├── db_manager.py        # Handles database connections and queries
│   ├── expense_manager.py   # CRUD operations for expenses
│   └── report_generator.py  # Generates reports and visualizations
├── test.py        # Test cases for the application
├── README.md                # Documentation
├── requirements.txt         # Python dependencies
└── .gitignore               # Files ignored by Git
```

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/expense-tracker.git
   cd expense-tracker
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Mac/Linux
   venv\Scripts\activate      # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

- Run the application using `python app.py`.
- Follow the on-screen menu to perform actions:
  - Add an expense.
  - View all expenses.
  - Update or delete an expense.
  - Generate reports and export data.