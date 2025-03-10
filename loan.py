import streamlit as st
import pandas as pd

# Title of the app
st.title("Loan Management System")

# File upload widget
uploaded_file = st.file_uploader("Upload Loan Data CSV", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataframe
    st.subheader("Loan Data Overview")
    st.write(df.head())

    # Display summary statistics for numerical columns
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Add loan calculation options
    st.sidebar.header("Loan Management")
    action = st.sidebar.selectbox("Select Action", ("View Loan Details", "Loan Calculations"))

    if action == "View Loan Details":
        # Allow the user to filter loans based on loan status or other criteria
        loan_status = st.sidebar.selectbox("Select Loan Status", df["Loan Status"].unique())
        filtered_df = df[df["Loan Status"] == loan_status]
        st.write(filtered_df)
        
    elif action == "Loan Calculations":
        # Allow user to select a loan
        loan_id = st.sidebar.selectbox("Select Loan ID", df["Loan ID"].unique())
        selected_loan = df[df["Loan ID"] == loan_id]

        if not selected_loan.empty:
            principal = selected_loan["Loan Amount"].values[0]
            interest_rate = selected_loan["Interest Rate"].values[0] / 100
            term_years = selected_loan["Loan Term (Years)"].values[0]

            # Loan calculation: EMI Calculation (Equated Monthly Installment)
            monthly_interest_rate = interest_rate / 12
            number_of_months = term_years * 12
            emi = (principal * monthly_interest_rate * (1 + monthly_interest_rate)**number_of_months) / ((1 + monthly_interest_rate)**number_of_months - 1)

            # Display EMI and other details
            st.write(f"Loan ID: {loan_id}")
            st.write(f"Principal Amount: {principal}")
            st.write(f"Annual Interest Rate: {interest_rate * 100}%")
            st.write(f"Loan Term: {term_years} Years")
            st.write(f"EMI: {emi:.2f}")
        
        else:
            st.warning("Loan ID not found in the dataset.")

else:
    st.info("Please upload a CSV file containing loan data.")
