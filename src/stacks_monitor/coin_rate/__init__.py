from datetime import datetime, timedelta

import requests
import time


def get_historical_rate(coin_id: str, vs_currency: str, date: datetime) -> float:
    from_ts = int((date - timedelta(hours=2)).timestamp())
    to_ts = int(date.timestamp())

    url = "https://api.coingecko.com/api/v3/coins/{}/market_chart/range?vs_currency={}&from={}&to={}" \
        .format(coin_id, vs_currency, from_ts, to_ts)

    resp = requests.get(url)

    # wait some and try again when rate limit exceeds
    if resp.text.strip() == "Throttled":
        time.sleep(60)
        resp = requests.get(url)

    prices = resp.json()["prices"]

    # most recent rate from list
    return prices[-1][1]


def get_stx_usd_for_date(date: datetime) -> float:
    return get_historical_rate("blockstack", "usd", date)


def get_stx_btc_for_date(date: datetime) -> float:
    return get_historical_rate("blockstack", "btc", date)
