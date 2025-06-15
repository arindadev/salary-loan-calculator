import streamlit as st
import requests
import pandas as pd
import os
from streamlit_confetti import confetti  # 🎉 Confetti magic!

# ========== DARK MODE TOGGLE ==========
st.set_page_config(page_title="Money Wizard", page_icon="🧙", layout="wide")
if st.button("🌙 Toggle Dark/Light Mode", key="dark_mode"):
    current_theme = st.get_theme()
    new_theme = "light" if current_theme["base"] == "dark" else "dark"
    st.set_theme(new_theme)
    st.rerun()

# ========== HEADER ==========
st.title("💰 Advanced Salary & Loan Calculator")
st.image("https://cdn-icons-png.flaticon.com/512/477/477103.png", width=100)
st.write("Calculate your salary advances and loan repayments easily!")

# Get backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    st.error("❌ BACKEND_URL environment variable not set!")
    st.stop()

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
                    confetti()  # 🎉 CONFETTI!
                else:
                    st.error("❌ Not eligible - requested amount exceeds maximum.")
            else:
                st.error(f"Backend error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect: {e}")

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
                confetti()  # 🎉 CONFETTI FOR LOANS TOO!
                
                # Display Yearly Payment Schedule
                if 'schedule' in result:
                    st.subheader("Yearly Payment Schedule")
                    
                    # Table View
                    for year_data in result['schedule']:
                        st.write(
                            f"Year {year_data['Year']}: "
                            f"Interest: ${year_data['Interest']:.2f}, "
                            f"Balance: ${year_data['Balance']:.2f}"
                        )
                    
                    # Show Chart
                    if st.checkbox("Show as chart", key="loan_chart"):
                        df = pd.DataFrame(result['schedule'])
                        st.line_chart(df.set_index('Year')['Balance'])
                    
                    # 📥 DOWNLOAD BUTTON
                    import io
                    buffer = io.BytesIO()
                    df = pd.DataFrame(result['schedule'])
                    df.to_csv(buffer, index=False)
                    buffer.seek(0)
                    
                    st.download_button(
                        label="📥 Download Full Report",
                        data=buffer,
                        file_name="loan_schedule.csv",
                        mime="text/csv"
                    )

            else:
                st.error(f"Backend error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect: {e}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, FastAPI, Pandas, and Docker")