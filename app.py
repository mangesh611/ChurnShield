import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import joblib
import os
import matplotlib.pyplot as plt
from user_management import authenticate, add_user
from preprocessing import preprocess

def clear_session():
    """Clear session state while preserving needed variables"""
    st.session_state['logged_in'] = False
    st.session_state['is_registering'] = False
    st.session_state['registered'] = False

def main():
    st.title('CHURN SHIELD')

    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, 'App.jpg')

    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image)
    else:
        st.error(f"Image file not found at {image_path}")

    # Load the model
    model_path = os.path.join(current_dir, 'notebook', 'model.sav')
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        st.write("Model loaded successfully!")
    else:
        st.error(f"Model file not found at {model_path}")

    st.title('Telco Customer Churn Prediction App')
    st.markdown("""
     :dart:  This Streamlit app predicts customer churn in a fictional telecom use case.
     Works for both online and batch predictions.\n
    """)

    # Add logout button to sidebar
    if st.sidebar.button('Logout'):
        clear_session()
        st.rerun()

    add_selectbox = st.sidebar.selectbox("How would you like to predict?", ("Online", "Batch"))
    st.sidebar.info('This app predicts Customer Churn')
    st.sidebar.image(image)

    if add_selectbox == "Online":
        st.info("Input data below")
        st.subheader("Demographic data")
        seniorcitizen = st.selectbox('Senior Citizen:', ('Yes', 'No'))
        dependents = st.selectbox('Dependent:', ('Yes', 'No'))

        st.subheader("Payment data")
        tenure = st.slider('Number of months the customer has stayed with the company', min_value=0, max_value=72, value=0)
        contract = st.selectbox('Contract', ('Month-to-month', 'One year', 'Two year'))
        paperlessbilling = st.selectbox('Paperless Billing', ('Yes', 'No'))
        PaymentMethod = st.selectbox('PaymentMethod',('Electronic check', 'Mailed check', 'Bank transfer (automatic)','Credit card (automatic)'))
        monthlycharges = st.number_input('The amount charged to the customer monthly', min_value=0, max_value=150, value=0)
        totalcharges = st.number_input('The total amount charged to the customer',min_value=0, max_value=10000, value=0)

        st.subheader("Services signed up for")
        multiplelines = st.selectbox("Does the customer have multiple lines",('Yes','No','No phone service'))
        phoneservice = st.selectbox('Phone Service:', ('Yes', 'No'))
        internetservice = st.selectbox("Does the customer have internet service", ('DSL', 'Fiber optic', 'No'))
        onlinesecurity = st.selectbox("Does the customer have online security",('Yes','No','No internet service'))
        onlinebackup = st.selectbox("Does the customer have online backup",('Yes','No','No internet service'))
        techsupport = st.selectbox("Does the customer have technology support", ('Yes','No','No internet service'))
        streamingtv = st.selectbox("Does the customer stream TV", ('Yes','No','No internet service'))
        streamingmovies = st.selectbox("Does the customer stream movies", ('Yes','No','No internet service'))

        data = {
                'SeniorCitizen': seniorcitizen,
                'Dependents': dependents,
                'tenure': tenure,
                'PhoneService': phoneservice,
                'MultipleLines': multiplelines,
                'InternetService': internetservice,
                'OnlineSecurity': onlinesecurity,
                'OnlineBackup': onlinebackup,
                'TechSupport': techsupport,
                'StreamingTV': streamingtv,
                'StreamingMovies': streamingmovies,
                'Contract': contract,
                'PaperlessBilling': paperlessbilling,
                'PaymentMethod': PaymentMethod, 
                'MonthlyCharges': monthlycharges, 
                'TotalCharges': totalcharges
                }
        features_df = pd.DataFrame.from_dict([data])
        st.write('Overview of input is shown below')
        st.dataframe(features_df)

        # Preprocess inputs
        preprocess_df, _ = preprocess(features_df, 'Online')

        prediction = model.predict(preprocess_df)
        prediction_proba = model.predict_proba(preprocess_df)[0][1]

        if st.button('Predict'):
            if prediction == 1:
                st.warning(f'Yes, the customer will terminate the service. Probability: {prediction_proba:.2%}')
            else:
                st.success(f'No, the customer is happy with Telco Services. Probability: {1 - prediction_proba:.2%}')
    else:
        st.subheader("Dataset upload")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
                st.write("Data Preview:")
                st.dataframe(data.head())
                
                # Verify required columns
                required_cols = ['customerID','SeniorCitizen','Dependents','tenure',
                               'PhoneService','MultipleLines','InternetService',
                               'OnlineSecurity','OnlineBackup','TechSupport',
                               'StreamingTV','StreamingMovies','Contract',
                               'PaperlessBilling','PaymentMethod',
                               'MonthlyCharges','TotalCharges']
                
                missing_cols = [col for col in required_cols if col not in data.columns]
                if missing_cols:
                    st.error(f"Missing required columns: {', '.join(missing_cols)}")
                    return
                
                if st.button('Predict Churn'):
                    with st.spinner('Processing...'):
                        try:
                            # Preprocess data
                            preprocess_df, customer_ids = preprocess(data, "Batch")
                            
                            # Get predictions and probabilities
                            predictions = model.predict(preprocess_df)
                            probabilities = model.predict_proba(preprocess_df)[:, 1]
                            
                            # Create reasons for churn
                            reasons = []
                            for idx, row in data.iterrows():
                                reason_parts = []
                                if row['Contract'] == 'Month-to-month':
                                    reason_parts.append("Month-to-month contract")
                                if row['InternetService'] == 'Fiber optic' and row['OnlineSecurity'] == 'No':
                                    reason_parts.append("No online security")
                                if row['TechSupport'] == 'No' and row['TechSupport'] != 'No internet service':
                                    reason_parts.append("No tech support")
                                if row['MonthlyCharges'] > data['MonthlyCharges'].median():
                                    reason_parts.append("High monthly charges")
                                reasons.append(", ".join(reason_parts) if reason_parts else "Low risk profile")
                            
                            # Create results
                            results = pd.DataFrame({
                                'Customer ID': customer_ids,
                                'Will Churn?': ['Yes' if x == 1 else 'No' for x in predictions],
                                'Probability': [f"{prob:.2%}" for prob in probabilities],
                                'Reason': reasons
                            })
                            
                            st.success("Predictions completed!")
                            st.dataframe(results)
                            
                            # Pie chart visualization
                            st.subheader("Churn Distribution")
                            churn_counts = results['Will Churn?'].value_counts()
                            fig, ax = plt.subplots()
                            ax.pie(churn_counts, 
                                  labels=churn_counts.index, 
                                  autopct='%1.1f%%',
                                  colors=['#ff9999','#66b3ff'],
                                  startangle=90)
                            ax.axis('equal')
                            st.pyplot(fig)
                            
                            # Download button
                            csv = results.to_csv(index=False)
                            st.download_button(
                                "Download Predictions",
                                csv,
                                "churn_predictions.csv",
                                "text/csv",
                                key='download-csv'
                            )
                            
                        except Exception as e:
                            st.error(f"Prediction failed: {str(e)}")
                            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

def register():
    st.title("User Registration")
    new_username = st.text_input("Enter a username")
    new_password = st.text_input("Enter a password", type="password")

    if st.button("Register"):
        if new_username and new_password:
            success = add_user(new_username, new_password)
            if success:
                st.session_state['registered'] = True
                st.session_state['is_registering'] = False
                st.success("You have successfully registered!")
                st.rerun()
            else:
                st.warning("Username already exists. Please choose a different one.")
        else:
            st.warning("Please fill out all fields.")
    
    if st.button("Back to Login"):
        st.session_state['is_registering'] = False
        st.rerun()

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Username or password is incorrect")
    
    with col2:
        if st.button("Register here"):
            st.session_state['is_registering'] = True
            st.rerun()

if __name__ == '__main__':
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'is_registering' not in st.session_state:
        st.session_state['is_registering'] = False
    if 'registered' not in st.session_state:
        st.session_state['registered'] = False

    if st.session_state['is_registering']:
        register()
    elif st.session_state['logged_in']:
        main()
    elif st.session_state['registered']:
        st.session_state['registered'] = False
        login()
    else:
        login()