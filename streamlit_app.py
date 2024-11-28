import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import weasyprint
from io import BytesIO
import base64

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
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(data)))
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    plt.title(title)
    return fig

# Function to generate performance line chart
def create_performance_chart():
    performance_df = pd.DataFrame(performance_data)
    performance_df.set_index("Performance Metric", inplace=True)

    fig, ax = plt.subplots(figsize=(5, 3))
    performance_df.transpose().plot(kind='line', marker='o', ax=ax)
    plt.title("Fund Performance vs Benchmark")
    plt.ylabel("Returns (%)")
    plt.xlabel("Time Periods")
    return fig

# Generate the PDF file from HTML
def generate_pdf(html_content):
    pdf = weasyprint.HTML(string=html_content).write_pdf()
    return pdf

# Convert image to base64 for embedding in HTML
def image_to_base64(image):
    img_stream = BytesIO()
    image.savefig(img_stream, format="png")
    img_stream.seek(0)
    img_str = base64.b64encode(img_stream.read()).decode('utf-8')
    return img_str

# Streamlit App
def app():
    st.title("Fund Factsheet Generator")

    # HTML Template
    html_template = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
                margin: 0;
                padding: 0;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }
            .section {
                width: 48%;
                margin-bottom: 10px;
            }
            .header {
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="section">
                <h2 class="header">Fund Overview</h2>
                <table>
                    <tr><th>Fund Name</th><td>XYZ Growth Fund</td></tr>
                    <tr><th>Fund Type</th><td>Equity</td></tr>
                    <tr><th>Investment Objective</th><td>Growth with Capital Appreciation</td></tr>
                    <tr><th>Risk Level</th><td>High</td></tr>
                    <tr><th>Fund Manager</th><td>John Doe</td></tr>
                    <tr><th>Inception Date</th><td>2020-01-01</td></tr>
                    <tr><th>Fund Size (USD)</th><td>100,000,000</td></tr>
                </table>
            </div>
            <div class="section">
                <h2 class="header">Performance Data</h2>
                <table>
                    <tr><th>Metric</th><th>Fund</th><th>Benchmark</th></tr>
                    <tr><td>1 Month</td><td>2.5%</td><td>2.0%</td></tr>
                    <tr><td>3 Months</td><td>5.6%</td><td>5.1%</td></tr>
                    <tr><td>1 Year</td><td>12.3%</td><td>10.5%</td></tr>
                    <tr><td>3 Years</td><td>36.1%</td><td>30.2%</td></tr>
                    <tr><td>5 Years</td><td>57.8%</td><td>50.1%</td></tr>
                    <tr><td>Since Inception</td><td>80.2%</td><td>70.4%</td></tr>
                </table>
            </div>
        </div>

        <div class="container">
            <div class="section">
                <h2 class="header">Portfolio Composition</h2>
                <img src="data:image/png;base64,{portfolio_img}" alt="Portfolio Composition" width="100%"/>
            </div>
            <div class="section">
                <h2 class="header">Top 10 Holdings</h2>
                <img src="data:image/png;base64,{top_holdings_img}" alt="Top 10 Holdings" width="100%"/>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the pie chart for Portfolio Composition
    fig_portfolio = create_pie_chart(portfolio_composition['Weight'], portfolio_composition['Asset Class'], 'Portfolio Composition')
    portfolio_img = image_to_base64(fig_portfolio)

    # Create the pie chart for Top 10 Holdings
    fig_holdings = create_pie_chart(top_holdings['Weight'], top_holdings['Holding Name'], 'Top 10 Holdings')
    top_holdings_img = image_to_base64(fig_holdings)

    # Replace placeholders in HTML template
    html_content = html_template.format(portfolio_img=portfolio_img, top_holdings_img=top_holdings_img)

    # PDF Generation Button
    if st.button("Generate PDF"):
        pdf = generate_pdf(html_content)
        
        # Create a download link for the PDF
        pdf_base64 = base64.b64encode(pdf).decode('utf-8')
        pdf_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="fund_factsheet.pdf">Download the Fund Factsheet PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
