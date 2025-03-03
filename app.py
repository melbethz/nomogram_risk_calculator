import streamlit as st
import simpleNomo
import pandas as pd
import matplotlib.pyplot as plt
import math

# Title and description of the app
st.title("Bleeding Risk Nomogram and Calculator")
st.write("This tool calculates your risk for postoperative bleeding after TURBT and displays a nomogram for visualization.")

# --- Risk Calculator Section ---
st.header("Risk Calculator")
st.write("Enter the following parameters to calculate your risk:")

# HAS-BLED Score slider with discrete integer steps (0,1,...,9)
has_bled = st.slider("HAS-BLED Score", min_value=0, max_value=9, value=5, step=1)

# Binary inputs for other predictors
alcohol = st.radio("High-risk Alcohol Consumption?", options=["No", "Yes"])
alcohol_val = 1 if alcohol == "Yes" else 0

pait = st.radio("Platelet Aggregation Inhibitor Therapy?", options=["No", "Yes"])
pait_val = 1 if pait == "Yes" else 0

oact = st.radio("Oral Anticoagulation Therapy?", options=["No", "Yes"])
oact_val = 1 if oact == "Yes" else 0

bridging = st.radio("Perioperative Bridging Therapy?", options=["No", "Yes"])
bridging_val = 1 if bridging == "Yes" else 0

# Calculate risk when the button is clicked
if st.button("Calculate Risk"):
    # Logistic regression coefficients (from your model)
    intercept = -3.7634
    coef_hasbled = 0.0284
    coef_alcohol = 0.9575
    coef_pait = 1.0074
    coef_oact = 0.5272
    coef_bridging = 1.0557

    # Calculate the linear predictor (log-odds)
    linear_pred = (intercept +
                   coef_hasbled * has_bled +
                   coef_alcohol * alcohol_val +
                   coef_pait * pait_val +
                   coef_oact * oact_val +
                   coef_bridging * bridging_val)

    # Convert log-odds to probability
    risk = 1 / (1 + math.exp(-linear_pred))

    st.subheader(f"Estimated Bleeding Risk: {risk:.2%}")

# --- Nomogram Section ---
st.header("Nomogram")
st.write("Below is the nomogram visualizing the logistic regression model for postoperative bleeding risk.")

# Path to the Excel file containing the model parameters
path = "model3.xlsx"
fig = simpleNomo.nomogram(path)

# Display the nomogram figure
st.pyplot(fig)
