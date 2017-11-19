from main import app, PageData
from flask import render_template, request, redirect, url_for, session, flash
import actions as act
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please Log In")
            return redirect(url_for('index'))

    return wrap


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if act.login(username, password):
            return redirect(url_for('dashboard'))
        flash("Invalid Login", category="danger")
    else:
        flash("Invalid Action", category="danger")
    return redirect(url_for('index'))


@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            if act.register(username, password):
                flash("Welcome {}, to your Personal Finance Assistant!".format(username), category="success")
                return redirect(url_for('dashboard'))
            else:
                flash("User Account already exists", category="danger")
                return redirect(url_for('index'))
        except Exception as e:
            flash("An error occurred: {}".format(str(e)), category="danger")
    else:
        flash("Invalid Action", category="danger")
    return redirect(url_for("index"))


@app.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
    return render_template('dashboard.html', page=PageData('dashboard', 'Dashboard'))

'''
@app.route('/debts', methods=["GET"])
@login_required
def dashboard():
    return render_template('debts.html', page=PageData('debts', 'Debts'))


@app.route('/expenses', methods=["GET"])
@login_required
def dashboard():
    return render_template('expenses.html', page=PageData('expenses', 'Expenses'))


@app.route('/stats', methods=["GET"])
@login_required
def dashboard():
    return render_template('stats.html', page=PageData('stats', 'Stats'))

'''
'''
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in.")
            return redirect(url_for('login_page'))

    return wrap
'''
'''
@app.route("login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if login(username, password):
            return redirect(url_for("dashboard_page"))
        else:
            flash("Invalid login credentials")
            return redirect(url_for("login_page"))
    else:
        if 'logged_in' in session:
            flash("You are already logged in")
            return redirect(url_for("dashboard_page"))
        page = PageData("login", "Login", "Register your details")
        return render_template("BlogOn/login.html", page=page)

'''
