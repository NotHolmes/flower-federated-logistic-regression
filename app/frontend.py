import streamlit as st
import requests

st.set_page_config(page_title="Page Title", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.title("Credit Scoring Prediction")

# Input fields - Part 1
col1, col2 = st.columns(2) 
with col1:
    month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    age = st.number_input("Age", min_value=18, max_value=100)

with col2:
    occupation = st.selectbox("Occupation", ["Architect", "Developer", "Doctor", "Engineer", "Entrepreneur", "Journalist", "Lawyer", "Manager", "Mechanic", "Media Manager", "Musician", "Scientist", "Teacher", "Writer", "Others"])
    if occupation == "Others":
        occupation = "________"

# Input fields - Part 2
col3, col4 = st.columns(2)
with col3: 
    annual_income = st.number_input("Annual Income")
    monthly_inhand_salary = st.number_input("Monthly Inhand Salary")
    num_bank_accounts = st.number_input("Number of Bank Accounts", min_value=0)

with col4:
    num_credit_card = st.number_input("Number of Credit Cards", min_value=0)
    interest_rate = st.slider("Interest Rate (%)", min_value=0, max_value=100) 
    num_of_loan = st.number_input("Number of Loans", min_value=0)

# Input fields - Part 3 
col5, col6 = st.columns(2)
with col5:
    delay_from_due_date = st.number_input("Days Delayed from Due Date", min_value=0)
    num_of_delayed_payment = st.number_input("Number of Delayed Payments", min_value=0)
    changed_credit_limit = st.number_input("Change in Credit Limit")

with col6:
    num_credit_inquiries = st.number_input("Number of Credit Inquiries")
    credit_mix = st.number_input("Credit Mix")  
    outstanding_debt = st.number_input("Outstanding Debt")

# Input fields - Part 4
col7, col8 = st.columns(2)
with col7:
    credit_utilization_ratio = st.number_input("Credit Utilization Ratio")
    credit_history_age = st.number_input("Credit History Age (e.g., '15 months')", min_value=0) 
    payment_of_min_amount = st.selectbox("Payment of Minimum Amount", ["No", "Yes"])
    payment_of_min_amount = 1 if payment_of_min_amount == "Yes" else 0

with col8: 
    total_emi_per_month = st.number_input("Total EMI per Month")
    amount_invested_monthly = st.number_input("Amount Invested Monthly")
    payment_behavior = st.selectbox("Payment Behaviour", ["Low_spent_Large_value_payments", "Low_spent_Medium_value_payments", "Low_spent_Small_value_payments", "High_spent_Large_value_payments", "High_spent_Medium_value_payments", "High_spent_Small_value_payments"])

# Input fields - Part 5  
monthly_balance = st.number_input("Monthly Balance")

st.header("Type of Loan Customer Has Taken")
type_of_loan_personal = st.checkbox("Personal Loan")
type_of_loan_home = st.checkbox("Home Loan")
type_of_loan_car = st.checkbox("Car Loan")
type_of_loan_education = st.checkbox("Education Loan")
type_of_loan_business = st.checkbox("Business Loan")

selected_loans = []
if type_of_loan_personal:
    selected_loans.append("Personal Loan")
if type_of_loan_home:
    selected_loans.append("Home Loan")
if type_of_loan_car:
    selected_loans.append("Car Loan")
if type_of_loan_education:
    selected_loans.append("Education Loan")
if type_of_loan_business:
    selected_loans.append("Business Loan")

type_of_loan = ", ".join(selected_loans)

if st.button("Send to API"):
    # Construct the input data as a dictionary
    input_data = {
        "Month": month,
        "Age": age,
        "Occupation": occupation,
        "Annual_Income": annual_income,
        "Monthly_Inhand_Salary": monthly_inhand_salary,
        "Num_Bank_Accounts": num_bank_accounts,
        "Num_Credit_Card": num_credit_card,
        "Interest_Rate": interest_rate,
        "Num_of_Loan": num_of_loan,
        "Delay_from_due_date": delay_from_due_date,
        "Num_of_Delayed_Payment": num_of_delayed_payment,
        "Changed_Credit_Limit": changed_credit_limit,
        "Num_Credit_Inquiries": num_credit_inquiries,
        "Credit_Mix": credit_mix,
        "Outstanding_Debt": outstanding_debt,
        "Credit_Utilization_Ratio": credit_utilization_ratio,
        "Credit_History_Age": credit_history_age,
        "Payment_of_Min_Amount": payment_of_min_amount,
        "Total_EMI_per_month": total_emi_per_month,
        "Amount_invested_monthly": amount_invested_monthly,
        "Payment_Behaviour": payment_behavior,
        "Monthly_Balance": monthly_balance,
        "Type_of_Loan": type_of_loan
    }

    # Send the data as JSON
    response = requests.post("http://localhost:8000/predict", json=input_data)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['prediction']}")
    else:
        st.error("Failed to send data to API")
