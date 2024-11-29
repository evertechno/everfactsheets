import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.generativeai import gemini

# Configure the API key securely from Streamlit's secrets
gemini.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI: Product Improvement & Beta Version Creator")
st.write("Use generative AI, data scraping, and automation to improve your product and create beta suggestions.")

# Feature 1: Web Data Scraping from Multiple Sources
def scrape_website(url):
    """ Scrape a website to collect data (e.g., reviews, comments). """
    try:
        st.write("Starting to scrape the website...")
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        if response.status_code != 200:
            st.error(f"Error: Unable to fetch the page. Status code: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('p', class_='review-text')  # Modify according to website structure
        
        # For debugging: Show the number of reviews fetched
        st.write(f"Found {len(reviews)} reviews.")
        
        review_texts = [review.get_text() for review in reviews]
        
        # For debugging: Show the first few reviews
        if review_texts:
            st.write("First few reviews:")
            st.write(review_texts[:5])
        
        return review_texts
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
    except Exception as e:
        st.error(f"Error scraping website: {e}")
    return []

# Feature 5: Visualization of Feedback Trends
def visualize_feedback_trends(feedback_data):
    """ Visualize trends in customer feedback (e.g., sentiment). """
    if not feedback_data:
        st.warning("No feedback data available to visualize.")
        return
    
    st.write("Visualizing sentiment trends...")
    # Placeholder sentiment: Use length of reviews as dummy sentiment
    sentiments = [len(fb) for fb in feedback_data]  # For now, using length as sentiment
    df = pd.DataFrame({'Feedback': feedback_data, 'Sentiment': sentiments})
    
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Sentiment'], bins=10, kde=True)
    st.pyplot(plt)

# Feature 6: Customizable Prompt for AI Model
def generate_custom_response(prompt):
    """ Generate AI responses based on user prompt. """
    st.write("Generating AI response for improvements...")
    model = gemini.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI Logic
url = st.text_input("Enter the competitor/product website URL:", "https://example.com")

# Button to trigger scraping and analysis
if st.button("Scrape and Analyze"):
    # Scrape website
    reviews = scrape_website(url)
    
    if reviews:
        st.write(f"Scraped {len(reviews)} reviews from {url}.")
        
        # Visualize feedback trends
        visualize_feedback_trends(reviews)
        
        # Suggest product improvements
        improvement_suggestions = generate_custom_response("Suggest improvements for product.")
        st.write("Suggested Product Improvements:")
        st.write(improvement_suggestions)
        
        # Generate beta version suggestions
        beta_suggestions = generate_custom_response("Generate beta version roadmap.")
        st.write("Suggested Beta Version Roadmap:")
        st.write(beta_suggestions)
