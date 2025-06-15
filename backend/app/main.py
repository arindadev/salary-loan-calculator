# 🚀 KEEP-ALIVE MAGIC (Prevents Render Free Tier Sleeping) 
import threading
import time
import requests
import os

def ping_server():
    """
    Ping our own backend every 10 minutes to keep it awake.
    Free Render services sleep after inactivity - this prevents that!
    """
    try:
        # Get current URL dynamically
        render_external_url = os.getenv("RENDER_EXTERNAL_URL")
        if render_external_url:
            requests.get(render_external_url)
            print(f"✅ Pinged {render_external_url} to stay awake!")
    except Exception as e:
        print(f"⚠️ Keep-alive ping failed: {str(e)}")
    
    # Repeat every 10 minutes (600 seconds)
    threading.Timer(600, ping_server).start()

# Start the keep-alive magic!
if __name__ == "__main__":
    ping_server()

# ========== ORIGINAL API CODE BELOW ==========
from fastapi import FastAPI
from .models import LoanRequest, AdvanceRequest
from .calculation import calculate_max_advance, calculate_loan_with_schedule

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Salary & Loan Calculator API is running!"}

@app.post("/calculate-loan")
def loan_calculator(loan: LoanRequest):
    total_amount, schedule_df = calculate_loan_with_schedule(
        principal=loan.principal,
        rate=loan.rate,
        time=loan.time
    )
    return {
        "total_amount": total_amount,
        "schedule": schedule_df.to_dict(orient='records')
    }

@app.post("/calculate-advance")
def advance_calculator(advance: AdvanceRequest):
    max_amount = calculate_max_advance(advance.salary, advance.frequency)
    eligible = advance.requested_advance <= max_amount
    return {
        "eligible": eligible,
        "max_advance": max_amount,
        "requested": advance.requested_advance
    }