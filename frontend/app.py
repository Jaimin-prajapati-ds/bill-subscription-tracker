import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import json

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Bill Subscription Tracker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(" Bill & Subscription Tracker")
st.markdown("*Track recurring payments, visualize spending, and never miss a renewal*")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select a section:",
        ["Dashboard", "Add Subscription", "Manage", "Analytics", "Reminders", "Export"]
    )
    st.markdown("---")
    st.markdown("### Quick Stats")
    try:
        resp = requests.get(f"{API_URL}/subscriptions")
        if resp.status_code == 200:
            subs = resp.json()
            st.metric("Total Subscriptions", len(subs))
            total_monthly = sum(s["amount"] if s["cycle"] == "monthly" else s["amount"]/12 for s in subs)
            st.metric("Monthly Cost", f"${total_monthly:.2f}")
    except:
        st.warning("Backend not reachable")

if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    try:
        resp = requests.get(f"{API_URL}/subscriptions/due/today")
        data = resp.json()
        col1.metric("Due Today", data["count"], ":red" if data["count"] > 0 else ":green")
    except:
        col1.metric("Due Today", "0")
    try:
        resp = requests.get(f"{API_URL}/subscriptions/due/soon?days=3")
        data = resp.json()
        col2.metric("Due in 3 Days", data["count"], ":orange" if data["count"] > 0 else ":green")
    except:
        col2.metric("Due in 3 Days", "0")
    try:
        resp = requests.get(f"{API_URL}/subscriptions")
        subs = resp.json()
        col3.metric("Total Subscriptions", len(subs))
    except:
        col3.metric("Total Subscriptions", "0")
    st.markdown("---")
    st.subheader("All Subscriptions")
    try:
        resp = requests.get(f"{API_URL}/subscriptions")
        subs = resp.json()
        if subs:
            df = pd.DataFrame(subs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No subscriptions yet. Add one to get started!")
    except:
        st.error("Failed to fetch subscriptions")

elif page == "Add Subscription":
    st.subheader("Add New Subscription/Bill")
    with st.form("add_subscription_form"):
        name = st.text_input("Subscription Name*", placeholder="e.g., Netflix")
        amount = st.number_input("Amount*", min_value=0.01, step=0.01)
        cycle = st.selectbox("Billing Cycle*", ["monthly", "annual", "one-time"])
        next_due = st.date_input("Next Due Date*")
        category = st.selectbox("Category*", ["OTT", "Utility", "Recharge", "SaaS", "Insurance", "Other"])
        notes = st.text_area("Notes", placeholder="Optional notes")
        submit = st.form_submit_button("Add Subscription")
        if submit:
            try:
                payload = {
                    "name": name,
                    "amount": amount,
                    "cycle": cycle,
                    "next_due": str(next_due),
                    "category": category,
                    "notes": notes
                }
                resp = requests.post(f"{API_URL}/subscriptions", json=payload)
                if resp.status_code == 200:
                    st.success("Subscription added successfully!")
                else:
                    st.error("Failed to add subscription")
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif page == "Manage":
    st.subheader("Manage Subscriptions")
    try:
        resp = requests.get(f"{API_URL}/subscriptions")
        subs = resp.json()
        if subs:
            selected = st.selectbox("Select subscription to edit/delete:", [s["name"] for s in subs])
            sub = next((s for s in subs if s["name"] == selected), None)
            if sub:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Delete"):
                        resp = requests.delete(f"{API_URL}/subscriptions/{sub['id']}")
                        if resp.status_code == 200:
                            st.success("Deleted!")
                        else:
                            st.error("Failed to delete")
                with col2:
                    st.write(f"ID: {sub['id']} | Amount: ${sub['amount']} | Due: {sub['next_due']}")
        else:
            st.info("No subscriptions to manage")
    except:
        st.error("Failed to fetch subscriptions")

elif page == "Analytics":
    st.subheader("Spending Analytics")
    try:
        resp = requests.get(f"{API_URL}/subscriptions/summary/monthly")
        summary = resp.json()
        fig = go.Figure(data=[go.Pie(labels=list(summary["by_category"].keys()), values=list(summary["by_category"].values()))])
        fig.update_layout(title=f"Monthly Spending by Category (Total: ${summary['total_monthly']:.2f})")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Failed to fetch analytics")

elif page == "Reminders":
    st.subheader("Renewal Reminders")
    try:
        resp = requests.get(f"{API_URL}/subscriptions/due/today")
        today_data = resp.json()
        st.warning(f"⚠️ Due Today: {today_data['count']} subscriptions")
        if today_data["subscriptions"]:
            for sub in today_data["subscriptions"]:
                st.info(f"{sub['name']} - ${sub['amount']} ({sub['cycle']})")
        resp = requests.get(f"{API_URL}/subscriptions/due/soon?days=7")
        soon_data = resp.json()
        st.info(f"📅 Due in Next 7 Days: {soon_data['count']} subscriptions")
        if soon_data["subscriptions"]:
            for sub in soon_data["subscriptions"]:
                st.success(f"{sub['name']} - {sub['next_due']}")
    except:
        st.error("Failed to fetch reminders")

elif page == "Export":
    st.subheader("Export Data")
    try:
        resp = requests.get(f"{API_URL}/subscriptions")
        subs = resp.json()
        if subs:
            df = pd.DataFrame(subs)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "subscriptions.csv", "text/csv")
        else:
            st.info("No data to export")
    except:
        st.error("Failed to export data")

st.markdown("---")
st.caption("Bill Subscription Tracker | Track smart, pay smart")
