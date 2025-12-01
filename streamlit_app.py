import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta, datetime
import json

# Page config
st.set_page_config(
    page_title="Bill Subscription Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alert-card {
        background: #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .success-card {
        background: #51cf66;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with better sample data
if 'subscriptions' not in st.session_state:
    st.session_state.subscriptions = [
        {
            "id": 1, 
            "name": "Netflix", 
            "amount": 199, 
            "cycle": "monthly", 
            "next_due": str(date.today() + timedelta(days=2)), 
            "category": "OTT", 
            "notes": "Premium HD plan",
            "created_at": str(datetime.now())
        },
        {
            "id": 2, 
            "name": "Spotify Premium", 
            "amount": 119, 
            "cycle": "monthly", 
            "next_due": str(date.today() + timedelta(days=5)), 
            "category": "OTT", 
            "notes": "Music streaming",
            "created_at": str(datetime.now())
        },
        {
            "id": 3, 
            "name": "Amazon Prime", 
            "amount": 1499, 
            "cycle": "annual", 
            "next_due": str(date.today() + timedelta(days=30)), 
            "category": "OTT", 
            "notes": "Annual membership",
            "created_at": str(datetime.now())
        },
        {
            "id": 4, 
            "name": "Mobile Recharge", 
            "amount": 399, 
            "cycle": "monthly", 
            "next_due": str(date.today()), 
            "category": "Recharge", 
            "notes": "Jio plan",
            "created_at": str(datetime.now())
        },
    ]

if 'next_id' not in st.session_state:
    st.session_state.next_id = 5

# Helper functions
def calculate_monthly_cost(amount, cycle):
    """Convert any subscription to monthly cost"""
    if cycle == "monthly":
        return amount
    elif cycle == "annual":
        return amount / 12
    else:  # one-time
        return 0

def get_due_subscriptions(days=0):
    """Get subscriptions due in next N days"""
    today = date.today()
    target_date = today + timedelta(days=days)
    
    due_subs = []
    for sub in st.session_state.subscriptions:
        due_date = date.fromisoformat(sub["next_due"])
        if days == 0:
            if due_date == today:
                due_subs.append(sub)
        else:
            if today < due_date <= target_date:
                due_subs.append(sub)
    return due_subs

def get_ai_insights():
    """Generate AI-powered insights"""
    subs = st.session_state.subscriptions
    if not subs:
        return []
    
    insights = []
    
    # Calculate category spending
    category_spending = {}
    for sub in subs:
        monthly = calculate_monthly_cost(sub["amount"], sub["cycle"])
        category_spending[sub["category"]] = category_spending.get(sub["category"], 0) + monthly
    
    # Find highest spending category
    if category_spending:
        max_category = max(category_spending, key=category_spending.get)
        insights.append(f"💡 Your highest spending category is **{max_category}** (₹{category_spending[max_category]:.2f}/month)")
    
    # Check for annual subscriptions
    annual_count = sum(1 for s in subs if s["cycle"] == "annual")
    if annual_count > 0:
        insights.append(f"📊 You have **{annual_count}** annual subscriptions. Consider switching to monthly for better cash flow.")
    
    # Check for due subscriptions
    due_soon = get_due_subscriptions(7)
    if len(due_soon) > 3:
        insights.append(f"⚠️ You have **{len(due_soon)}** renewals in the next 7 days. Budget accordingly!")
    
    # Total spending insight
    total_monthly = sum(calculate_monthly_cost(s["amount"], s["cycle"]) for s in subs)
    insights.append(f"💰 Your total monthly subscription cost is **₹{total_monthly:.2f}**")
    
    return insights

# Main title
st.markdown('<div class="main-header">💰 Bill & Subscription Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Track recurring payments, visualize spending, and never miss a renewal</div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio(
        "Select a section:",
        ["📊 Dashboard", "➕ Add Subscription", "⚙️ Manage", "📈 Analytics", "🔔 Reminders", "💾 Export"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📌 Quick Stats")
    
    subs = st.session_state.subscriptions
    total_monthly = sum(calculate_monthly_cost(s["amount"], s["cycle"]) for s in subs)
    total_annual = total_monthly * 12
    
    st.metric("Total Subscriptions", len(subs))
    st.metric("Monthly Cost", f"₹{total_monthly:.2f}")
    st.metric("Annual Cost", f"₹{total_annual:.2f}")
    
    due_today = get_due_subscriptions(0)
    if due_today:
        st.error(f"⚠️ {len(due_today)} due today!")
    
    st.markdown("---")
    st.markdown("### 🎯 AI Insights")
    insights = get_ai_insights()
    for insight in insights[:2]:  # Show first 2 insights
        st.info(insight)

# Page routing
if page == "📊 Dashboard":
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    due_today = get_due_subscriptions(0)
    due_week = get_due_subscriptions(7)
    
    with col1:
        st.metric(
            "Due Today", 
            len(due_today),
            delta="Urgent" if len(due_today) > 0 else "None",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Due in 7 Days", 
            len(due_week),
            delta="Plan ahead" if len(due_week) > 0 else "All clear",
            delta_color="normal"
        )
    
    with col3:
        st.metric("Active Subscriptions", len(st.session_state.subscriptions))
    
    with col4:
        total_monthly = sum(calculate_monthly_cost(s["amount"], s["cycle"]) for s in st.session_state.subscriptions)
        st.metric("Monthly Spend", f"₹{total_monthly:.2f}")
    
    st.markdown("---")
    
    # Urgent alerts
    if due_today:
        st.markdown('<div class="alert-card">⚠️ <b>URGENT:</b> Pay these subscriptions today!</div>', unsafe_allow_html=True)
        for sub in due_today:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{sub['name']}**")
            col2.write(f"₹{sub['amount']}")
            col3.write(sub['cycle'])
    
    st.subheader("📋 All Subscriptions")
    
    if st.session_state.subscriptions:
        df = pd.DataFrame(st.session_state.subscriptions)
        
        # Add monthly cost column
        df['monthly_cost'] = df.apply(lambda row: calculate_monthly_cost(row['amount'], row['cycle']), axis=1)
        
        # Reorder columns
        column_order = ['name', 'amount', 'cycle', 'next_due', 'category', 'monthly_cost', 'notes']
        df = df[column_order]
        
        # Format column names
        df.columns = ['Name', 'Amount (₹)', 'Cycle', 'Next Due', 'Category', 'Monthly Cost (₹)', 'Notes']
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Monthly Cost (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Next Due": st.column_config.DateColumn(format="DD/MM/YYYY")
            }
        )
    else:
        st.info("📭 No subscriptions yet. Add your first one to get started!")

elif page == "➕ Add Subscription":
    st.subheader("Add New Subscription/Bill")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("add_subscription_form", clear_on_submit=True):
            name = st.text_input("Subscription Name*", placeholder="e.g., Netflix, Electricity Bill")
            amount = st.number_input("Amount (₹)*", min_value=0.01, step=1.0, format="%.2f")
            cycle = st.selectbox("Billing Cycle*", ["monthly", "annual", "one-time"])
            next_due = st.date_input("Next Due Date*", value=date.today() + timedelta(days=30))
            category = st.selectbox(
                "Category*", 
                ["OTT", "Utility", "Recharge", "SaaS", "Insurance", "Education", "Fitness", "Other"]
            )
            notes = st.text_area("Notes (Optional)", placeholder="Add any additional notes here...")
            
            submit = st.form_submit_button("➕ Add Subscription", use_container_width=True, type="primary")
            
            if submit:
                if name and amount:
                    new_sub = {
                        "id": st.session_state.next_id,
                        "name": name.strip(),
                        "amount": float(amount),
                        "cycle": cycle,
                        "next_due": str(next_due),
                        "category": category,
                        "notes": notes.strip(),
                        "created_at": str(datetime.now())
                    }
                    st.session_state.subscriptions.append(new_sub)
                    st.session_state.next_id += 1
                    st.success(f"✅ '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
    
    with col2:
        st.info("""
        **💡 Quick Tips:**
        
        - Choose **monthly** for recurring monthly bills
        - Choose **annual** for yearly subscriptions
        - Choose **one-time** for single payments
        - Set **Next Due Date** accurately to get timely reminders
        - Use **Notes** for payment methods, discount codes, etc.
        """)
        
        if st.session_state.subscriptions:
            st.success(f"📊 You currently have **{len(st.session_state.subscriptions)}** active subscriptions.")

elif page == "⚙️ Manage":
    st.subheader("Manage Subscriptions")
    
    if st.session_state.subscriptions:
        # Search/filter
        search = st.text_input("🔍 Search subscriptions", placeholder="Type to filter...")
        
        filtered_subs = st.session_state.subscriptions
        if search:
            filtered_subs = [
                s for s in st.session_state.subscriptions 
                if search.lower() in s["name"].lower() or search.lower() in s["category"].lower()
            ]
        
        if not filtered_subs:
            st.warning("No subscriptions match your search.")
        else:
            selected_name = st.selectbox(
                "Select subscription to manage:", 
                [s["name"] for s in filtered_subs],
                key="manage_select"
            )
            
            sub = next((s for s in filtered_subs if s["name"] == selected_name), None)
            
            if sub:
                st.markdown("---")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Subscription Details:**
                    - 💳 **Name:** {sub['name']}
                    - 💰 **Amount:** ₹{sub['amount']}
                    - 🔄 **Cycle:** {sub['cycle'].title()}
                    - 📅 **Next Due:** {sub['next_due']}
                    - 📂 **Category:** {sub['category']}
                    - 📝 **Notes:** {sub['notes'] or 'N/A'}
                    """)
                
                with col2:
                    if st.button("🗑️ Delete", type="primary", use_container_width=True):
                        st.session_state.subscriptions = [
                            s for s in st.session_state.subscriptions if s["id"] != sub["id"]
                        ]
                        st.success(f"✅ '{sub['name']}' deleted successfully!")
                        st.rerun()
                    
                    if st.button("🔄 Mark as Paid", use_container_width=True):
                        # Update next due date based on cycle
                        current_due = date.fromisoformat(sub["next_due"])
                        if sub["cycle"] == "monthly":
                            new_due = current_due + timedelta(days=30)
                        elif sub["cycle"] == "annual":
                            new_due = current_due + timedelta(days=365)
                        else:
                            new_due = current_due
                        
                        for s in st.session_state.subscriptions:
                            if s["id"] == sub["id"]:
                                s["next_due"] = str(new_due)
                        
                        st.success(f"✅ Marked as paid! Next due: {new_due}")
                        st.rerun()
    else:
        st.info("📭 No subscriptions to manage. Add some first!")

elif page == "📈 Analytics":
    st.subheader("Spending Analytics")
    
    if st.session_state.subscriptions:
        # Category breakdown
        category_data = {}
        for sub in st.session_state.subscriptions:
            monthly = calculate_monthly_cost(sub["amount"], sub["cycle"])
            category_data[sub["category"]] = category_data.get(sub["category"], 0) + monthly
        
        total_monthly = sum(category_data.values())
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(category_data.keys()), 
                values=list(category_data.values()),
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            fig_pie.update_layout(
                title=f"Monthly Spending by Category (Total: ₹{total_monthly:.2f})",
                height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = go.Figure(data=[go.Bar(
                x=list(category_data.keys()),
                y=list(category_data.values()),
                marker=dict(color=list(category_data.values()), colorscale='Viridis')
            )])
            fig_bar.update_layout(
                title="Category-wise Monthly Spending",
                xaxis_title="Category",
                yaxis_title="Amount (₹)",
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed breakdown table
        st.subheader("Detailed Breakdown")
        breakdown_data = []
        for category, amount in category_data.items():
            count = sum(1 for s in st.session_state.subscriptions if s["category"] == category)
            breakdown_data.append({
                "Category": category,
                "Subscriptions": count,
                "Monthly Cost (₹)": f"₹{amount:.2f}",
                "Annual Cost (₹)": f"₹{amount * 12:.2f}",
                "Percentage": f"{(amount/total_monthly)*100:.1f}%"
            })
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
        
        # AI Insights
        st.markdown("---")
        st.subheader("🤖 AI-Powered Insights")
        insights = get_ai_insights()
        for i, insight in enumerate(insights, 1):
            st.markdown(f"{i}. {insight}")
    else:
        st.info("📭 No data to display. Add subscriptions first!")

elif page == "🔔 Reminders":
    st.subheader("Renewal Reminders")
    
    today = date.today()
    due_today = get_due_subscriptions(0)
    due_3days = get_due_subscriptions(3)
    due_week = get_due_subscriptions(7)
    
    # Due today
    if due_today:
        st.markdown('<div class="alert-card">🚨 <b>URGENT: Due Today</b></div>', unsafe_allow_html=True)
        for sub in due_today:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            col1.error(f"**{sub['name']}**")
            col2.write(f"₹{sub['amount']}")
            col3.write(sub['cycle'])
            col4.write(sub['category'])
    else:
        st.markdown('<div class="success-card">✅ No subscriptions due today!</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Due in 3 days
    if due_3days:
        st.warning(f"⚠️ **Due in Next 3 Days:** {len(due_3days)} subscriptions")
        for sub in due_3days:
            days_left = (date.fromisoformat(sub['next_due']) - today).days
            st.info(f"📅 **{sub['name']}** - ₹{sub['amount']} (Due in {days_left} days)")
    
    st.markdown("---")
    
    # Due in week
    if due_week:
        st.info(f"📆 **Due in Next 7 Days:** {len(due_week)} subscriptions")
        for sub in due_week:
            days_left = (date.fromisoformat(sub['next_due']) - today).days
            if days_left > 3:  # Don't show ones already shown in 3-day section
                st.success(f"✓ **{sub['name']}** - ₹{sub['amount']} (Due in {days_left} days)")
    
    if not due_today and not due_3days and not due_week:
        st.success("🎉 All clear! No renewals in the next week.")

elif page == "💾 Export":
    st.subheader("Export Your Data")
    
    if st.session_state.subscriptions:
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Export Options:**
            
            Download your subscription data as CSV for:
            - Backup purposes
            - Analysis in Excel/Google Sheets
            - Importing to other apps
            - Sharing with financial advisors
            """)
        
        with col2:
            df = pd.DataFrame(st.session_state.subscriptions)
            
            # Calculate monthly costs
            df['monthly_cost'] = df.apply(
                lambda row: calculate_monthly_cost(row['amount'], row['cycle']), 
                axis=1
            )
            
            # Add summary stats
            total_monthly = df['monthly_cost'].sum()
            total_annual = total_monthly * 12
            
            st.metric("Total Subscriptions", len(df))
            st.metric("Monthly Cost", f"₹{total_monthly:.2f}")
            st.metric("Annual Cost", f"₹{total_annual:.2f}")
        
        st.markdown("---")
        
        # CSV download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"subscriptions_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
        
        # JSON download
        json_data = json.dumps(st.session_state.subscriptions, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"subscriptions_{date.today()}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("Preview")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No data to export. Add subscriptions first!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><b>Bill Subscription Tracker</b> | Track Smart, Pay Smart 💡</p>
        <p style='font-size: 0.8rem;'>Built with ❤️ using Streamlit | 
        <a href='https://github.com/Jaimin-prajapati-ds/bill-subscription-tracker' target='_blank'>GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)
