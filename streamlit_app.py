import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from textstat.textstat import textstatistics
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline

# Configure the Gemini API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI: Product Improvement & Beta Version Creator")
st.write("Use generative AI, data scraping, and automation to improve your product and create beta suggestions.")

# Default URL to analyze if no input is given
default_url = "https://example.com"  # Replace this with a real URL or a placeholder for automatic scraping

# Feature 1: Scrape Website Data (Text)
def scrape_website(url):
    try:
        st.write("Starting to scrape the website...")
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        if response.status_code != 200:
            st.error(f"Error: Unable to fetch the page. Status code: {response.status_code}")
            return None, None, None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape all text content
        text_data = soup.get_text()

        # Get the number of paragraphs, headings, etc.
        headings = soup.find_all(['h1', 'h2', 'h3'])
        paragraphs = soup.find_all('p')

        return text_data, headings, paragraphs
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
    except Exception as e:
        st.error(f"Error scraping website: {e}")
    return None, None, None

# Feature 2: Word Cloud Visualization
def create_word_cloud(text_data):
    if not text_data:
        st.warning("No text data available to visualize.")
        return

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

# Feature 3: Visualize Basic Data Insights (Word Frequency Analysis)
def analyze_word_frequency(text_data):
    if not text_data:
        st.warning("No text data available to visualize.")
        return

    words = text_data.split()
    word_counts = Counter(words)
    common_words = word_counts.most_common(10)

    # Create bar plot for word frequency
    words, counts = zip(*common_words)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(words), y=list(counts))
    plt.title("Most Common Words in Scraped Text")
    st.pyplot()

# Feature 4: Sentiment Analysis
def analyze_sentiment(text_data):
    sentiment = TextBlob(text_data).sentiment
    return sentiment

# Feature 5: Keyword Extraction (TF-IDF)
def extract_keywords(text_data):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text_data])
    feature_names = vectorizer.get_feature_names_out()
    dense = X.todense()
    keyword_scores = dense.tolist()[0]
    keywords = [(feature_names[i], keyword_scores[i]) for i in range(len(feature_names))]
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:5]
    return keywords

# Feature 6: Topic Modeling (LDA)
def topic_modeling(text_data):
    if not text_data:
        st.warning("No text data available for topic modeling.")
        return
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text_data])
    
    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    lda.fit(X)
    
    topics = []
    for idx, topic in enumerate(lda.components_):
        topic_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
        topics.append(f"Topic {idx + 1}: " + ", ".join(topic_words))
    
    return topics

# Feature 7: Readability Analysis (Flesch-Kincaid)
def readability_analysis(text_data):
    if not text_data:
        st.warning("No text data available for readability analysis.")
        return
    
    readability_score = textstatistics().flesch_kincaid_grade(text_data)
    return f"Readability (Flesch-Kincaid Grade Level): {readability_score}"

# Feature 8: Clustering of Product Features
def cluster_product_features(keywords):
    if not keywords:
        st.warning("No keywords available for clustering.")
        return
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([keyword[0] for keyword in keywords])
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)
    
    labels = kmeans.labels_
    clusters = {}
    for label, keyword in zip(labels, keywords):
        clusters.setdefault(label, []).append(keyword[0])
    
    return clusters

# Feature 9: Product Rating Analysis
def analyze_product_ratings(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        ratings = [float(rating.get_text()) for rating in soup.find_all('span', class_='product-rating')]
        avg_rating = np.mean(ratings) if ratings else None
        return avg_rating
    except Exception as e:
        st.warning(f"Error analyzing ratings: {e}")
        return None

# Feature 10: Keyword Trend Analysis (Compare multiple URLs)
def keyword_trend_analysis(urls):
    all_keywords = []
    for url in urls:
        text_data, _, _ = scrape_website(url)
        if text_data:
            keywords = extract_keywords(text_data)
            all_keywords.append([keyword[0] for keyword in keywords])
    
    return all_keywords

# Feature 11: Text Similarity Comparison
def text_similarity_comparison(text1, text2):
    if not text1 or not text2:
        st.warning("Insufficient data to compare text similarity.")
        return
    
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([text1, text2])
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix[0][1]

# Feature 12: AI-powered Feature Generation
def generate_ai_feature_suggestion(text_data):
    st.write("Generating AI-powered feature suggestions...")
    prompt = f"Based on the following text data, suggest new features for a product: {text_data[:300]}"
    feature_suggestion = generate_custom_response(prompt)
    return feature_suggestion

# Streamlit UI Logic
url_input = st.text_input("Enter the competitor/product website URL (Leave blank for default URL):", "")
competitor_url_input = st.text_input("Enter competitor/product URL for comparison:", "")

url = url_input if url_input else default_url

# Initialize session state for text data
if "text_data" not in st.session_state:
    st.session_state.text_data = None

# Button to trigger scraping and analysis
if st.button("Analyze and Suggest Improvements"):
    # Scrape website
    st.session_state.text_data, headings, paragraphs = scrape_website(url)
    
    if st.session_state.text_data:
        # Display content
        st.write(f"Scraped content from {url}.")
        st.write("Scraped Text (First 500 characters):")
        st.write(st.session_state.text_data[:500])

        # Visualizations and Analysis
        analyze_word_frequency(st.session_state.text_data)
        create_word_cloud(st.session_state.text_data)

        # Sentiment Analysis
        sentiment = analyze_sentiment(st.session_state.text_data)
        st.write(f"Sentiment Analysis: Polarity = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}")

        # Extract Keywords
        keywords = extract_keywords(st.session_state.text_data)
        st.write("Top 5 Keywords:")
        st.write(keywords)

        # Topic Modeling
        topics = topic_modeling(st.session_state.text_data)
        st.write("Identified Topics:")
        st.write(topics)

        # Readability Analysis
        readability = readability_analysis(st.session_state.text_data)
        st.write(readability)

        # Clustering Keywords
        clusters = cluster_product_features(keywords)
        st.write("Keyword Clusters:")
        st.write(clusters)

        # Product Rating Analysis
        avg_rating = analyze_product_ratings(url)
        if avg_rating:
            st.write(f"Average Product Rating: {avg_rating}")

        # AI Feature Suggestion
        ai_feature = generate_ai_feature_suggestion(st.session_state.text_data)
        st.write("Suggested New Feature:")
        st.write(ai_feature)

# Compare with competitor data if URL is provided
if competitor_url_input:
    competitor_text_data, _, _ = scrape_website(competitor_url_input)
    if competitor_text_data:
        similarity = text_similarity_comparison(st.session_state.text_data, competitor_text_data)
        st.write(f"Text Similarity with Competitor: {similarity}")

# Button to generate overall summary
if st.button("Generate Overall Advisory"):
    if st.session_state.text_data:
        # Summarize the analysis
        summary_prompt = f"Please summarize the analysis of the following product data: {st.session_state.text_data[:500]}"
        summary = generate_custom_response(summary_prompt)
        st.write("Summary of Analysis:")
        st.write(summary)
    else:
        st.error("No data available to generate advisory. Please check the website URL or try again.")
