# -------------------------------
# Import required libraries
# -------------------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from typing import Optional
import os

# -------------------------------
# Initialize FastAPI application
# -------------------------------

app = FastAPI(title="Local Excel IVR API")

EXCEL_FILE = "IVR_Agentic_POC_Sample_Data.xlsx"

# -------------------------------
# Column order (used if Excel is missing)
# -------------------------------

COLUMNS = [
    "Call_ID",
    "Customer_Name",
    "Phone_Number",
    "Policy_Number",
    "Question_Asked",
    "Customer_Response",
    "Response_Type",
    "Call_Status",
    "Confidence_Score",
    "Agent_Action_Required"
]

# =========================================================
# DATA MODELS
# =========================================================

class CallRecord(BaseModel):
    """Full record used for POST and PUT"""
    Call_ID: int
    Customer_Name: str
    Phone_Number: str
    Policy_Number: str
    Question_Asked: str
    Customer_Response: str
    Response_Type: str
    Call_Status: str
    Confidence_Score: float = Field(ge=0, le=1)
    Agent_Action_Required: str


class CallUpdate(BaseModel):
    """Partial update model used for PATCH"""
    Customer_Response: Optional[str] = None
    Call_Status: Optional[str] = None
    Confidence_Score: Optional[float] = Field(default=None, ge=0, le=1)
    Agent_Action_Required: Optional[str] = None

# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def read_excel_df() -> pd.DataFrame:
    """
    Reads Excel into DataFrame.
    Creates empty Excel if missing.
    """
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(EXCEL_FILE, index=False)
        return df

    return pd.read_excel(EXCEL_FILE)


def write_excel_df(df: pd.DataFrame):
    """Writes DataFrame back to Excel"""
    df.to_excel(EXCEL_FILE, index=False)

# =========================================================
# READ ALL
# =========================================================

@app.get("/calls")
def get_all_calls():
    """Fetch all call records"""
    df = read_excel_df()
    return df.to_dict(orient="records")

# =========================================================
# READ BY ID
# =========================================================

@app.get("/calls/{call_id}")
def get_call_by_id(call_id: int):
    """Fetch call record by Call_ID"""
    df = read_excel_df()

    if call_id not in df["Call_ID"].values:
        raise HTTPException(status_code=404, detail="Call_ID not found")

    return df[df["Call_ID"] == call_id].iloc[0].to_dict()

# =========================================================
# CREATE (NO DUPLICATES)
# =========================================================

@app.post("/calls")
def create_call(record: CallRecord):
    """Create a new call record (unique Call_ID)"""
    df = read_excel_df()

    if record.Call_ID in df["Call_ID"].values:
        raise HTTPException(
            status_code=400,
            detail=f"Call_ID {record.Call_ID} already exists"
        )

    df = pd.concat([df, pd.DataFrame([record.dict()])], ignore_index=True)
    write_excel_df(df)

    return {"message": "Call record created", "Call_ID": record.Call_ID}

# =========================================================
# UPSERT (PUT)
# =========================================================

@app.put("/calls/{call_id}")
def upsert_call(call_id: int, record: CallRecord):
    """
    Replace existing record or insert new one.
    Ensures URL Call_ID and body Call_ID match.
    """
    if call_id != record.Call_ID:
        raise HTTPException(
            status_code=400,
            detail="Call_ID in URL and body must match"
        )

    df = read_excel_df()

    # Remove old record if exists
    df = df[df["Call_ID"] != call_id]

    df = pd.concat([df, pd.DataFrame([record.dict()])], ignore_index=True)
    write_excel_df(df)

    return {"message": "Call record upserted", "Call_ID": call_id}

# =========================================================
# PARTIAL UPDATE (PATCH)
# =========================================================

@app.patch("/calls/{call_id}")
def update_call(call_id: int, update: CallUpdate):
    """Update selected fields of a call record"""
    df = read_excel_df()

    if call_id not in df["Call_ID"].values:
        raise HTTPException(status_code=404, detail="Call_ID not found")

    for field, value in update.dict(exclude_unset=True).items():
        df.loc[df["Call_ID"] == call_id, field] = value

    write_excel_df(df)

    return {"message": f"Call_ID {call_id} updated successfully"}

# =========================================================
# DELETE
# =========================================================

@app.delete("/calls/{call_id}")
def delete_call(call_id: int):
    """Delete a call record"""
    df = read_excel_df()

    if call_id not in df["Call_ID"].values:
        raise HTTPException(status_code=404, detail="Call_ID not found")

    df = df[df["Call_ID"] != call_id]
    write_excel_df(df)

    return {"message": f"Call_ID {call_id} deleted"}
