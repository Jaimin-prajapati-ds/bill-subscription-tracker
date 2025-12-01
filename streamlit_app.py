import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import json

# Page config
st.set_page_config(
    page_title="Bill Subscription Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for subscriptions
if 'subscriptions' not in st.session_state:
    st.session_state.subscriptions = [
        {"id": 1, "name": "Netflix", "amount": 199, "cycle": "monthly", "next_due": "2025-12-05", "category": "OTT", "notes": "Premium plan"},
        {"id": 2, "name": "Spotify", "amount": 119, "cycle": "monthly", "next_due": "2025-12-10", "category": "OTT", "notes": "Music streaming"},
        {"id": 3, "name": "Amazon Prime", "amount": 1499, "cycle": "annual", "next_due": "2025-12-15", "category": "OTT", "notes": "Annual membership"},
    ]

if 'next_id' not in st.session_state:
    st.session_state.next_id = 4

# Title
st.title("💰 Bill & Subscription Tracker")
st.markdown("*Track recurring payments, visualize spending, and never miss a renewal*")

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select a section:",
        ["Dashboard", "Add Subscription", "Manage", "Analytics", "Reminders", "Export"]
    )
    st.markdown("---")
    st.markdown("### Quick Stats")
    subs = st.session_state.subscriptions
    st.metric("Total Subscriptions", len(subs))
    total_monthly = sum(s["amount"] if s["cycle"] == "monthly" else s["amount"]/12 for s in subs)
    st.metric("Monthly Cost", f"₹{total_monthly:.2f}")

if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    
    # Calculate due subscriptions
    today = date.today()
    due_today = [s for s in st.session_state.subscriptions if s["next_due"] == str(today)]
    due_soon = [s for s in st.session_state.subscriptions 
                if date.fromisoformat(s["next_due"]) <= today + timedelta(days=3) and date.fromisoformat(s["next_due"]) > today]
    
    col1.metric("Due Today", len(due_today), delta=None if len(due_today) == 0 else "⚠️")
    col2.metric("Due in 3 Days", len(due_soon))
    col3.metric("Total Subscriptions", len(st.session_state.subscriptions))
    
    st.markdown("---")
    st.subheader("All Subscriptions")
    
    if st.session_state.subscriptions:
        df = pd.DataFrame(st.session_state.subscriptions)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No subscriptions yet. Add one to get started!")

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
            if name and amount:
                new_sub = {
                    "id": st.session_state.next_id,
                    "name": name,
                    "amount": amount,
                    "cycle": cycle,
                    "next_due": str(next_due),
                    "category": category,
                    "notes": notes
                }
                st.session_state.subscriptions.append(new_sub)
                st.session_state.next_id += 1
                st.success("Subscription added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")

elif page == "Manage":
    st.subheader("Manage Subscriptions")
    
    if st.session_state.subscriptions:
        selected = st.selectbox("Select subscription to edit/delete:", 
                                [s["name"] for s in st.session_state.subscriptions])
        
        sub = next((s for s in st.session_state.subscriptions if s["name"] == selected), None)
        
        if sub:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Delete", type="primary"):
                    st.session_state.subscriptions = [s for s in st.session_state.subscriptions if s["id"] != sub["id"]]
                    st.success("Deleted!")
                    st.rerun()
            
            with col2:
                st.write(f"**ID:** {sub['id']} | **Amount:** ₹{sub['amount']} | **Due:** {sub['next_due']}")
    else:
        st.info("No subscriptions to manage")

elif page == "Analytics":
    st.subheader("Spending Analytics")
    
    if st.session_state.subscriptions:
        # Calculate by category
        category_sum = {}
        for s in st.session_state.subscriptions:
            monthly_cost = s["amount"] if s["cycle"] == "monthly" else s["amount"]/12
            category_sum[s["category"]] = category_sum.get(s["category"], 0) + monthly_cost
        
        total_monthly = sum(category_sum.values())
        
        fig = go.Figure(data=[go.Pie(labels=list(category_sum.keys()), 
                                     values=list(category_sum.values()))])
        fig.update_layout(title=f"Monthly Spending by Category (Total: ₹{total_monthly:.2f})")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data to display")

elif page == "Reminders":
    st.subheader("Renewal Reminders")
    
    today = date.today()
    due_today = [s for s in st.session_state.subscriptions if s["next_due"] == str(today)]
    due_soon = [s for s in st.session_state.subscriptions 
                if date.fromisoformat(s["next_due"]) <= today + timedelta(days=7) 
                and date.fromisoformat(s["next_due"]) > today]
    
    if due_today:
        st.warning(f"⚠️ Due Today: {len(due_today)} subscriptions")
        for sub in due_today:
            st.error(f"**{sub['name']}** - ₹{sub['amount']} ({sub['cycle']})")
    else:
        st.success("✅ No subscriptions due today")
    
    st.markdown("---")
    
    if due_soon:
        st.info(f"📅 Due in Next 7 Days: {len(due_soon)} subscriptions")
        for sub in due_soon:
            st.info(f"**{sub['name']}** - Due on {sub['next_due']}")
    else:
        st.success("All clear for the next week!")

elif page == "Export":
    st.subheader("Export Data")
    
    if st.session_state.subscriptions:
        df = pd.DataFrame(st.session_state.subscriptions)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "subscriptions.csv", "text/csv")
    else:
        st.info("No data to export")

st.markdown("---")
st.caption("Bill Subscription Tracker | Track smart, pay smart 💡")
