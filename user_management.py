import mysql.connector
from mysql.connector import Error
import hashlib

# Database configuration
db_config = {
    'user': 'root',       # Replace with your MySQL username
    'password': 'mangesh',   # Replace with your MySQL password
    'host': 'localhost',           # Replace with your MySQL host if necessary
    'database': 'Churn_User_Management',   # Replace with your database name
    'raise_on_warnings': True
}

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as err:
        print(f"Error: {err}")
        return None

def add_user(username, password):
    """Add a new user to the database."""
    hashed_password = hash_password(password)
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            connection.commit()
            return True
        except Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

def authenticate(username, password):
    """Authenticate a user."""
    hashed_password = hash_password(password)
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None and result[0] == hashed_password
        except Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

# Example usage:
# if __name__ == "__main__":
#     new_user = add_user('newuser', 'password123')
#     if new_user:
#         print("User added successfully.")
#     else:
#         print("Failed to add user.")

#     auth_user = authenticate('newuser', 'password123')
#     if auth_user:
#         print("User authenticated successfully.")
#     else:
#         print("Authentication failed.")