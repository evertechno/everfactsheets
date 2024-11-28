import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
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

# Convert image to base64 for embedding in HTML
def image_to_base64(image):
    img_stream = BytesIO()
    image.savefig(img_stream, format="png")
    img_stream.seek(0)
    img_str = base64.b64encode(img_stream.read()).decode('utf-8')
    return img_str

# Function to generate PDF
def generate_pdf():
    # Create a new PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Fund Overview Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 750, "Fund Overview:")
    y_position = 730
    c.setFont("Helvetica", 10)
    for key, value in fund_overview.items():
        c.drawString(50, y_position, f"{key}: {value[0]}")
        y_position -= 15

    # Performance Data Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Performance Data:")
    y_position -= 20
    performance_df = pd.DataFrame(performance_data)
    c.setFont("Helvetica", 10)
    for i, row in performance_df.iterrows():
        c.drawString(50, y_position, f"{row['Performance Metric']}: {row[1]:.2f}% / {row[2]:.2f}%")
        y_position -= 15
    
    # Portfolio Composition Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Portfolio Composition:")
    y_position -= 20
    fig_portfolio = create_pie_chart(portfolio_composition['Weight'], portfolio_composition['Asset Class'], 'Portfolio Composition')
    portfolio_img = image_to_base64(fig_portfolio)
    c.drawImage(f"data:image/png;base64,{portfolio_img}", 50, y_position-100, width=200, height=150)
    y_position -= 160

    # Top Holdings Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Top 10 Holdings:")
    y_position -= 20
    fig_holdings = create_pie_chart(top_holdings['Weight'], top_holdings['Holding Name'], 'Top 10 Holdings')
    top_holdings_img = image_to_base64(fig_holdings)
    c.drawImage(f"data:image/png;base64,{top_holdings_img}", 50, y_position-100, width=200, height=150)
    
    # Finalize and save the PDF
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit App
def app():
    st.title("Fund Factsheet Generator")

    # PDF Generation Button
    if st.button("Generate PDF"):
        pdf_buffer = generate_pdf()
        
        # Provide the generated PDF as a download link
        pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
        pdf_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="fund_factsheet.pdf">Download the Fund Factsheet PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
