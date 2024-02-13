import csv
import requests

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']

with open('currency_rates.csv', 'w', newline='', encoding='utf-8') as csvfile:
      fieldnames = ['currency', 'code', 'bid', 'ask']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

      writer.writeheader()
      for rate in rates:
          writer.writerow(rate)
from flask import Flask, render_template, request

app = Flask(__name__)

def read_currency_rates():
      with open('currency_rates.csv', newline='', encoding='utf-8') as csvfile:
          reader = csv.DictReader(csvfile, delimiter=';')
          currency_rates = [row for row in reader]
      return currency_rates

@app.route('/', methods=['GET', 'POST'])
def index():
      currency_rates = read_currency_rates()
      if request.method == 'POST':
          selected_currency = request.form['currency']
          amount = float(request.form['amount'])
          for rate in currency_rates:
              if rate['code'] == selected_currency:
                  cost_in_pln = amount * float(rate['ask'])
                  return f'Koszt {amount} {selected_currency} w PLN: {cost_in_pln:.2f} PLN'
      return render_template('form.html', currency_rates=currency_rates)

if __name__ == '__main__':
      app.run(debug=True)
