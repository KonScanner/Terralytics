import requests as rq
import streamlit as st
import pandas as pd
import json


def request_data(url: str, return_df=True):
    response = rq.get(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        },
    )
    if response.status_code == 200:
        if return_df:
            return pd.DataFrame(response.json())
        else:
            return response.json()
    return pd.DataFrame([])


def read_config(fname: str = "config.json") -> dict:
    with open(fname, "r") as f:
        config = json.loads(f.read())
    return config


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def terra_network_metrics(trunc_date="daily") -> pd.DataFrame:
    urls = read_config()
    if trunc_date == "daily":
        url = urls["FLIPSIDE"]["TERRA"]["NETWORK_METRICS"]["DAILY"]
    elif trunc_date == "weekly":
        url = urls["FLIPSIDE"]["TERRA"]["NETWORK_METRICS"]["WEEKLY"]
    else:
        url = urls["FLIPSIDE"]["TERRA"]["NETWORK_METRICS"]["MONTHLY"]
    df = request_data(url=url)  # for now
    if df.empty:
        return None
    df["DATE"] = pd.to_datetime(df["DATE"])
    df = df[:-1]
    return df


def terra_bridge_metrics(trunc_date="daily") -> pd.DataFrame:
    urls = read_config()
    if trunc_date == "daily":
        url = urls["FLIPSIDE"]["TERRA"]["BRIDGE_METRICS"]["DAILY"]
    elif trunc_date == "weekly":
        url = urls["FLIPSIDE"]["TERRA"]["BRIDGE_METRICS"]["WEEKLY"]
    else:
        url = urls["FLIPSIDE"]["TERRA"]["BRIDGE_METRICS"]["WEEKLY"]
    df = request_data(url=url)
    if df.empty:
        return None
    df["DATE"] = pd.to_datetime(df["DATE"])
    df = df[:-1]
    return df


def terra_bridge_metrics2():
    urls = read_config()
    url = urls["FLIPSIDE"]["TERRA"]["BRIDGE_METRICS"]["IBC"]["DAILY"]
    df = request_data(url=url)
    if df.empty:
        return None
    df["DATE"] = pd.to_datetime(df["DATE"])
    df = df[:-1]
    return df


def terra_ust_metrics(vs_currency: str = "usd"):
    url = f"https://www.coingecko.com/market_cap/coins_market_cap_chart_data?coin_ids=325%2C6319%2C12681%2C9576%2C9956%2C16786%2C13422&locale=en&vs_currency={vs_currency}"
    results = request_data(url=url, return_df=False)
    dfs = []
    for result in results:
        name = result["name"]
        data = result["data"]
        df = pd.DataFrame(data)
        df.rename(
            {0: "date", 1: f"market_cap_{name.lower().replace(' ','_')}"},
            axis=1,
            inplace=True,
        )
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        dfs.append(df)
    expr = ""
    for i in range(len(dfs) - 2):
        if i == 0:
            expr += f'dfs[{i}].merge(dfs[{i+1}], on="date", how="inner").'
        if i < 7:
            expr += f'merge(dfs[{i+2}], on="date", how="inner").'
    df = eval(expr[:-1])
    return df
