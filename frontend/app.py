import streamlit as st
import requests
import pandas as pd  # Required for chart display

# Set backend URL (will work in Docker or local dev)
BACKEND_URL = "http://backend:8000"  # For Docker Compose
# BACKEND_URL = "http://localhost:8000"  # For local testing without Docker

st.set_page_config(page_title="Salary & Loan Calculator", layout="wide")
st.title("💰 Advanced Salary & Loan Calculator")
st.write("Calculate your salary advances and loan repayments easily!")

# Salary Advance Section
with st.expander("Salary Advance Calculator", expanded=True):
    st.subheader("Enter Your Salary Details")
    col1, col2 = st.columns(2)
    with col1:
        salary = st.number_input("Gross Monthly Salary ($)", min_value=0.0, value=2000.0)
    with col2:
        frequency = st.selectbox("Pay Frequency", ["monthly", "weekly"], index=0)
    
    requested_advance = st.number_input("Requested Advance Amount ($)", min_value=0.0, value=500.0)
    
    if st.button("Calculate Advance", key="advance_btn"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate-advance",
                json={
                    "salary": salary,
                    "frequency": frequency,
                    "requested_advance": requested_advance
                }
            )
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("Advance Results")
                st.write(f"**Maximum Advance:** ${result['max_advance']:,.2f}")
                st.write(f"**Requested Amount:** ${result['requested']:,.2f}")
                
                if result['eligible']:
                    st.success("✅ You are eligible for this advance!")
                else:
                    st.error("❌ Not eligible - requested amount exceeds maximum.")
            else:
                st.error("Backend returned an error 😢")
        except Exception as e:
            st.error(f"Could not connect to the calculator service: {e}")

# Loan Calculator Section
with st.expander("Loan Calculator", expanded=True):
    st.subheader("Enter Loan Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        loan_amount = st.number_input("Loan Amount ($)", min_value=0.0, value=10000.0)
    with col2:
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0)
    with col3:
        loan_term = st.number_input("Loan Term (years)", min_value=1, value=3)
    
    if st.button("Calculate Loan", key="loan_btn"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate-loan",
                json={
                    "principal": loan_amount,
                    "rate": interest_rate,
                    "time": loan_term
                }
            )
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("Loan Results")
                st.write(f"**Total Repayable Amount:** ${result['total_amount']:,.2f}")
                st.write(f"**Total Interest:** ${result['total_amount'] - loan_amount:,.2f}")
                
                # Display Yearly Payment Schedule if present
                if 'schedule' in result:
                    st.subheader("Yearly Payment Schedule")
                    
                    # Table View - Changed to Yearly
                    for year_data in result['schedule']:
                        st.write(
                            f"Year {year_data['Year']}: "
                            f"Interest: ${year_data['Interest']:.2f}, "
                            f"Balance: ${year_data['Balance']:.2f}"
                        )
                    
                    # Optional: Show Chart - Changed to Yearly
                    if st.checkbox("Show as chart", key="loan_chart"):
                        df = pd.DataFrame(result['schedule'])
                        st.line_chart(df.set_index('Year')['Balance'])

            else:
                st.error("Backend returned an error 😢")
        except Exception as e:
            st.error(f"Could not connect to the calculator service: {e}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, FastAPI, Pandas, and Docker.")