import numpy as np
import pickle
import joblib
import pandas as pd
import os

# Load the model
loaded_model = joblib.load("D:\\codecraft essentials\\sayooj\\stroke_backend\\stroke\\ml_model\\decision_tree_model.pkl")

# Load the scaler
SCALER_PATH = "D:\codecraft essentials\sayooj\scaler.pkl"

# Check if file exists
if os.path.exists(SCALER_PATH):
    print(f"Scaler file found at: {SCALER_PATH}")
    print(f"File size: {os.path.getsize(SCALER_PATH)} bytes")
    
    try:
        with open(SCALER_PATH, "rb") as scaler_file:
            scaler = pickle.load(scaler_file)
            print("Scaler loaded successfully.")
    except Exception as e:
        print(f"Failed to load scaler: {e}")
else:
    print(f"Scaler file not found at: {SCALER_PATH}")
    scaler = None

def predict_stroke(data):
    gender_map = {'Male': 0, 'Female': 1}
    work_type_map = {'Private': 0, 'Self-employed': 1, 'children': 2, 'Govt_job': 3, 'Never_worked': 4}
    residence_map = {'Urban': 0, 'Rural': 1}
    smoking_map = {'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3}

    # Convert input dictionary into numerical form
    user_data = np.array([[gender_map[data["gender"]],
                           float(data["age"]),
                           int(data["hypertension"]),
                           int(data["heart_disease"]),
                           1 if data["ever_married"] == "Yes" else 0,
                           work_type_map[data["work_type"]],
                           residence_map[data["residence_type"]],
                           float(data["avg_glucose_level"]),
                           float(data["bmi"]),
                           smoking_map[data["smoking_status"]]]])

    # Feature names
    feature_names = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 
                     'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']

    # Convert user data to DataFrame
    df_user_data = pd.DataFrame(user_data, columns=feature_names)
    
    # Create a copy of the data before scaling
    print("Original User Data:")
    print(df_user_data)
    
    # Scale only avg_glucose_level and bmi columns
    if scaler is not None:
        try:
            # Create a separate DataFrame with just the columns the scaler was trained on
            columns_to_scale = ['avg_glucose_level', 'bmi']
            scaling_df = df_user_data[columns_to_scale].copy()
            
            # Try to transform using the scaler
            scaled_values = scaler.transform(scaling_df)
            
            # Update the original DataFrame with the scaled values
            df_user_data[columns_to_scale] = scaled_values
            
            print("Data scaled successfully!")
        except Exception as e:
            print(f"Error during scaling: {e}")
            # If scaling fails, continue with unscaled data
    else:
        print("Warning: Scaler not loaded. Using unscaled data.")

    # Debugging print statement
    print("Processed User Data (after scaling):")
    print(df_user_data)
    
    # Make prediction
    prediction = loaded_model.predict(df_user_data)
    return prediction[0]