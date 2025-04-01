# Churn Shield - Telecom Customer Churn Prediction App

![App Screenshot](App.jpg)

Churn Shield is a Streamlit-based web application that predicts customer churn for telecom companies. It helps businesses identify customers who are likely to cancel their services, enabling proactive retention strategies.

## Features

- **Two Prediction Modes**:
  - **Online Prediction**: Input individual customer data through a form
  - **Batch Prediction**: Upload CSV files for bulk predictions

- **User Management**:
  - Secure login/registration system
  - Password hashing for security
  - MySQL database integration

- **Advanced Features**:
  - Churn probability scores
  - Reason analysis for potential churn
  - Data visualization (pie charts)
  - Downloadable prediction results

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: Scikit-learn
- **Database**: MySQL
- **Libraries**:
  - Pandas, NumPy for data processing
  - Joblib for model persistence
  - Matplotlib for visualization
  - mysql-connector for database operations

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/churn-shield.git
   cd churn-shield



Install dependencies:

bash
Copy
pip install -r requirements.txt
Set up MySQL database:

Create a database named Churn_User_Management

Create a table named users with columns: username (VARCHAR), password (VARCHAR)

Configure database credentials in user_management.py and preprocessing.py

Run the application:

bash
Copy
streamlit run app.py
Usage
Register a new account or login with existing credentials

Choose prediction mode (Online or Batch)

For Online mode:

Fill in customer details

Click "Predict" to get churn probability

For Batch mode:

Upload a CSV file with customer data

Download prediction results

File Structure
Copy
churn-shield/
├── app.py               # Main application file
├── user_management.py   # User authentication logic
├── preprocessing.py     # Data preprocessing functions
├── notebook/
│   └── model.sav        # Trained ML model
├── App.jpg              # Application screenshot
├── requirements.txt     # Python dependencies
└── README.md            # This file
Requirements
Python 3.7+

MySQL Server

Libraries listed in requirements.txt

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Co
