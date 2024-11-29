import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns
from datetime import datetime
import random
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer

# Configure the Gemini API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI: Product Improvement & Beta Version Creator")
st.write("Use generative AI, data scraping, and automation to improve your product and create beta suggestions.")

# Feature 1: Scrape Website Data (Text, Images, Links, etc.)
def scrape_website(url):
    try:
        st.write("Starting to scrape the website...")
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        if response.status_code != 200:
            st.error(f"Error: Unable to fetch the page. Status code: {response.status_code}")
            return "", [], []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape all text content
        text_data = soup.get_text()
        
        # Scrape all image URLs
        image_tags = soup.find_all('img')
        image_urls = [img['src'] for img in image_tags if img.get('src')]

        # Scrape all link URLs
        link_tags = soup.find_all('a', href=True)
        link_urls = [link['href'] for link in link_tags]

        # For debugging: Show the number of images and links fetched
        st.write(f"Found {len(image_urls)} images and {len(link_urls)} links.")
        
        return text_data, image_urls, link_urls
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
    except Exception as e:
        st.error(f"Error scraping website: {e}")
    return "", [], []

# Feature 2: Visualize Basic Data Insights
def visualize_data_analysis(text_data):
    if not text_data:
        st.warning("No text data available to visualize.")
        return
    
    # Create a word cloud to visualize the content of the scraped text
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

    st.image(wordcloud.to_array(), caption="Word Cloud of Scraped Text")

# Feature 3: Customizable AI Analysis (Product Improvements)
def generate_custom_response(prompt):
    st.write("Generating AI response for improvements...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Feature 4: Generate Beta Version Roadmap
def generate_beta_roadmap(text_data):
    st.write("Generating Beta Version Roadmap...")
    prompt = f"Create a beta version roadmap based on the following website data: {text_data[:300]}"
    roadmap = generate_custom_response(prompt)
    return roadmap

# Feature 5: Sentiment Analysis
def analyze_sentiment(text_data):
    sentiment = TextBlob(text_data).sentiment
    return sentiment

# Feature 6: Word Frequency Analysis
def analyze_word_frequency(text_data):
    words = text_data.split()
    word_counts = Counter(words)
    common_words = word_counts.most_common(10)
    
    # Create bar plot
    words, counts = zip(*common_words)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(words), y=list(counts))
    plt.title("Most Common Words in Scraped Text")
    st.pyplot()

# Feature 7: Show Image Gallery from Scraped Images
def show_image_gallery(image_urls):
    st.write("Displaying Images...")
    for img_url in image_urls[:5]:
        st.image(img_url, caption="Scraped Image", use_column_width=True)

# Feature 8: Show Links List
def show_links_list(link_urls):
    st.write("Found Links:")
    for link in link_urls[:5]:
        st.write(f"[{link}]({link})")

# Feature 9: Keyword Extraction
def extract_keywords(text_data):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text_data])
    feature_names = vectorizer.get_feature_names_out()
    dense = X.todense()
    keyword_scores = dense.tolist()[0]
    keywords = [(feature_names[i], keyword_scores[i]) for i in range(len(feature_names))]
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:5]
    return keywords

# Feature 10: Generate Smart Product Suggestion (based on analysis)
def generate_smart_product_suggestion(text_data, keywords, sentiment):
    """ Generate smart product suggestions based on the analysis of scraped data. """
    if sentiment.polarity < 0:
        suggestion = "Improve the user experience by addressing negative feedback."
    else:
        suggestion = "Enhance features related to user demand."
    
    common_keywords = [keyword[0] for keyword in keywords]
    
    if 'usability' in common_keywords or 'interface' in common_keywords:
        suggestion = "Consider improving the user interface for better accessibility."
    elif 'performance' in common_keywords or 'speed' in common_keywords:
        suggestion = "Optimize the product for better performance and speed."
    elif 'support' in common_keywords or 'help' in common_keywords:
        suggestion = "Expand your customer support options and resources."
    elif 'security' in common_keywords or 'privacy' in common_keywords:
        suggestion = "Enhance security features to build user trust."
    
    return suggestion

# Streamlit UI Logic
url = st.text_input("Enter the competitor/product website URL:", "https://example.com")

# Button to trigger scraping and analysis
if st.button("Scrape and Analyze"):
    # Scrape website
    text_data, image_urls, link_urls = scrape_website(url)
    
    if text_data:
        # Show the basic website data
        st.write(f"Scraped content from {url}.")
        
        # Show first few characters of the scraped text
        st.write("Scraped Text (First 500 characters):")
        st.write(text_data[:500])
        
        # Visualize insights from the scraped text (e.g., word cloud)
        visualize_data_analysis(text_data)
        
        # Sentiment Analysis
        sentiment = analyze_sentiment(text_data)
        st.write(f"Sentiment Analysis: Polarity = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}")
        
        # Word Frequency Analysis
        analyze_word_frequency(text_data)
        
        # Show Image Gallery
        if image_urls:
            show_image_gallery(image_urls)
        
        # Show Links
        if link_urls:
            show_links_list(link_urls)
        
        # Extract Keywords
        keywords = extract_keywords(text_data)
        st.write("Top 5 Keywords:")
        st.write(keywords)
        
        # Generate a smarter product improvement suggestion based on the analysis
        smart_suggestion = generate_smart_product_suggestion(text_data, keywords, sentiment)
        st.write(f"Smart Product Suggestion: {smart_suggestion}")
        
        # Generate beta version roadmap based on scraped data
        beta_roadmap = generate_beta_roadmap(text_data)
        st.write("Suggested Beta Version Roadmap:")
        st.write(beta_roadmap)
