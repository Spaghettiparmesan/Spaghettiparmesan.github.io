import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from functions import apology, login_required, get_average_data, save_consumption_chart, get_chart_data

from datetime import datetime, date
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///data.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Overview"""
    if request.method == 'POST':
        date = datetime.now()
        quantity = float(request.form['gas_quantity'])
        expenses = float(request.form['expenses'])
        price = round((expenses / quantity),2)
        reach = float(request.form['reach'])
        consumption = round((100 * int(quantity) / int(reach)),2)
        event = db.execute("INSERT INTO history (userid, date, quantity, expenses, price, reach, consumption) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], date, quantity, expenses, price, reach, consumption)
        return redirect("/history")
    else:
        return render_template("index.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE userid=?", session["user_id"])
    print(history)
    print(session["user_id"])
    return render_template("history.html", history=history)


@app.route('/analytics')
def analytics():
    user_id = session.get("user_id")
    if user_id is None:
        # Handle the case where the user is not logged in
        return redirect("/login")

    history = db.execute("SELECT * FROM history WHERE userid=?", session["user_id"])
    average_data = get_average_data(history)
    dates = list(range(1,len(history)+1))

    return render_template('analytics.html', average_data=average_data, history=history, dates=dates)


@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit(event_id):
    # Retrieve the existing data for the specified event_id
    event = db.execute("SELECT * FROM history WHERE id = ?", event_id)#.fetchone()
    print(event)
    if request.method == "POST":
        # Update the data with the submitted values
        new_date = request.form.get("new_date")
        new_quantity = float(request.form.get("new_quantity"))
        new_expenses = float(request.form.get("new_expenses"))
        new_reach = float(request.form.get("new_reach"))
        new_price = round((new_expenses / new_quantity),2)
        new_consumption = round((100 * int(new_quantity) / int(new_reach)),2)

        db.execute("UPDATE history SET date=?, quantity=?, expenses=?, reach=?, price=?, consumption=? WHERE id=?", new_date, new_quantity, new_expenses, new_reach, new_price, new_consumption, event_id)

        # Redirect to the history page after editing
        return redirect("/history")

    return render_template("edit.html", event=event[0])

@app.route('/tips')
def tips():
    return render_template('tips.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    #Register user
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        pw = request.form.get("password")
        pwcheck = request.form.get("confirmation")
        usercheck = db.execute("SELECT * FROM users where username=?", username)

        if len(username) < 1:
            return apology("Please enter a username")
        elif len(usercheck) > 0:
            return apology("This username already exists")
        elif len(pw) < 1:
            return apology("You need to enter a password")
        elif pw != pwcheck:
            return apology("You have to enter the same password twice")
        else:
            insertion = db.execute(
                "INSERT INTO users (username,hash) VALUES (?, ?)",
                username,
                generate_password_hash(pw, method="pbkdf2:sha1", salt_length=8),
            )
            check = db.execute("SELECT * FROM users WHERE username=?", username)
            session["user_id"] = check[0]["id"]
            return redirect("/")
