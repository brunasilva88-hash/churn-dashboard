import pandas as pdimport streamlit as st
# Mapa que "traduz" os nomes do dataset IBM estendido# para os nomes clássicos que o dashboard usaCOLUMN_MAP = {    "Customer ID": "customerID",    "Gender": "gender",    "Senior Citizen": "SeniorCitizen",    "Married": "Partner",    "Dependents": "Dependents",    "Tenure in Months": "tenure",    "Phone Service": "PhoneService",    "Multiple Lines": "MultipleLines",    "Internet Service": "InternetService",    "Online Security": "OnlineSecurity",    "Online Backup": "OnlineBackup",    "Device Protection Plan": "DeviceProtection",    "Premium Tech Support": "TechSupport",    "Streaming TV": "StreamingTV",    "Streaming Movies": "StreamingMovies",    "Contract": "Contract",    "Paperless Billing": "PaperlessBilling",    "Payment Method": "PaymentMethod",    "Monthly Charge": "MonthlyCharges",    "Total Charges": "TotalCharges",    "Churn Label": "Churn",}

@st.cache_datadef load_data(path: str = "data/telco_churn.csv") -> pd.DataFrame:    # Lê o CSV (separado por vírgula)    df = pd.read_csv(path)
    # Renomeia as colunas para os nomes clássicos    df = df.rename(columns=COLUMN_MAP)
    # --- Ajustes de valores ---
    # SeniorCitizen: no seu arquivo vem "Yes"/"No" -> converte pra 1/0    if df["SeniorCitizen"].dtype == object:        df["SeniorCitizen"] = (            df["SeniorCitizen"].str.strip().str.lower().map({"yes": 1, "no": 0})        )
    # TotalCharges: garante que seja número (troca vazios por 0)    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    # MonthlyCharges: garante número    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce").fillna(0)
    # tenure: garante número inteiro    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").fillna(0).astype(int)
    # Churn: garante "Yes"/"No" limpos    df["Churn"] = df["Churn"].str.strip().str.capitalize()
    return df
