import pandas as pd

def calculate_max_advance(salary: float, frequency: str) -> float:
    freq = frequency.lower()
    if salary <= 0:
        raise ValueError("Salary must be greater than zero.")
    if freq == "monthly":
        return round(salary * 0.5, 2)
    elif freq == "weekly":
        return round(salary * 2, 2)
    else:
        raise ValueError("Frequency must be 'monthly' or 'weekly'.")

def calculate_loan_with_schedule(principal: float, rate: float, time: int):
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    if time <= 0:
        raise ValueError("Time period must be greater than zero.")
    
    # Simple yearly compounding (not monthly)
    total_amount = principal * (1 + rate/100) ** time
    
    # Create yearly schedule
    schedule_data = []
    for year in range(1, time + 1):
        balance = principal * (1 + rate/100) ** year
        interest = balance - (principal * (1 + rate/100) ** (year-1)) if year > 1 else balance - principal
        
        schedule_data.append({
            'Year': year,
            'Interest': round(interest, 2),
            'Balance': round(balance, 2)
        })
    
    return round(total_amount, 2), pd.DataFrame(schedule_data)