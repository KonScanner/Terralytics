import requests as rq
import streamlit as st
import pandas as pd
import json


def request_data(url: str):
    response = rq.get(url, headers={"Accept": "application/json"})
    if response.status_code == 200:
        return pd.DataFrame(response.json())
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
