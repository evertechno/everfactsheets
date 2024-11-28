import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load the CSV data
def load_data(file):
    return pd.read_csv(file)

# Function to display portfolio composition as a pie chart
def display_portfolio_composition(df):
    st.subheader('Portfolio Composition')
    # Assuming 'Asset Class' and 'Weight' are columns in the CSV
    composition = df.groupby('Asset Class')['Weight'].sum()
    fig, ax = plt.subplots()
    composition.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_ylabel('')
    st.pyplot(fig)

# Function to display top 10 holdings
def display_top_holdings(df):
    st.subheader('Top 10 Holdings')
    # Assuming 'Holding Name' and 'Value' are columns in the CSV
    top_10 = df.nlargest(10, 'Value')[['Holding Name', 'Value']]
    st.dataframe(top_10)

# Function to display the investment objective (assuming this is in the CSV)
def display_investment_objective(df):
    st.subheader('Investment Objective')
    # Assuming there's a column 'Investment Objective' in the CSV
    objective = df['Investment Objective'].iloc[0]  # Just an example
    st.write(objective)

# Main function to build the app
def main():
    st.title("Dynamic Factsheet Generator")

    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        # Show the raw data
        st.subheader('Raw Data')
        st.write(df.head())

        # Generate the factsheet sections
        display_portfolio_composition(df)
        display_top_holdings(df)
        display_investment_objective(df)

if __name__ == "__main__":
    main()
