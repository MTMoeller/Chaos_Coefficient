import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# Create a streamlit config page

st.set_page_config("Chaos Coefficient", page_icon=":bar_chart:", layout="wide")

# Title
st.title("Chaos Coefficient")

st.write("Welcome to the Chaos Coefficient! This app is designed to help you understand the chaos in your lifestyle. Enter the number of kids you have and their birthdates.")

# Create a latex form that explains the chaos coefficient: the sum of all kids ages divided by the number of kids minus the number of kids
st.latex(r"Chaos = \frac{ \sum_{i=1}^{n} age_i }{n}- n")


# Create a data entry for number of kids
num_kids = st.number_input("Number of kids", min_value=1, max_value=18, value=1)
# for number of kids create multiple rows for each kid

# Create a dataframe to store the data
df = pd.DataFrame(columns=["Kid", "Birthdate"])

for i in range(num_kids):
    col1, col2 = st.columns([1, 3])
    with col1:    
        kid = st.text_input(f"Kid {i+1} name", f"Kid {i+1}")
    with col2:
        birthdate = st.date_input(f"Kid {i+1} birthdate")
    df.loc[i] = [kid, birthdate]



# Create metrics for the chaos coefficient
# Calculate the age of each kid
# Convert the 'Birthdate' column to pandas datetime format before the subtraction
df["Birthdate"] = pd.to_datetime(df["Birthdate"])

# Now the subtraction should work
df["Age"] = (pd.to_datetime("today") - df["Birthdate"]).dt.days 
#st.dataframe(df)
# Calculate the sum of all kids ages
total_age = df["Age"].sum()
# Calculate the chaos coefficient
chaos = (total_age / (365*num_kids)) - num_kids
#Display the chaos coefficient
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Chaos Coefficient", chaos)
with col2:
    # Date out of negative chaos coefficient
    # Calculate the date when the chaos coefficient will be 0
    # Calculate the number of days to reach 0 chaos
    days_to_zero = (num_kids ** 2) * 365.25
    # Calculate the date when the chaos coefficient will be 0
    date_zero = pd.to_datetime("today") + pd.Timedelta(days=days_to_zero)
    st.metric("Date to Zero Chaos", str(date_zero.date()))
with col3:
    # Calculate what the score would be if you had a score 9 months from today
    # Calculate the number of days to reach 9 months
    days_to_9months = 9 * 30
    # Calculate the chaos coefficient in 9 months
    chaos_9months = ((total_age + (days_to_9months*num_kids))  / ((num_kids+1)*365)) - (num_kids+1)
    st.metric("Aaron Chaos Estimate", chaos_9months)

# Display a chart that shows the chaos coefficient from the date of the youngest child to the date of the oldest child + 10 years
# Calculate the date of the youngest child
oldest = df["Birthdate"].min()
# Calculate the date of the oldest child
youngest = df["Birthdate"].max()
# Calculate the date 10 years after the oldest child
youngest_10years = youngest + pd.DateOffset(years=10)
# Create a date range from the youngest child to 10 years after the oldest child
date_range = pd.date_range(oldest, youngest_10years, freq="D")
# Plot the chaos coefficient over the date range
# The chaos coefficient is a time series that starts at the date of the oldest child and ends 10 years after the youngest child each kid changes the algorithm and the plot should reflect this
# Create a dataframe with the date range and the chaos coefficient
chaos_range = []
for date in date_range:
    # Calculate the chaos coefficient for the date based off which kids existed at that time
    # Check to see which kids were born at that time
    kids = df[df["Birthdate"] <= date]
    # Calculate the chaos coefficient for the date
    # Calculate the sum of all kids ages at that time based on the date
    kids_age = []
    for kid in kids["Birthdate"]:
        age = (date - kid).days 
        kids_age.append(age)
    total_age = sum(kids_age)/ 365.25
    num_kids = len(kids)
    # Calculate the chaos coefficient
    chaos = (total_age / num_kids) - num_kids
    chaos_range.append(chaos)
# Create a dataframe with the date range and the chaos coefficient
df_plot = pd.DataFrame({"Date": date_range, "Chaos": chaos_range})
# Plot the chart and fill the area under the curve with a color representing the chaos coefficient red if negative, blue if positive
# Plot the chart and fill the area under the curve with a color representing the chaos coefficient
chart = alt.Chart(df_plot).mark_area().encode(
    x="Date",
    y="Chaos",
    color=alt.Color('Color:N')  # Use the new 'Color' column to set the color
)
# Add a vertical line at the current date make it thick and white
today = pd.to_datetime("today")
rule = alt.Chart(pd.DataFrame({"Date": [today]})).mark_rule(color="white").encode(x="Date:T")

chart = chart + rule

st.altair_chart(chart, use_container_width=True)




#chart = alt.Chart(df_plot).mark_line().encode(x="Date", y="Chaos")
#st.altair_chart(chart, use_container_width=True)