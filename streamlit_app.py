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

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Ever AI: Product Improvement & Beta Version Creator")
st.write("Use generative AI, data scraping, and automation to improve your product and create beta suggestions.")

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            st.error(f"Error: Unable to fetch the page. Status code: {response.status_code}")
            return "", [], []
        soup = BeautifulSoup(response.text, 'html.parser')
        text_data = soup.get_text()
        image_urls = [img['src'] for img in soup.find_all('img') if img.get('src')]
        link_urls = [link['href'] for link in soup.find_all('a', href=True)]
        return text_data, image_urls, link_urls
    except requests.exceptions.Timeout:
        st.error("The request timed out.")
    except Exception as e:
        st.error(f"Error: {e}")
    return "", [], []

def visualize_data_analysis(text_data):
    if not text_data: return
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
    st.image(wordcloud.to_array(), caption="Word Cloud")

def generate_custom_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content(prompt).text

def generate_beta_roadmap(text_data):
    return generate_custom_response(f"Create a beta version roadmap: {text_data[:300]}")

def analyze_sentiment(text_data):
    return TextBlob(text_data).sentiment

def analyze_word_frequency(text_data):
    words = text_data.split()
    common_words = Counter(words).most_common(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=[x[0] for x in common_words], y=[x[1] for x in common_words])
    plt.title("Most Common Words in Scraped Text")
    st.pyplot()

def show_image_gallery(image_urls):
    for img_url in image_urls[:5]:
        st.image(img_url, caption="Scraped Image", use_column_width=True)

def show_links_list(link_urls):
    for link in link_urls[:5]:
        st.write(f"[{link}]({link})")

def extract_keywords(text_data):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text_data])
    feature_names = vectorizer.get_feature_names_out()
    dense = X.todense()
    keyword_scores = dense.tolist()[0]
    keywords = sorted([(feature_names[i], keyword_scores[i]) for i in range(len(feature_names))], key=lambda x: x[1], reverse=True)[:5]
    return keywords

def random_product_suggestion():
    return random.choice([
        "Improve the user interface.", "Offer a mobile version.", "Add social media sharing.",
        "Implement a loyalty rewards system.", "Integrate voice search.", "Improve documentation."
    ])

url = st.text_input("Enter website URL:", "https://example.com")

if st.button("Scrape and Analyze"):
    text_data, image_urls, link_urls = scrape_website(url)
    
    if text_data:
        st.write(f"Scraped content from {url}.")
        st.write("Scraped Text (First 500 characters):")
        st.write(text_data[:500])
        
        visualize_data_analysis(text_data)
        
        improvement_suggestions = generate_custom_response(f"Suggest improvements: {text_data[:500]}")
        st.write("Suggested Product Improvements:")
        st.write(improvement_suggestions)
        
        beta_roadmap = generate_beta_roadmap(text_data)
        st.write("Suggested Beta Version Roadmap:")
        st.write(beta_roadmap)
        
        sentiment = analyze_sentiment(text_data)
        st.write(f"Sentiment: Polarity = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}")
        
        analyze_word_frequency(text_data)
        
        if image_urls:
            show_image_gallery(image_urls)
        
        if link_urls:
            show_links_list(link_urls)
        
        keywords = extract_keywords(text_data)
        st.write("Top 5 Keywords:")
        st.write(keywords)
        
        random_suggestion = random_product_suggestion()
        st.write(f"Random Product Suggestion: {random_suggestion}")
