from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from modules.db_manager import init_users_db, get_user_by_userid, create_user, update_password,enter_expense,show_expense
from datetime import timedelta

# Initialize database
init_users_db()

# Flask app configuration
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Use environment variables for production
app.permanent_session_lifetime = timedelta(minutes=3)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Temporary state for password reset
reset_session = {}

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_userid(user_id)
    return User(user_data['username']) if user_data else None


@app.before_request
def redirect_authenticated_user():
    """Redirect authenticated users away from login or signup pages."""
    if current_user.is_authenticated and request.endpoint in ['login', 'signup']:
        return redirect(url_for('protected', username=current_user.id))


@app.route('/')
def home():
    """Redirect to login or protected page based on authentication status."""
    logout_user()  # Logs out the user
    session.clear()
    if current_user.is_authenticated:
        return redirect(url_for('protected', username=current_user.id))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    session.clear()  # Ensure clean session
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        user_data = get_user_by_userid(username)
        if user_data and check_password_hash(user_data['password'], password):
            session['user'] = username
            session.permanent = True
            login_user(User(username))
            return redirect(url_for('protected', username=username))

        flash("Invalid username or password")
    return render_template('login_signup.html', mode="login")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        if get_user_by_userid(username):
            flash("User already exists")
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            create_user(username, hashed_password)
            flash("Signup successful. Please log in.")
            return redirect(url_for('login'))

    return render_template('login_signup.html', mode="signup")


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle password reset."""
    email_form = True

    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')

        if username and not new_password:
            user = get_user_by_userid(username)
            if not user:
                flash("User does not exist")
                return redirect(url_for('forgot_password'))

            reset_session['user'] = username
            email_form = False
            return render_template('forgot_password.html', email_form=email_form)

        if reset_session.get('user') and new_password:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            update_password(reset_session['user'], hashed_password)
            flash("Password updated successfully!")
            reset_session.clear()
            return redirect(url_for('login'))

        flash("An error occurred. Please try again.")
    return render_template('forgot_password.html', email_form=email_form)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Log out the current user."""
    logout_user()  # Logs out the user
    session.clear()  # Clears the session
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/protected/<username>', methods=['GET'])
@login_required
def protected(username):
    """Protected route accessible only to authenticated users."""
    return render_template('index.html', username=current_user.id)

@app.route("/protected/add_expense", methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        Date = request.form.get('Date')
        Category = request.form.get('Category')
        Particular = request.form.get('Particular')
        Amount = request.form.get('Amount')

        try:
            if request.form.get('username') == current_user.id:
                if enter_expense(current_user.id, Date, Category, Particular, Amount):
                    flash("Successfully added data")
                else:
                    flash("An error occurred adding expense.") 
            else:
                flash("Invalid Username")
        except Exception as e:
            # Log the error for debugging
            app.logger.error(f"Error adding expense: {e}") 
            flash("An unexpected error occurred. Please try again later.") 

    return render_template('index.html', username=current_user.id, mode="Add")

@app.route("/view_expense")
@login_required
def view_expense():
    return render_template('index.html', username=current_user.id, mode="View",credentials=show_expense(current_user.id))

if __name__ == "__main__":
    app.run(debug=True)
