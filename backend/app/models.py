from pydantic import BaseModel

class LoanRequest(BaseModel):
    principal: float
    rate: float
    time: int  # in years

class AdvanceRequest(BaseModel):
    salary: float
    frequency: str
    requested_advance: float