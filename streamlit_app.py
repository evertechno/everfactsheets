import streamlit as st
import pandas as pd
import io

# Sample CSV Template Data
fund_overview = """Fund Name,Fund Type,Investment Objective,Risk Level,Fund Manager
XYZ Growth Fund,Equity,Growth with Capital Appreciation,High,John Doe
Inception Date,Fund Size,Base Currency,Minimum Investment
2020-01-01,100000000,USD,10000
"""

performance_data = """Performance Metric,1 Month,3 Months,1 Year,3 Years,5 Years,Since Inception
Fund Return,2.5%,5.6%,12.3%,36.1%,57.8%,80.2%
Benchmark Return,2.0%,5.1%,10.5%,30.2%,50.1%,70.4%
"""

portfolio_composition = """Asset Class,Weight
Equity,60%
Fixed Income,30%
Cash,5%
Alternative Assets,5%
"""

top_holdings = """Rank,Holding Name,Asset Class,Value (USD),Weight
1,Company A,Equity,20000000,20%
2,Company B,Equity,15000000,15%
3,Treasury Bond 10Y,Fixed Income,10000000,10%
4,Company C,Equity,8000000,8%
5,Money Market Fund,Cash,5000000,5%
6,Company D,Equity,4000000,4%
7,Corporate Bond A,Fixed Income,3000000,3%
8,Company E,Equity,2500000,2.5%
9,Company F,Equity,2000000,2%
10,Company G,Equity,1500000,1.5%
"""

sector_allocation = """Sector,Weight
Technology,25%
Healthcare,20%
Financials,15%
Consumer Discretionary,10%
Industrials,10%
Utilities,8%
Energy,7%
Materials,5%
Real Estate,3%
"""

risk_metrics = """Risk Metric,1 Year,3 Years,5 Years
Volatility,10%,12%,14%
Sharpe Ratio,1.2,1.3,1.5
Max Drawdown,-15%,-20%,-18%
"""

fund_manager_commentary = """Fund Manager Commentary
"The fund performed well during the period, outperforming the benchmark. We are overweight in technology stocks, and expect continued growth in the sector."
"""

# Function to generate CSV template
def generate_csv_template():
    # Combine all sections into one CSV template
    full_template = (
        "# Fund Overview\n" + fund_overview + "\n\n" +
        "# Performance Data\n" + performance_data + "\n\n" +
        "# Portfolio Composition\n" + portfolio_composition + "\n\n" +
        "# Top 10 Holdings\n" + top_holdings + "\n\n" +
        "# Sector Allocation\n" + sector_allocation + "\n\n" +
        "# Risk Metrics\n" + risk_metrics + "\n\n" +
        "# Fund Manager Commentary\n" + fund_manager_commentary
    )
    
    # Convert to byte stream for download
    return io.BytesIO(full_template.encode())

# Streamlit App
def app():
    # Title and Instructions
    st.title("Fund Factsheet Generator")
    st.write("""
    This application allows you to generate a fund factsheet by uploading a CSV file.
    You can also download a template to fill out and upload back to generate your factsheet.
    """)

    # Download Template Button
    st.download_button(
        label="Download Fund Factsheet Template",
        data=generate_csv_template(),
        file_name="fund_factsheet_template.csv",
        mime="text/csv",
    )
    
    st.markdown("---")

    # File Upload Section
    uploaded_file = st.file_uploader("Upload your CSV file for factsheet", type=["csv"])
    
    if uploaded_file is not None:
        # Read the uploaded CSV into a DataFrame
        df = pd.read_csv(uploaded_file)
        st.write("Data from the uploaded CSV:")
        st.dataframe(df)
        
        # Displaying specific sections if available
        if "# Fund Overview" in df.to_string():
            st.header("Fund Overview")
            fund_overview_df = df[df["Fund Name"].notna()]
            st.write(fund_overview_df)

        if "# Performance Data" in df.to_string():
            st.header("Performance Data")
            performance_df = df[df["Performance Metric"].notna()]
            st.write(performance_df)

        if "# Portfolio Composition" in df.to_string():
            st.header("Portfolio Composition")
            portfolio_df = df[df["Asset Class"].notna()]
            st.write(portfolio_df)

        if "# Top 10 Holdings" in df.to_string():
            st.header("Top 10 Holdings")
            holdings_df = df[df["Rank"].notna()]
            st.write(holdings_df)

        if "# Sector Allocation" in df.to_string():
            st.header("Sector Allocation")
            sector_df = df[df["Sector"].notna()]
            st.write(sector_df)

        if "# Risk Metrics" in df.to_string():
            st.header("Risk Metrics")
            risk_df = df[df["Risk Metric"].notna()]
            st.write(risk_df)

        if "# Fund Manager Commentary" in df.to_string():
            st.header("Fund Manager Commentary")
            commentary_df = df[df["Fund Manager Commentary"].notna()]
            st.write(commentary_df)

if __name__ == "__main__":
    app()
