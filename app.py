from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)
FILE_NAME = "expenses.csv"

def init_file():
    try:
        with open(FILE_NAME, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

@app.route("/")
def index():
    expenses = []
    with open(FILE_NAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        description = request.form["description"]
        date = datetime.now().strftime("%Y-%m-%d")

        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, amount, description])

        return redirect(url_for("index"))
    return render_template("add.html")

if __name__ == "__main__":
    init_file()
    app.run(debug=True)
