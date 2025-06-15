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