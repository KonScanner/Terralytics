import streamlit as st
from utils.utils import (
    terra_network_metrics,
    terra_bridge_metrics,
    terra_bridge_metrics2,
)
import plotly.express as px

st.set_page_config(page_title="Terra Metrics Dashboard", page_icon="📈", layout="wide")
color = "#172852"
st.markdown("# [Terralytics](.)", unsafe_allow_html=True)
option = "daily"
option = st.selectbox("View:", ("daily", "weekly", "monthly"), index=1)


@st.cache(suppress_st_warning=True)
def load_data():
    network_metrics = terra_network_metrics(trunc_date=option)
    tx_count = network_metrics[["DATE", "TXN_COUNT"]].rename(
        columns={"DATE": "Date", "TXN_COUNT": "Terra Transaction Count"}
    )
    uq_addresses = network_metrics[["DATE", "ACTIVE_UNIQUE_ADDRESSES"]].rename(
        columns={"DATE": "Date", "ACTIVE_UNIQUE_ADDRESSES": "Terra Unique Addresses"}
    )
    avg_txn = network_metrics[["DATE", "AVG_TXN_PER_ADDRESS"]].rename(
        columns={
            "DATE": "Date",
            "AVG_TXN_PER_ADDRESS": "Terra Average Transactions per Unique Address",
        }
    )
    bridge_metrics_non_ibc = terra_bridge_metrics(trunc_date=option)
    bridge_metrics_non_ibc.rename(
        columns={
            "DATE": "Date",
            "TOTAL_AMOUNT_USD": "Total Amount USD",
            "AMOUNT_LUNA": "Amount LUNA",
            "AMOUNT_UST": "Amount UST",
            "DENOM": "Denomination",
            "LABEL": "Bridge Label",
        },
        inplace=True,
    )
    bridge_metrics_ibc = terra_bridge_metrics2()
    return (
        network_metrics,
        tx_count,
        uq_addresses,
        avg_txn,
        bridge_metrics_non_ibc,
        bridge_metrics_ibc,
    )


(
    network_metrics,
    tx_count,
    uq_addresses,
    avg_txn,
    bridge_metrics_non_ibc,
    bridge_metrics_ibc,
) = load_data()
st.markdown("## Network Metrics")
fig_cols = st.columns(3)
with fig_cols[0]:
    # st.markdown("### First Chart Title")
    fig = px.line(
        tx_count,
        x="Date",
        y="Terra Transaction Count",
        title=f"Terra Transaction count | {option.capitalize()}",
    )
    fig.update_traces(line_color=color)
    st.write(fig)
with fig_cols[1]:
    # st.markdown("### Second Chart Title")
    fig2 = px.line(
        uq_addresses,
        x="Date",
        y="Terra Unique Addresses",
        title=f"Terra Unique Addresses | {option.capitalize()}",
    )
    fig2.update_traces(line_color=color)
    st.write(fig2)
with fig_cols[2]:
    # st.markdown("### Third Chart Title")
    fig3 = px.line(
        avg_txn,
        x="Date",
        y="Terra Average Transactions per Unique Address",
        title=f"Terra Average Transactions per Unique Address | {option.capitalize()}",
    )
    fig3.update_traces(line_color=color)
    st.write(fig3)

st.markdown("## Bridge Metrics")
fig_cols2 = st.columns(2)
with fig_cols2[0]:
    opt = "weekly" if option == "monthly" else option
    fig4 = px.bar(
        bridge_metrics_non_ibc,
        x="Date",
        y="Amount LUNA",
        color="Bridge Label",
        title=f"Bridging OUT | LUNA Amount | Per bridge | {opt.capitalize()}",
    )
    fig4.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.write(fig4)

with fig_cols2[1]:
    opt = "weekly" if option == "monthly" else option
    fig5 = px.bar(
        bridge_metrics_non_ibc,
        x="Date",
        y="Amount UST",
        color="Bridge Label",
        title=f"Bridging OUT | UST Amount | Per bridge | {opt.capitalize()}",
    )
    fig5.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.write(fig5)

fig_cols3 = st.columns(2)
with fig_cols3[0]:
    opt = "weekly" if option == "monthly" else option
    fig6 = px.bar(
        bridge_metrics_non_ibc,
        x="Date",
        y="Total Amount USD",
        color="Bridge Label",
        title=f"Bridging OUT | USD amount | Per bridge | {opt.capitalize()}",
    )
    fig6.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.write(fig6)

with fig_cols3[1]:
    opt = "weekly" if option == "monthly" else option
    fig7 = px.bar(
        bridge_metrics_non_ibc,
        x="Date",
        y="Total Amount USD",
        color="Denomination",
        title=f"Bridging OUT | USD amount | Per coin | {opt.capitalize()}",
    )
    fig7.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.write(fig7)
# st.title("### Data Table")
# st.dataframe(df)
