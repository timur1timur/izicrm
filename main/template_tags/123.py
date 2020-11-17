import requests

def get_currency():
    res = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = res.json()['Valute']['USD']['Value']
    eur = res.json()['Valute']['EUR']['Value']
    f = f'USD: {round(usd,2)} руб  EUR: {round(eur,2)} руб'
    return f

f = get_currency()
print(f)