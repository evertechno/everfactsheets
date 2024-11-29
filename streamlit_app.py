import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email.mime.text import MIMEText
from textblob import TextBlob
import asyncio

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI: Product Improvement & Beta Version Creator")
st.write("Use generative AI, data scraping, and automation to improve your product and create beta suggestions.")

# Feature 1: Web Data Scraping from Multiple Sources
async def scrape_website(url):
    """ Scrape a website to collect data (e.g., reviews, comments). """
    try:
        response = await asyncio.to_thread(requests.get, url, timeout=10)  # 10 seconds timeout
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('p', class_='review-text')  # Modify according to website structure
        review_texts = [review.get_text() for review in reviews]
        return review_texts
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
    except Exception as e:
        st.error(f"Error scraping website: {e}")
    return []

# Feature 2: Sentiment Analysis (TextBlob)
def sentiment_analysis(text):
    """ Perform sentiment analysis on the given text. """
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    return sentiment

# Feature 3: Competitor Feature Comparison
async def competitor_feature_comparison(features):
    """ Compare product features with competitors. """
    prompt = f"Compare these features with current competitors: {features}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 4: Customer Feedback Aggregation
def aggregate_feedback(feedback_list):
    """ Aggregate multiple feedback sources into one cohesive list. """
    return "\n".join(feedback_list)

# Feature 5: Visualization of Feedback Trends
def visualize_feedback_trends(feedback_data):
    """ Visualize trends in customer feedback (e.g., sentiment). """
    sentiments = [sentiment_analysis(fb) for fb in feedback_data]
    df = pd.DataFrame({'Feedback': feedback_data, 'Sentiment': sentiments})
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Sentiment'], bins=10, kde=True)
    st.pyplot(plt)

# Feature 6: Customizable Prompt for AI Model
async def generate_custom_response(prompt):
    """ Generate AI responses based on user prompt. """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 7: Automated Email Notifications for Beta Testing Invitations
def send_beta_invite(email, invite_message):
    """ Send an invitation email to beta testers. """
    try:
        msg = MIMEText(invite_message)
        msg['Subject'] = 'Beta Test Invitation'
        msg['From'] = 'youremail@example.com'
        msg['To'] = email
        
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login('youremail@example.com', 'yourpassword')
        server.sendmail('youremail@example.com', email, msg.as_string())
        server.quit()
        st.success(f"Invitation sent to {email}")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Feature 8: Integration with Slack for Real-Time Updates
def send_slack_message(slack_webhook_url, message):
    """ Send message to Slack channel. """
    payload = {"text": message}
    try:
        response = requests.post(slack_webhook_url, json=payload)
        if response.status_code == 200:
            st.success("Message sent to Slack!")
        else:
            st.error("Error sending message to Slack.")
    except Exception as e:
        st.error(f"Error sending message to Slack: {e}")

# Feature 9: Machine Learning for Feature Prioritization
async def prioritize_features(features):
    """ Use ML model (e.g., decision tree) to prioritize features. """
    prompt = f"Prioritize these features based on user feedback: {features}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 10: User Profile for Personalized Feedback
def get_user_profile(user_id):
    """ Fetch user profile for personalized feedback. """
    # Example: Fetch user data from a database (using user_id)
    user_data = {"user_id": user_id, "preferences": "User likes dark mode."}
    return user_data

# Feature 11: User Interface Suggestions via AI
async def ui_suggestions(feedback):
    """ Generate user interface suggestions based on feedback. """
    prompt = f"Based on the following feedback, suggest UI improvements: {feedback}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 12: Error Log for Monitoring
def log_error(error_message):
    """ Log errors for debugging and monitoring purposes. """
    with open("error_log.txt", "a") as log_file:
        log_file.write(error_message + "\n")

# Feature 13: Trending Topic Identification
async def identify_trending_topics(feedback):
    """ Identify trending topics based on feedback data. """
    prompt = f"Identify trending topics from the following feedback: {feedback}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 14: Version Control and Diff for Beta Releases
async def version_diff(current_version, new_version):
    """ Compare differences between versions. """
    prompt = f"Compare these two versions:\nCurrent Version: {current_version}\nNew Version: {new_version}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 15: Automated A/B Testing Suggestions
async def ab_testing_suggestions(current_features, new_features):
    """ Generate A/B testing suggestions. """
    prompt = f"Suggest A/B testing strategies for:\nCurrent Features: {current_features}\nNew Features: {new_features}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

# Feature 17: Exporting Data to CSV/Excel
def export_data_to_csv(data):
    """ Export data to CSV. """
    df = pd.DataFrame(data)
    df.to_csv("scraped_data.csv", index=False)
    st.download_button("Download Data", data="scraped_data.csv", file_name="scraped_data.csv")

# Streamlit UI Logic
url = st.text_input("Enter the competitor/product website URL:", "https://example.com")
if st.button("Scrape and Analyze"):
    # Asynchronously scrape website and perform analysis
    reviews = asyncio.run(scrape_website(url))
    if reviews:
        st.write(f"Scraped {len(reviews)} reviews from {url}.")
        # Visualize feedback trends
        visualize_feedback_trends(reviews)
        
        # Suggest product improvements
        improvement_suggestions = asyncio.run(generate_custom_response("Suggest improvements for product."))
        st.write("Suggested Product Improvements:")
        st.write(improvement_suggestions)
        
        # Generate beta version suggestions
        beta_suggestions = asyncio.run(generate_custom_response("Generate beta version roadmap."))
        st.write("Suggested Beta Version Roadmap:")
        st.write(beta_suggestions)
