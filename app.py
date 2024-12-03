# Importing necessary libraries
import streamlit as st 
import pandas as pd
from joblib import load
import numpy as np  # Ensure NumPy is imported for predictions

# Filter warnings
import warnings
warnings.filterwarnings('ignore')

# Load joblib model
try:
    Model = load('SleepDisorderModel.joblib')
except FileNotFoundError:
    st.error("Model file not found. Please upload the 'SleepDisorderModel.joblib' file.")

# Title for the App
st.title("Sleep Disorder Classification App")

# UI for input details
st.header("Enter the details below:")

# Input fields for user data
person_id = st.text_input("Person ID:")
gender = st.selectbox("Gender:", ("Male", "Female"))
age = st.number_input("Age (in years):", step=1, format="%d")
occupation = st.text_input("Occupation:")
sleep_duration = st.number_input("Sleep Duration (in hours):", format="%.2f")
quality_of_sleep = st.slider("Quality of Sleep (1-10):", min_value=1, max_value=10, step=1)
physical_activity = st.selectbox("Physical Activity Level:", ("Low", "Medium", "High"))
stress_level = st.slider("Stress Level (1-10):", min_value=1, max_value=10, step=1)
bmi_category = st.selectbox("BMI Category:", ("Underweight", "Normal", "Overweight", "Obesity"))
blood_pressure = st.number_input("Blood Pressure (in mmHg):", format="%.2f")
heart_rate = st.number_input("Heart Rate (in bpm):", step=1, format="%d")
daily_steps = st.number_input("Daily Steps:", step=1, format="%d")

# Map categorical variables to numeric values (if necessary for the model)
gender_map = {"Male": 0, "Female": 1}
physical_activity_map = {"Low": 0, "Medium": 1, "High": 2}
bmi_category_map = {"Underweight": 0, "Normal": 1, "Overweight": 2, "Obesity": 3}

# Convert inputs to numeric values
gender_numeric = gender_map[gender]
physical_activity_numeric = physical_activity_map[physical_activity]
bmi_category_numeric = bmi_category_map[bmi_category]

# Prediction button
if st.button("Classify Sleep Disorder"):
    # Prepare input as a 2D array
    input_features = np.array([[gender_numeric, age, sleep_duration, quality_of_sleep,
                                 physical_activity_numeric, stress_level, bmi_category_numeric,
                                 blood_pressure, heart_rate, daily_steps]])

    # Perform prediction
    try:
        prediction = Model.predict(input_features)

        # Display result
        st.header("Prediction Result")
        if prediction[0] == 0:
            st.success("The person has no sleep disorder.")
        elif prediction[0] == 1:
            st.warning("The person is likely experiencing Insomnia.")
        else:
            st.error("The person is likely experiencing Sleep Apnea.")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
