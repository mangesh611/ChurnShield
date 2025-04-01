import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import mysql.connector
from mysql.connector import Error
import os

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='churn_prediction_db'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def preprocess(df, option):
    # Store customerID if it exists
    customer_ids = df['customerID'].copy() if 'customerID' in df.columns else None
    
    def binary_map(feature):
        return feature.map({'Yes':1, 'No':0})

    binary_list = ['SeniorCitizen','Dependents', 'PhoneService', 'PaperlessBilling']
    df[binary_list] = df[binary_list].apply(binary_map)

    if option == "Online":
        columns = ['SeniorCitizen', 'Dependents', 'tenure', 'PhoneService', 'PaperlessBilling', 
                 'MonthlyCharges', 'TotalCharges', 'MultipleLines_No_phone_service', 
                 'MultipleLines_Yes', 'InternetService_Fiber_optic', 'InternetService_No', 
                 'OnlineSecurity_No_internet_service', 'OnlineSecurity_Yes', 
                 'OnlineBackup_No_internet_service', 'TechSupport_No_internet_service', 
                 'TechSupport_Yes', 'StreamingTV_No_internet_service', 'StreamingTV_Yes', 
                 'StreamingMovies_No_internet_service', 'StreamingMovies_Yes', 
                 'Contract_One_year', 'Contract_Two_year', 'PaymentMethod_Electronic_check']
        df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)
    elif option == "Batch":
        # Keep only necessary columns
        df = df[['SeniorCitizen','Dependents','tenure','PhoneService','MultipleLines',
                'InternetService','OnlineSecurity','OnlineBackup','TechSupport',
                'StreamingTV','StreamingMovies','Contract','PaperlessBilling',
                'PaymentMethod','MonthlyCharges','TotalCharges']]
        
        columns = ['SeniorCitizen', 'Dependents', 'tenure', 'PhoneService', 'PaperlessBilling', 
                 'MonthlyCharges', 'TotalCharges', 'MultipleLines_No_phone_service', 
                 'MultipleLines_Yes', 'InternetService_Fiber_optic', 'InternetService_No', 
                 'OnlineSecurity_No_internet_service', 'OnlineSecurity_Yes', 
                 'OnlineBackup_No_internet_service', 'TechSupport_No_internet_service', 
                 'TechSupport_Yes', 'StreamingTV_No_internet_service', 'StreamingTV_Yes', 
                 'StreamingMovies_No_internet_service', 'StreamingMovies_Yes', 
                 'Contract_One_year', 'Contract_Two_year', 'PaymentMethod_Electronic_check']
        df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)

    # Feature scaling
    sc = MinMaxScaler()
    df['tenure'] = sc.fit_transform(df[['tenure']])
    df['MonthlyCharges'] = sc.fit_transform(df[['MonthlyCharges']])
    df['TotalCharges'] = sc.fit_transform(df[['TotalCharges']])
    
    return df, customer_ids