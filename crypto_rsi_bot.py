# crypto_rsi_bot.py

import requests
import pandas as pd
import pandas_ta as ta
import time

# Add near the top of your script
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjkLMNopQRstUVwxyz"
TELEGRAM_CHAT_ID = "987654321"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")


# STEP 1: Get top 10 coins by market cap from CoinGecko
def get_top_coins(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1
    }
    response = requests.get(url, params=params)
    return [coin["id"] for coin in response.json()]

# STEP 2: Fetch hourly historical prices
def get_hourly_prices(coin_id, hours=24):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 1,
        "interval": "hourly"
    }
    response = requests.get(url, params=params)
    prices = response.json()["prices"]
    close_prices = [price[1] for price in prices]
    return close_prices

# STEP 3: Compute RSI using pandas-ta
def compute_rsi(close_prices, length=14):
    df = pd.DataFrame(close_prices, columns=["close"])
    rsi_series = ta.rsi(df["close"], length=length)
    return rsi_series.iloc[-1]  # return latest RSI value

# STEP 4: Check RSI and print signal
def check_rsi_signal(coin_id):
    try:
        prices = get_hourly_prices(coin_id)
        rsi = compute_rsi(prices)
        print(f"{coin_id.upper()} - RSI: {rsi:.2f}")
        if rsi < 30:
            print(f"💹 BUY SIGNAL for {coin_id.upper()}! RSI = {rsi:.2f}")
    except Exception as e:
        print(f"Error checking {coin_id}: {e}")

# STEP 5: Main loop
def run_bot():
    print("Fetching RSI values...")
    top_coins = get_top_coins()
    for coin in top_coins:
        check_rsi_signal(coin)

if __name__ == "__main__":
    run_bot()
