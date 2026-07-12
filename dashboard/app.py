


# # import streamlit as st
# # import pandas as pd
# # from sqlalchemy import create_engine
# # import plotly.express as px
# # from streamlit_autorefresh import st_autorefresh

# # # -----------------------------
# # # AUTO REFRESH
# # # -----------------------------

# # st_autorefresh(interval=5000, key="refresh")

# # # -----------------------------
# # # DATABASE CONNECTION
# # # -----------------------------

# # engine = create_engine(
# #     "sqlite:///../app/fraud.db"
# # )

# # # -----------------------------
# # # LOAD DATA
# # # -----------------------------

# # query = "SELECT * FROM transactions"

# # df = pd.read_sql(query, engine)

# # # -----------------------------
# # # PAGE TITLE
# # # -----------------------------

# # st.title("🚨 Real-Time Fraud Monitoring System")

# # # -----------------------------
# # # EMPTY DATABASE CHECK
# # # -----------------------------

# # if df.empty:

# #     st.warning("No transactions found.")

# #     st.stop()

# # # -----------------------------
# # # FRAUD FILTER
# # # -----------------------------

# # frauds = df[df["risk_score"] >= 50]

# # # -----------------------------
# # # METRICS
# # # -----------------------------

# # total_transactions = len(df)

# # total_frauds = len(frauds)

# # fraud_percentage = round(
# #     (total_frauds / total_transactions) * 100,
# #     2
# # )

# # avg_risk = int(df["risk_score"].mean())

# # col1, col2, col3, col4 = st.columns(4)

# # col1.metric(
# #     "Total Transactions",
# #     total_transactions
# # )

# # col2.metric(
# #     "Fraud Transactions",
# #     total_frauds
# # )

# # col3.metric(
# #     "Fraud %",
# #     f"{fraud_percentage}%"
# # )

# # col4.metric(
# #     "Average Risk Score",
# #     avg_risk
# # )

# # # -----------------------------
# # # LIVE FRAUD ALERTS
# # # -----------------------------

# # st.subheader("🚨 High Risk Alerts")

# # if not frauds.empty:

# #     latest_frauds = frauds.tail(5)

# #     for _, row in latest_frauds.iterrows():

# #         st.error(
# #             f"""
# #             HIGH RISK TRANSACTION

# #             User: {row['user_id']}

# #             Country: {row['country']}

# #             Amount: ₹{row['amount']}

# #             Risk Score: {row['risk_score']}
# #             """
# #         )

# # else:

# #     st.success("No high-risk fraud detected.")

# # # -----------------------------
# # # LATEST TRANSACTIONS
# # # -----------------------------

# # st.subheader("📄 Latest Transactions")

# # st.dataframe(df.tail(20))

# # # -----------------------------
# # # COUNTRY ANALYSIS
# # # -----------------------------

# # st.subheader("🌍 Country Analysis")

# # fig1 = px.histogram(
# #     df,
# #     x="country",
# #     color="country",
# #     title="Transactions by Country"
# # )

# # st.plotly_chart(fig1)

# # # -----------------------------
# # # RISK SCORE DISTRIBUTION
# # # -----------------------------

# # st.subheader("⚠ Risk Score Distribution")

# # fig2 = px.histogram(
# #     df,
# #     x="risk_score",
# #     nbins=20,
# #     title="Risk Score Distribution"
# # )

# # st.plotly_chart(fig2)

# # # -----------------------------
# # # MERCHANT ANALYSIS
# # # -----------------------------

# # st.subheader("🏪 Merchant Analysis")

# # fig3 = px.pie(
# #     df,
# #     names="merchant",
# #     title="Merchant Distribution"
# # )

# # st.plotly_chart(fig3)

# # # -----------------------------
# # # TOP RISKY USERS
# # # -----------------------------

# # st.subheader("👤 Top Risky Users")

# # top_users = (
# #     df.groupby("user_id")["risk_score"]
# #     .mean()
# #     .sort_values(ascending=False)
# #     .head(10)
# # )

# # st.bar_chart(top_users)

# # # -----------------------------
# # # HIGH RISK TABLE
# # # -----------------------------

# # st.subheader("🚨 High Risk Transactions")

# # st.dataframe(
# #     frauds.sort_values(
# #         by="risk_score",
# #         ascending=False
# #     )
# # )


# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine
# import plotly.express as px
# from streamlit_autorefresh import st_autorefresh

# # -----------------------------
# # AUTO REFRESH
# # -----------------------------

# st_autorefresh(
#     interval=5000,
#     key="fraud_dashboard"
# )

# # -----------------------------
# # PAGE CONFIG
# # -----------------------------

# st.set_page_config(
#     page_title="Fraud Detection Dashboard",
#     layout="wide"
# )

# # -----------------------------
# # DATABASE CONNECTION
# # -----------------------------

# engine = create_engine(
#     "sqlite:///../app/fraud.db"
# )

# # -----------------------------
# # LOAD DATA
# # -----------------------------

# query = "SELECT * FROM transactions"

# df = pd.read_sql(
#     query,
#     engine
# )

# # -----------------------------
# # TITLE
# # -----------------------------

# st.title(
#     "🚨 Real-Time Fraud Detection Dashboard"
# )

# # -----------------------------
# # EMPTY CHECK
# # -----------------------------

# if df.empty:

#     st.warning(
#         "No transaction data found."
#     )

#     st.stop()

# # -----------------------------
# # METRICS
# # -----------------------------

# total_transactions = len(df)

# high_risk = len(
#     df[df["risk_score"] >= 70]
# )

# medium_risk = len(
#     df[
#         (df["risk_score"] >= 40)
#         &
#         (df["risk_score"] < 70)
#     ]
# )

# avg_risk = round(
#     df["risk_score"].mean(),
#     2
# )

# col1, col2, col3, col4 = st.columns(4)

# col1.metric(
#     "Total Transactions",
#     total_transactions
# )

# col2.metric(
#     "High Risk",
#     high_risk
# )

# col3.metric(
#     "Medium Risk",
#     medium_risk
# )

# col4.metric(
#     "Average Risk Score",
#     avg_risk
# )

# # -----------------------------
# # HIGH RISK ALERTS
# # -----------------------------

# st.subheader(
#     "🚨 Latest High Risk Alerts"
# )

# alerts = df[
#     df["risk_score"] >= 70
# ].tail(5)

# if not alerts.empty:

#     for _, row in alerts.iterrows():

#         st.error(
#             f"""
#             HIGH FRAUD RISK

#             User ID: {row['user_id']}

#             Merchant: {row['merchant']}

#             Country: {row['country']}

#             Amount: ₹{round(row['amount'], 2)}

#             Risk Score: {row['risk_score']}
#             """
#         )

# else:

#     st.success(
#         "No high-risk alerts."
#     )

# # -----------------------------
# # LATEST TRANSACTIONS
# # -----------------------------

# st.subheader(
#     "📄 Latest Transactions"
# )

# st.dataframe(
#     df.tail(20),
#     use_container_width=True
# )

# # -----------------------------
# # COUNTRY ANALYSIS
# # -----------------------------

# st.subheader(
#     "🌍 Transactions by Country"
# )

# country_chart = px.histogram(
#     df,
#     x="country",
#     color="country"
# )

# st.plotly_chart(
#     country_chart,
#     use_container_width=True
# )

# # -----------------------------
# # RISK DISTRIBUTION
# # -----------------------------

# st.subheader(
#     "⚠ Risk Score Distribution"
# )

# risk_chart = px.histogram(
#     df,
#     x="risk_score",
#     nbins=20
# )

# st.plotly_chart(
#     risk_chart,
#     use_container_width=True
# )

# # -----------------------------
# # MERCHANT ANALYSIS
# # -----------------------------

# st.subheader(
#     "🏪 Merchant Analysis"
# )

# merchant_chart = px.pie(
#     df,
#     names="merchant"
# )

# st.plotly_chart(
#     merchant_chart,
#     use_container_width=True
# )

# # -----------------------------
# # TOP RISKY USERS
# # -----------------------------

# st.subheader(
#     "👤 Top Risky Users"
# )

# top_users = (
#     df.groupby("user_id")[
#         "risk_score"
#     ]
#     .mean()
#     .sort_values(
#         ascending=False
#     )
#     .head(10)
# )

# st.bar_chart(top_users)


import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# AUTO REFRESH
# -----------------------------

st_autorefresh(
    interval=5000,
    key="fraud_dashboard"
)

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

# -----------------------------
# BACKEND CONFIGURATION
# -----------------------------
st.sidebar.markdown("### ⚙️ System Settings")
API_URL = st.sidebar.text_input("FastAPI Backend URL", "http://localhost:8000")

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data(ttl=2)
def load_data(url):
    try:
        response = requests.get(f"{url}/transactions", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if not data:
                return pd.DataFrame(columns=[
                    "id", "user_id", "merchant", "country",
                    "payment_method", "device", "amount",
                    "risk_score", "prediction", "timestamp"
                ])
            df = pd.DataFrame(data)
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df
    except Exception as e:
        st.sidebar.error(f"Error connecting to backend: {e}")
    return pd.DataFrame()

df = load_data(API_URL)

# -----------------------------
# TITLE
# -----------------------------

st.title(
    "🚨 Real-Time Fraud Detection Dashboard"
)

# -----------------------------
# EMPTY DATABASE CHECK
# -----------------------------

if df.empty:

    st.warning(
        "No transaction data found."
    )

    st.stop()

# -----------------------------
# LIVE CRITICAL FRAUD BANNER
# -----------------------------

critical_alerts = df[
    df["risk_score"] >= 90
]

if not critical_alerts.empty:

    st.markdown(
        """
        <div style="
            background-color:red;
            padding:20px;
            border-radius:10px;
            text-align:center;
            color:white;
            font-size:28px;
            font-weight:bold;
        ">
        🚨 CRITICAL FRAUD ALERT DETECTED 🚨
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# METRICS
# -----------------------------

total_transactions = len(df)

high_risk = len(
    df[df["risk_score"] >= 70]
)

medium_risk = len(
    df[
        (df["risk_score"] >= 40)
        &
        (df["risk_score"] < 70)
    ]
)

low_risk = len(
    df[df["risk_score"] < 40]
)

avg_risk = round(
    df["risk_score"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    total_transactions
)

col2.metric(
    "High Risk",
    high_risk
)

col3.metric(
    "Medium Risk",
    medium_risk
)

col4.metric(
    "Average Risk",
    avg_risk
)

# -----------------------------
# LIVE FRAUD ALERTS
# -----------------------------

st.subheader(
    "🚨 Live Fraud Alerts"
)

alerts = df[
    df["risk_score"] >= 40
].tail(10)

if not alerts.empty:

    for _, row in alerts.iterrows():

        severity = "LOW"

        if row["risk_score"] >= 90:

            severity = "CRITICAL"

        elif row["risk_score"] >= 70:

            severity = "HIGH"

        elif row["risk_score"] >= 40:

            severity = "MEDIUM"

        st.error(
            f"""
            🚨 {severity} FRAUD ALERT

            User ID: {row['user_id']}

            Merchant: {row['merchant']}

            Country: {row['country']}

            Amount: ₹{round(row['amount'], 2)}

            Risk Score: {row['risk_score']}
            """
        )

else:

    st.success(
        "No fraud alerts detected."
    )

# -----------------------------
# LATEST TRANSACTIONS
# -----------------------------

st.subheader(
    "📄 Latest Transactions"
)

st.dataframe(
    df.tail(20),
    use_container_width=True
)

# -----------------------------
# COUNTRY ANALYSIS
# -----------------------------

st.subheader(
    "🌍 Transactions by Country"
)

country_chart = px.histogram(
    df,
    x="country",
    color="country",
    title="Country Distribution"
)

st.plotly_chart(
    country_chart,
    use_container_width=True
)

# -----------------------------
# RISK DISTRIBUTION
# -----------------------------

st.subheader(
    "⚠ Risk Score Distribution"
)

risk_chart = px.histogram(
    df,
    x="risk_score",
    nbins=20,
    title="Risk Score Distribution"
)

st.plotly_chart(
    risk_chart,
    use_container_width=True
)

# -----------------------------
# MERCHANT ANALYSIS
# -----------------------------

st.subheader(
    "🏪 Merchant Analysis"
)

merchant_chart = px.pie(
    df,
    names="merchant",
    title="Merchant Transactions"
)

st.plotly_chart(
    merchant_chart,
    use_container_width=True
)

# -----------------------------
# TOP RISKY USERS
# -----------------------------

st.subheader(
    "👤 Top Risky Users"
)

top_users = (
    df.groupby("user_id")[
        "risk_score"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
)

st.bar_chart(top_users)

# -----------------------------
# RISK LEVEL COUNTS
# -----------------------------

st.subheader(
    "📊 Risk Level Summary"
)

risk_summary = pd.DataFrame({

    "Risk Level": [
        "Low",
        "Medium",
        "High"
    ],

    "Count": [
        low_risk,
        medium_risk,
        high_risk
    ]
})

summary_chart = px.bar(
    risk_summary,
    x="Risk Level",
    y="Count",
    title="Fraud Risk Levels"
)

st.plotly_chart(
    summary_chart,
    use_container_width=True
)

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
    "### ✅ AI-Powered Real-Time Fraud Monitoring System"
)