import streamlit as st

# -------------------------------
# Session state setup
# -------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# Login Page
# -------------------------------
def login_page():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == "admin" and password == "nightclub123":
                st.session_state.authenticated = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password")

# -------------------------------
# Main Calculator App
# -------------------------------
def power_of_one_app():
    st.title("Power of One Cashflow Calculator — Nightclub Edition (AED)")

    st.sidebar.header("📥 Input Your Financials")
    # 1. BASE INPUTS
    revenue = st.sidebar.number_input("Revenue (AED)", value=3500000, step=10000)
    cogs = st.sidebar.number_input("COGS (AED)", value=900000, step=10000)
    overheads = st.sidebar.number_input("Overheads (AED)", value=300000, step=10000)
    accounts_receivable = st.sidebar.number_input("Accounts Receivable (AED)", value=250000, step=10000)
    inventory = st.sidebar.number_input("Inventory (AED)", value=150000, step=10000)
    accounts_payable = st.sidebar.number_input("Accounts Payable (AED)", value=180000, step=10000)
    base_cashflow = st.sidebar.number_input("Net Cash Flow (AED)", value=300000, step=10000)
    base_profit = st.sidebar.number_input("Operating Profit (AED)", value=2300000, step=10000)

    # 2. DETAILED EXPENSE LINES
    promo_groups = st.sidebar.number_input("Promo Groups & CoOrganizers Incentives (AED)", value=0, step=1000)
    part_time_cogs = st.sidebar.number_input("Part-time Staff and Services COGS (AED)", value=0, step=1000)
    art_entertainment = st.sidebar.number_input("Art & Entertainment (AED)", value=0, step=1000)
    marketing_expenses = st.sidebar.number_input("Marketing (AED)", value=0, step=1000)
    operation_expenses = st.sidebar.number_input("Operation Expenses (AED)", value=0, step=1000)
    rent_utility = st.sidebar.number_input("Rent & Utility (AED)", value=0, step=1000)
    production_services = st.sidebar.number_input("Production Services & Maintenance (AED)", value=0, step=1000)
    production_employees = st.sidebar.number_input("Production Employees (AED)", value=0, step=1000)
    financial_legal = st.sidebar.number_input("Financial & Legal Fees (AED)", value=0, step=1000)
    commercial_employees = st.sidebar.number_input("Commercial Employees (AED)", value=0, step=1000)
    admin_services = st.sidebar.number_input("Administrative Services (AED)", value=0, step=1000)

    # Compose total overheads and cogs for summary & core adjustments
    total_overheads = (overheads + marketing_expenses + operation_expenses + rent_utility +
                       production_services + production_employees + financial_legal +
                       commercial_employees + admin_services + promo_groups + art_entertainment)
    total_cogs = cogs + part_time_cogs

    st.subheader("Your Current Position")
    st.metric(label="Net Cash Flow", value=f"AED {base_cashflow:,.0f}")
    st.metric(label="Operating Profit", value=f"AED {base_profit:,.0f}")

    with st.expander("Additional Expense Parameters (current values)"):
        st.write(f"Promo Groups & CoOrganizers Incentives: AED {promo_groups:,.0f}")
        st.write(f"Part-time Staff and Services COGS: AED {part_time_cogs:,.0f}")
        st.write(f"Art & Entertainment: AED {art_entertainment:,.0f}")
        st.write(f"Marketing: AED {marketing_expenses:,.0f}")
        st.write(f"Operation Expenses: AED {operation_expenses:,.0f}")
        st.write(f"Rent & Utility: AED {rent_utility:,.0f}")
        st.write(f"Production Services & Maintenance: AED {production_services:,.0f}")
        st.write(f"Production Employees: AED {production_employees:,.0f}")
        st.write(f"Financial & Legal Fees: AED {financial_legal:,.0f}")
        st.write(f"Commercial Employees: AED {commercial_employees:,.0f}")
        st.write(f"Administrative Services: AED {admin_services:,.0f}")

    st.metric(label="Total Overheads (incl. breakdown)", value=f"AED {total_overheads:,.0f}")
    st.metric(label="Total COGS (incl. part-time/services)", value=f"AED {total_cogs:,.0f}")

    # ========== POWER OF ONE — CORE LEVERS ==========
    st.subheader("Your Power of One (Core Levers)")
    adjustments = {
        "Price Increase": revenue,
        "Volume Increase": revenue,
        "Cost of Goods Reduction": total_cogs,
        "Overheads Reduction": total_overheads,
        "Reduction in Accounts Receivable Days": accounts_receivable,
        "Reduction in Inventory Days": inventory,
        "Increase in Accounts Payable Days": accounts_payable
    }

    st.markdown("### Core Adjustments Summary")
    header_cols = st.columns([3, 2, 2, 3])
    header_cols[0].markdown("**Adjustment**")
    header_cols[1].markdown("**% Change**")
    header_cols[2].markdown("**Impact on Cash Flow**")
    header_cols[3].markdown("**Impact on EBIT**")

    total_cashflow = 0
    total_profit = 0

    for label, base_impact in adjustments.items():
        cols = st.columns([3, 2, 2, 3])
        with cols[0]:
            st.write(label)
        with cols[1]:
            change = st.number_input(
                f"{label} % Change",
                min_value=-100.0,
                max_value=100.0,
                step=1.0,
                value=0.0,
                key=label)
        impact_cashflow = base_impact * (change / 100)
        impact_profit = base_impact * (change / 100)
        total_cashflow += impact_cashflow
        total_profit += impact_profit

        arrow_cf = "↑" if impact_cashflow > 0 else "↓" if impact_cashflow < 0 else ""
        arrow_pf = "↑" if impact_profit > 0 else "↓" if impact_profit < 0 else ""
        color_cf = "green" if impact_cashflow > 0 else "red" if impact_cashflow < 0 else "gray"
        color_pf = "green" if impact_profit > 0 else "red" if impact_profit < 0 else "gray"

        with cols[2]:
            st.markdown(f"<span style='color:{color_cf}'>{arrow_cf} AED {impact_cashflow:,.0f}</span>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"<span style='color:{color_pf}'>{arrow_pf} AED {impact_profit:,.0f}</span>", unsafe_allow_html=True)

    # ========== POWER OF ONE — DETAILED EXPENSES ==========
    st.subheader("Additional Expense Levers: Power of One")
    expense_levers = {
        "Promo Groups & CoOrganizers Incentives": promo_groups,
        "Part-time Staff and Services COGS": part_time_cogs,
        "Art & Entertainment": art_entertainment,
        "Marketing": marketing_expenses,
        "Operation Expenses": operation_expenses,
        "Rent & Utility": rent_utility,
        "Production Services & Maintenance": production_services,
        "Production Employees": production_employees,
        "Financial & Legal Fees": financial_legal,
        "Commercial Employees": commercial_employees,
        "Administrative Services": admin_services
    }

    expense_header = st.columns([3, 2, 2, 3])
    expense_header[0].markdown("**Expense Item**")
    expense_header[1].markdown("**% Change**")
    expense_header[2].markdown("**Impact on Cash Flow**")
    expense_header[3].markdown("**Impact on EBIT**")

    exp_total_cash = 0
    exp_total_profit = 0

    for label, base_value in expense_levers.items():
        cols = st.columns([3, 2, 2, 3])
        with cols[0]:
            st.write(label)
        with cols[1]:
            exp_percent = st.number_input(
                f"{label} % Change",
                min_value=-100.0,
                max_value=100.0,
                step=1.0,
                value=0.0,
                key=f"exp_{label}"
            )
        # For expenses, a REDUCTION is positive for profit/cash flow
        exp_impact_cashflow = -base_value * (exp_percent / 100)
        exp_impact_profit = -base_value * (exp_percent / 100)
        exp_total_cash += exp_impact_cashflow
        exp_total_profit += exp_impact_profit

        arrow_cf = "↑" if exp_impact_cashflow > 0 else "↓" if exp_impact_cashflow < 0 else ""
        arrow_pf = "↑" if exp_impact_profit > 0 else "↓" if exp_impact_profit < 0 else ""
        color_cf = "green" if exp_impact_cashflow > 0 else "red" if exp_impact_cashflow < 0 else "gray"
        color_pf = "green" if exp_impact_profit > 0 else "red" if exp_impact_profit < 0 else "gray"

        with cols[2]:
            st.markdown(f"<span style='color:{color_cf}'>{arrow_cf} AED {exp_impact_cashflow:,.0f}</span>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"<span style='color:{color_pf}'>{arrow_pf} AED {exp_impact_profit:,.0f}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.success("TOTAL Power of One Impact (all levers)")
    final_delta_cash = total_cashflow + exp_total_cash
    final_delta_profit = total_profit + exp_total_profit

    st.metric(label="New Net Cash Flow",
              value=f"AED {base_cashflow + final_delta_cash:,.0f}",
              delta=f"AED {final_delta_cash:,.0f}")

    st.metric(label="New Operating Profit",
              value=f"AED {base_profit + final_delta_profit:,.0f}",
              delta=f"AED {final_delta_profit:,.0f}")

    st.button("Logout", on_click=logout)

# -------------------------------
# Logout handler
# -------------------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""

# -------------------------------
# App Controller
# -------------------------------
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        power_of_one_app()

if __name__ == "__main__":
    main()
