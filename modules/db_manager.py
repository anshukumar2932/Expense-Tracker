import sqlite3

DATABASE = 'database\\expense_tracker.db'

def init_users_db():
    """Initialize the users database and create the users table if it doesn't exist."""
    try:
        with get_db() as conn:
            conn.execute(''' 
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()
    except Exception as e:
        message = f"Error initializing the users database: {e}"
        print(message)
        return message

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def get_user_by_userid(user_id):
    """Fetch user data from the database by username."""
    try:
        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE username = ?", (user_id,))
            user_data = cursor.fetchone()
            return user_data
    except Exception as e:
        message = f"Error fetching user: {e}"
        print(message)
        return message

def create_user(username, password):
    """Insert a user and initialize their expenses."""
    try:
        with get_db() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

            # Create a new table for expenses if it doesn't exist
            table_name = f"expenses_{username}"  
            conn.execute(f''' 
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Date DATE NOT NULL,
                    Category TEXT NOT NULL,
                    Particular TEXT NOT NULL,
                    Amount DECIMAL NOT NULL
                )
            ''')
            conn.commit()
    except Exception as e:
        message = f"Error initializing the expense database: {e}"
        print(message)
        return message

def update_password(username, hashed_password):
    """Update user's password in the database."""
    try:
        with get_db() as conn:
            conn.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
    except Exception as e:
        message = f"Error updating password: {e}"
        print(message)
        return message

def enter_expense(username, Date, Category, Particular, Amount):
    """Insert a new expense for a specific user."""
    try:
        with get_db() as conn:
            table_name = f"expenses_{username}" 
            conn.execute(f'''
                INSERT INTO {table_name} (Date, Category, Particular, Amount)
                VALUES (?, ?, ?, ?)
            ''', (Date, Category, Particular, Amount))
            conn.commit()
            print(f"Expense added successfully for {username}.")
            return True
    except Exception as e:
        message = f"Error adding expense for {username}: {e}"
        print(message)
        return message

def show_expense(username):
    """Fetch all rows for a user's expenses."""
    try:
        with get_db() as conn:
            table = f"expenses_{username}"  # Fixed table name
            cursor = conn.execute(f'''
                SELECT * FROM {table}
            ''')
            rows = cursor.fetchall()
            
            # Check if rows exist
            if rows:
                return [dict(row) for row in rows]  # Return a list of dictionaries
            else:
                print(f"No expenses found for {username}.")
                return []  # Return an empty list if no rows found
    except Exception as e:
        print(f"Error fetching expenses for {username}: {e}")
        return []  # Return an empty list in case of an error

            
    except Exception as e:
        message = f"Error in showing expense for {username}: {e}"
        print(message)
        return message

def delete_user_expense(username, e_id):
    """Delete an expense from a specific user's table."""
    try:
        e_id = int(e_id)  # Ensure e_id is an integer
        table_name = f"expenses_{username}"  # Dynamically set the table name
        with get_db() as conn:
            conn.execute(f'''
                DELETE FROM {table_name} WHERE id = ?
            ''', (e_id,))  # Pass the correct variable
            conn.commit()
            print(f"Expense with ID {e_id} deleted successfully for {username}.")
            return True
    except Exception as e:
        message = f"Error deleting expense for {username}: {e}"
        print(message)
        return False  # Return False instead of an error message string

