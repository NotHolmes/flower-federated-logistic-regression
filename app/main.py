from typing import Union
from fastapi import FastAPI
import uvicorn
import joblib
import pandas as pd
from src.utils import CREDIT_SCORE_CLASSES, scale_data

app = FastAPI()
model = joblib.load("model/model_fedavg.joblib")
model_trim = joblib.load("model/model_fedtrimmedavg.joblib")
model_krum = joblib.load("model/model_krum.joblib")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict_credit_score(data: dict):
    
    data = data_to_pred(data)
    
    scale_data(pd.DataFrame(data), pd.DataFrame(data))
    prediction = model.predict(data)[0]
    prediction_trim = model_trim.predict(data)[0]
    prediction_krum = model_krum.predict(data)[0]
    
    probability = max(model.predict_proba(data)[0])
    probability_trim = max(model_trim.predict_proba(data)[0])
    probability_krum = max(model_krum.predict_proba(data)[0])
    
    return {
        "prediction": CREDIT_SCORE_CLASSES[prediction],
        "prediction_trim": CREDIT_SCORE_CLASSES[prediction_trim],
        "prediction_krum": CREDIT_SCORE_CLASSES[prediction_krum],
        "probability": probability,
        "probability_trim": probability_trim,
        "probability_krum": probability_krum
    }

def data_to_pred(data: dict):
    pred = {
    'Age': data['Age'],
    'Annual_Income': data['Annual_Income'],
    'Monthly_Inhand_Salary': data['Monthly_Inhand_Salary'],
    'Num_Bank_Accounts': data['Num_Bank_Accounts'],
    'Num_Credit_Card': data['Num_Credit_Card'],
    'Interest_Rate': data['Interest_Rate'],
    'Num_of_Loan': data['Num_of_Loan'],
    'Delay_from_due_date': data['Delay_from_due_date'],
    'Num_of_Delayed_Payment': data['Num_of_Delayed_Payment'],
    'Changed_Credit_Limit': data['Changed_Credit_Limit'],
    'Num_Credit_Inquiries': data['Num_Credit_Inquiries'],
    'Credit_Mix': data['Credit_Mix'],
    'Outstanding_Debt': data['Outstanding_Debt'],
    'Credit_Utilization_Ratio': data['Credit_Utilization_Ratio'],
    'Credit_History_Age': data['Credit_History_Age'],
    'Total_EMI_per_month': data['Total_EMI_per_month'],
    'Amount_invested_monthly': data['Amount_invested_monthly'],
    'Monthly_Balance': data['Monthly_Balance'],
    'Credit-Builder Loan': 'Credit-Builder Loan' in data['Type_of_Loan'],
    'Personal Loan': 'Personal Loan' in data['Type_of_Loan'],
    'Debt Consolidation Loan': 'Debt Consolidation Loan' in data['Type_of_Loan'],
    'Student Loan': 'Student Loan' in data['Type_of_Loan'],
    'Payday Loan': 'Payday Loan' in data['Type_of_Loan'],
    'Mortgage Loan': 'Mortgage Loan' in data['Type_of_Loan'],
    'Auto Loan': 'Auto Loan' in data['Type_of_Loan'],
    'Home Equity Loan': 'Home Equity Loan' in data['Type_of_Loan'],
    'Month_August': data['Month'] == 'August',
    'Month_February': data['Month'] == 'February',
    'Month_January': data['Month'] == 'January',
    'Month_July': data['Month'] == 'July',
    'Month_June': data['Month'] == 'June',
    'Month_March': data['Month'] == 'March',
    'Month_May': data['Month'] == 'May',
    'Occupation_Architect': data['Occupation'] == 'Architect',
    'Occupation_Developer': data['Occupation'] == 'Developer',
    'Occupation_Doctor': data['Occupation'] == 'Doctor',
    'Occupation_Engineer': data['Occupation'] == 'Engineer',
    'Occupation_Entrepreneur': data['Occupation'] == 'Entrepreneur',
    'Occupation_Journalist': data['Occupation'] == 'Journalist',
    'Occupation_Lawyer': data['Occupation'] == 'Lawyer',
    'Occupation_Manager': data['Occupation'] == 'Manager',
    'Occupation_Mechanic': data['Occupation'] == 'Mechanic',
    'Occupation_Media_Manager': data['Occupation'] == 'Media Manager',
    'Occupation_Musician': data['Occupation'] == 'Musician',
    'Occupation_Scientist': data['Occupation'] == 'Scientist',
    'Occupation_Teacher': data['Occupation'] == 'Teacher',
    'Occupation_Writer': data['Occupation'] == 'Writer',
    'Occupation________': data['Occupation'] == '________',
    'Payment_of_Min_Amount_Yes': data['Payment_of_Min_Amount'],
    'Payment_Behaviour_High_spent_Medium_value_payments': 'High_spent_Medium_value_payments' in data['Payment_Behaviour'],
    'Payment_Behaviour_High_spent_Small_value_payments': 'High_spent_Small_value_payments' in data['Payment_Behaviour'],
    'Payment_Behaviour_Low_spent_Large_value_payments': 'Low_spent_Large_value_payments' in data['Payment_Behaviour'],
    'Payment_Behaviour_Low_spent_Medium_value_payments': 'Low_spent_Medium_value_payments' in data['Payment_Behaviour'],
    'Payment_Behaviour_Low_spent_Small_value_payments': 'Low_spent_Small_value_payments' in data['Payment_Behaviour'],
    }
    
    return pd.DataFrame([pred])
    

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)