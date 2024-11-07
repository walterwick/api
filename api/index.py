

from flask import Flask, render_template_string
from binance.client import Client

app = Flask(__name__)

# API anahtarlarınızı buraya girin

@app.route('/')
def index():
    total_value_in_usd = 0.0
    balances = []

    # Binance istemcisini oluşturun
    client = Client(api_key, api_secret)

    # Hesap bilgilerini alın
    account_info = client.get_account()

    for balance in account_info['balances']:
        asset = balance['asset']
        free_balance = float(balance['free'])
        
        if free_balance > 0:
            # Her bir kripto paranın USD cinsinden fiyatını alın
            try:
                if asset != 'USDT':
                    price = client.get_symbol_ticker(symbol=f"{asset}USDT")['price']
                    value_in_usd = free_balance * float(price)
                else:
                    value_in_usd = free_balance  # USDT cinsinden zaten
            except Exception as e:
                print(f"{asset} için fiyat alınamadı: {e}")
                continue
            
            balances.append({
                'coin': asset,
                'balance': free_balance,
                'value_in_usd': value_in_usd
            })
            total_value_in_usd += value_in_usd

    # HTML içeriği
    html_content = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Binance Bakiye Kontrol</title>
    </head>
    <body>
        <h1>Binance Bakiye Kontrol</h1>
        <form method="POST">
            <input type="submit" value="Bakiye Kontrol Et">
        </form>

        {% if balances %}
            <h2>Bakiye Bilgileri</h2>
            <table border="1">
                <tr>
                    <th>Coin</th>
                    <th>Bakiye</th>
                    <th>Değer (USD)</th>
                </tr>
                {% for balance in balances %}
                <tr>
                    <td>{{ balance.coin }}</td>
                    <td>{{ balance.balance }}</td>
                    <td>{{ balance.value_in_usd }}</td>
                </tr>
                {% endfor %}
            </table>
            <h3>Toplam Değer (USD): {{ total_value_in_usd }}</h3>
        {% endif %}
    </body>
    </html>
    '''

    return render_template_string(html_content, balances=balances, total_value_in_usd=total_value_in_usd)

if __name__ == '__main__':
    app.run(debug=True)
