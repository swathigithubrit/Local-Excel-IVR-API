🔹 Project Overview

This project demonstrates a fully local REST API built with FastAPI to read, write, update, and delete call records stored in an Excel file.
It simulates an IVR call log system where each call has a unique Call_ID and multiple attributes such as customer name, phone number, policy details, response type, and confidence score.

✅ The entire system runs locally — no cloud, no server required.

Key Features:

CRUD operations on Excel data:

Create new call records (POST)

Read all records or a specific record (GET)

Update partially (PATCH) or completely (PUT)

Delete records (DELETE)

Duplicate prevention for Call_ID

Validation of Confidence_Score (0–1) and mandatory fields

Handles missing Excel file by creating it automatically

Swagger UI available for testing: http://127.0.0.1:8000/docs

Fully offline — Excel remains local, API runs on your machine

🔹 Project Structure
Excel_API_Project/
├─ main.py                 # FastAPI application code
├─ IVR_Agentic_POC_Sample_Data.xlsx   # Excel file storing call records
└─ README.md               # Project documentation


Install Python libraries

pip install fastapi uvicorn pandas openpyxl


Run the API

uvicorn main:app --reload


Open Swagger UI

http://127.0.0.1:8000/docs


Use this UI to test all endpoints (GET, POST, PUT, PATCH, DELETE)

🔹 API Endpoints
| Endpoint           | Method | Description                    |
| ------------------ | ------ | ------------------------------ |
| `/calls`           | GET    | Read all call records          |
| `/calls/{call_id}` | GET    | Read a specific call record    |
| `/calls`           | POST   | Create a new call record       |
| `/calls/{call_id}` | PUT    | Replace a call record (upsert) |
| `/calls/{call_id}` | PATCH  | Partially update a call record |
| `/calls/{call_id}` | DELETE | Delete a call record           |


🔹 Example Call Record
{
  "Call_ID": 1003,
  "Customer_Name": "Suresh Reddy",
  "Phone_Number": "9XXXXXXXX3",
  "Policy_Number": "POL54321",
  "Question_Asked": "Claim Status",
  "Customer_Response": "Pending",
  "Response_Type": "Voice",
  "Call_Status": "In Progress",
  "Confidence_Score": 0.78,
  "Agent_Action_Required": "Yes"
}

🔹 Features & Corner Cases Handled
| Scenario                      | Handled                 |
| ----------------------------- | ----------------------- |
| Duplicate `Call_ID` on create | ❌ Rejected with 400     |
| Update non-existing `Call_ID` | ❌ Returns 404           |
| Partial update                | ✅ PATCH allowed         |
| Replace record completely     | ✅ PUT allowed           |
| Delete missing `Call_ID`      | ❌ Returns 404           |
| Confidence score validation   | ✅ 0–1 enforced          |
| Excel missing                 | ✅ Automatically created |

🔹 How It Works

FastAPI acts as a REST API backend.

Pandas reads/writes Excel.

Endpoints interact with Excel locally, returning JSON responses.

Data is validated with Pydantic models.

Supports full CRUD operations safely and efficiently.

Architecture:

Client (Browser/Postman/Swagger UI)
        ↓
   FastAPI Backend
        ↓
   Excel File (Local Storage)

🔹 Demo / Testing

Start server:

uvicorn main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs


Test endpoints:

POST /calls → add new record

GET /calls → view all records

PATCH /calls/{id} → update partial fields

PUT /calls/{id} → replace record

DELETE /calls/{id} → remove record
