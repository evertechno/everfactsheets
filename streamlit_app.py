import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Configure the Gemini API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI: Product Improvement & Beta Version Creator")
st.write("Use generative AI, data scraping, and automation to improve your product and create beta suggestions.")

# Feature 1: Scrape Website Data (Text, Images, Links, etc.)
def scrape_website(url):
    """ Scrape a website to collect various data (text, images, links). """
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
    """ Visualize basic data insights (word cloud, sentiment, etc.) """
    if not text_data:
        st.warning("No text data available to visualize.")
        return
    
    # Create a word cloud to visualize the content of the scraped text
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

    st.image(wordcloud.to_array(), caption="Word Cloud of Scraped Text")

# Feature 3: Customizable AI Analysis (Product Improvements)
def generate_custom_response(prompt):
    """ Generate AI responses based on user prompt (e.g., product improvement). """
    st.write("Generating AI response for improvements...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Feature 4: Generate Beta Version Roadmap
def generate_beta_roadmap(text_data):
    """ Generate beta version roadmap based on scraped website data (text). """
    st.write("Generating Beta Version Roadmap...")
    prompt = f"Create a beta version roadmap based on the following website data: {text_data[:300]}"  # Limit to first 300 characters for brevity
    roadmap = generate_custom_response(prompt)
    return roadmap

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
        
        # Analyze scraped data and generate product improvement suggestions
        improvement_suggestions = generate_custom_response(f"Suggest improvements for product based on the following website data: {text_data[:500]}")
        st.write("Suggested Product Improvements:")
        st.write(improvement_suggestions)
        
        # Generate beta version roadmap based on scraped data
        beta_roadmap = generate_beta_roadmap(text_data)
        st.write("Suggested Beta Version Roadmap:")
        st.write(beta_roadmap)

        # Show the scraped images and links
        if image_urls:
            st.write(f"Found {len(image_urls)} images:")
            for img_url in image_urls[:5]:  # Show only first 5 images for simplicity
                st.image(img_url, caption="Image", use_column_width=True)
        
        if link_urls:
            st.write(f"Found {len(link_urls)} links:")
            for link in link_urls[:5]:  # Show only first 5 links
                st.write(f"[Link]({link})")

