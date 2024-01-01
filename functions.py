from flask import redirect, render_template, session
from functools import wraps
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_average_data(history):
    if not history:
        return None

    dates = []
    quantities = []
    expenses = []
    total_expenses = 0
    prices = []
    reach = []
    consumption = []

    for entry in history:
        print(history)
        print("\n\n\n\n")
        print(entry)
        dates.append(entry["date"])
        quantities.append(entry["quantity"])
        expenses.append(entry["expenses"])
        total_expenses += entry["expenses"]
        prices.append(entry["price"])
        reach.append(entry["reach"])
        consumption.append(entry["consumption"])

    average_quantity = np.mean(quantities)
    average_expenses = np.mean(expenses)
    average_price = np.mean(prices)
    average_reach = np.mean(reach)
    average_consumption = np.mean(consumption)

    return {
        'average_quantity': round(average_quantity, 2),
        'average_expenses': round(average_expenses, 2),
        'average_price': round(average_price, 2),
        'average_reach': round(average_reach, 2),
        'average_consumption': round(average_consumption, 2),
        'dates': dates,
        'quantities': quantities,
        'prices' : prices,
        'reach' : reach,
        'consumption' : consumption,
        'total_expenses': total_expenses,
    }

def save_consumption_chart(history):
    if not history:
        return

    dates = [entry["date"] for entry in history]
    quantities = [entry["quantity"] for entry in history]

    plt.plot(dates, quantities, marker='o', linestyle='-')
    plt.title('Gas Consumption Over Time')
    plt.xlabel('Date')
    plt.ylabel('Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/consumption_chart.png')
    plt.close()

def get_chart_data(history):
    if not history:
        return None

    dates = [entry["date"] for entry in history]
    quantities = [entry["quantity"] for entry in history]

    chart_data = {
        'dates': dates,
        'quantities': quantities,
    }

    return chart_data
