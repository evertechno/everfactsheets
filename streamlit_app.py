import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Sample Data for the Fund Factsheet

# Fund Overview
fund_overview = {
    "Fund Name": ["XYZ Growth Fund"],
    "Fund Type": ["Equity"],
    "Investment Objective": ["Growth with Capital Appreciation"],
    "Risk Level": ["High"],
    "Fund Manager": ["John Doe"],
    "Inception Date": ["2020-01-01"],
    "Fund Size (USD)": [100000000],
    "Base Currency": ["USD"],
    "Minimum Investment (USD)": [10000]
}

# Performance Data
performance_data = {
    "Performance Metric": ["Fund Return", "Benchmark Return"],
    "1 Month": [2.5, 2.0],
    "3 Months": [5.6, 5.1],
    "1 Year": [12.3, 10.5],
    "3 Years": [36.1, 30.2],
    "5 Years": [57.8, 50.1],
    "Since Inception": [80.2, 70.4]
}

# Portfolio Composition (Pie Chart)
portfolio_composition = {
    "Asset Class": ["Equity", "Fixed Income", "Cash", "Alternative Assets"],
    "Weight": [60, 30, 5, 5]
}

# Top 10 Holdings (Pie Chart)
top_holdings = {
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Holding Name": ["Company A", "Company B", "Treasury Bond 10Y", "Company C", "Money Market Fund", 
                     "Company D", "Corporate Bond A", "Company E", "Company F", "Company G"],
    "Asset Class": ["Equity", "Equity", "Fixed Income", "Equity", "Cash", "Equity", "Fixed Income", "Equity", "Equity", "Equity"],
    "Value (USD)": [20000000, 15000000, 10000000, 8000000, 5000000, 4000000, 3000000, 2500000, 2000000, 1500000],
    "Weight": [20, 15, 10, 8, 5, 4, 3, 2.5, 2, 1.5]
}

# Risk Metrics
risk_metrics = {
    "Risk Metric": ["Volatility", "Sharpe Ratio", "Max Drawdown"],
    "1 Year": [10, 1.2, -15],
    "3 Years": [12, 1.3, -20],
    "5 Years": [14, 1.5, -18]
}

# Fund Manager Commentary
fund_manager_commentary = {
    "Fund Manager Commentary": ["The fund performed well during the period, outperforming the benchmark. We are overweight in technology stocks, and expect continued growth in the sector."]
}

# Function to create pie chart for portfolio composition
def create_pie_chart(data, labels, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(data)))
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    plt.title(title)
    return fig

# Function to generate performance line chart
def create_performance_chart():
    performance_df = pd.DataFrame(performance_data)
    performance_df.set_index("Performance Metric", inplace=True)

    fig, ax = plt.subplots()
    performance_df.transpose().plot(kind='line', marker='o', ax=ax)
    plt.title("Fund Performance vs Benchmark")
    plt.ylabel("Returns (%)")
    plt.xlabel("Time Periods")
    return fig

# Function to generate Excel template
def generate_excel_template():
    # Create a Pandas Excel writer using BytesIO to avoid saving it to the disk
    output = io.BytesIO()

    # Write all sections as separate sheets
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(fund_overview).to_excel(writer, sheet_name='Fund Overview', index=False)
        pd.DataFrame(performance_data).to_excel(writer, sheet_name='Performance Data', index=False)
        pd.DataFrame(portfolio_composition).to_excel(writer, sheet_name='Portfolio Composition', index=False)
        pd.DataFrame(top_holdings).to_excel(writer, sheet_name='Top 10 Holdings', index=False)
        pd.DataFrame(risk_metrics).to_excel(writer, sheet_name='Risk Metrics', index=False)
        pd.DataFrame(fund_manager_commentary).to_excel(writer, sheet_name='Fund Manager Commentary', index=False)

    output.seek(0)  # Go to the beginning of the BytesIO stream
    return output

# Streamlit App
def app():
    # Title and Instructions
    st.title("Fund Factsheet Generator")
    st.write("""
    This application allows you to generate a fund factsheet with graphs, charts, and performance data.
    You can download a template in Excel format, fill it out, and upload it back to generate a dynamic factsheet.
    """)

    # Download Template Button
    st.download_button(
        label="Download Fund Factsheet Template (Excel)",
        data=generate_excel_template(),
        file_name="fund_factsheet_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.markdown("---")

    # File Upload Section
    uploaded_file = st.file_uploader("Upload your Excel file for factsheet", type=["xlsx"])
    
    if uploaded_file is not None:
        # Read the uploaded Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)  # Read all sheets

        st.write("### Data from the uploaded Excel:")

        # Display Fund Overview
        if 'Fund Overview' in excel_data:
            st.header("Fund Overview")
            st.write(excel_data['Fund Overview'])

        # Display Performance Data
        if 'Performance Data' in excel_data:
            st.header("Performance Data")
            st.write(excel_data['Performance Data'])

        # Display Portfolio Composition Pie Chart
        if 'Portfolio Composition' in excel_data:
            st.header("Portfolio Composition")
            portfolio_df = excel_data['Portfolio Composition']
            fig = create_pie_chart(portfolio_df['Weight'], portfolio_df['Asset Class'], 'Portfolio Composition')
            st.pyplot(fig)

        # Display Top 10 Holdings Pie Chart
        if 'Top 10 Holdings' in excel_data:
            st.header("Top 10 Holdings")
            holdings_df = excel_data['Top 10 Holdings']
            fig = create_pie_chart(holdings_df['Weight'], holdings_df['Holding Name'], 'Top 10 Holdings')
            st.pyplot(fig)

        # Display Risk Metrics
        if 'Risk Metrics' in excel_data:
            st.header("Risk Metrics")
            st.write(excel_data['Risk Metrics'])

        # Display Fund Manager Commentary
        if 'Fund Manager Commentary' in excel_data:
            st.header("Fund Manager Commentary")
            st.write(excel_data['Fund Manager Commentary'])

        # Display Fund Performance Line Chart
        st.header("Fund Performance")
        fig = create_performance_chart()
        st.pyplot(fig)

if __name__ == "__main__":
    app()
