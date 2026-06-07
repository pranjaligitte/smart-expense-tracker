from flask import Flask, render_template, request, redirect
import csv
import pandas as pd
import matplotlib
from sklearn.linear_model import LinearRegression
import numpy as np

matplotlib.use('Agg')

import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']

        with open('expenses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, amount, category])

        print("Amount:", amount)
        print("Category:", category)

    df = pd.read_csv('expenses.csv')

    category_data = df.groupby('Category')['Amount'].sum()

    plt.figure(figsize=(5, 5))

    plt.pie(
        category_data,
        labels=category_data.index,
        autopct='%1.1f%%'
    )

    plt.title('Expenses by Category')

    plt.savefig('static/chart.png')

    plt.close()

    total = df['Amount'].sum()

    budget = 5000
    remaining = budget - total

    months = np.array(range(len(df))).reshape(-1, 1)

    expenses = df['Amount'].values

    prediction = 0

    if len(df) >= 2:

        model = LinearRegression()

        model.fit(months, expenses)

        prediction = int(
            model.predict([[len(df)]])[0]
        )

    return render_template(
        'index.html',
        expenses=df.to_dict('records'),
        total=total,
        budget=budget,
        remaining=remaining,
        prediction=prediction
    )

@app.route('/delete/<int:index>')
def delete(index):

    df = pd.read_csv('expenses.csv')

    df = df.drop(index)

    df.to_csv('expenses.csv', index=False)

    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)