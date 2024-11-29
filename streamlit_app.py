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

# Feature 5: Sentiment Analysis
def analyze_sentiment(text_data):
    """ Perform sentiment analysis on the scraped text data. """
    sentiment = TextBlob(text_data).sentiment
    return sentiment

# Feature 6: Word Frequency Analysis
def analyze_word_frequency(text_data):
    """ Analyze word frequency and plot most common words. """
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
    """ Display a gallery of images scraped from the website. """
    st.write("Displaying Images...")
    for img_url in image_urls[:5]:  # Show only first 5 images for simplicity
        st.image(img_url, caption="Scraped Image", use_column_width=True)

# Feature 8: Show Links List
def show_links_list(link_urls):
    """ Display a list of links scraped from the website. """
    st.write("Found Links:")
    for link in link_urls[:5]:  # Show only first 5 links for simplicity
        st.write(f"[{link}]({link})")

# Feature 9: Keyword Extraction
def extract_keywords(text_data):
    """ Extract and return the top 5 keywords from the text. """
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text_data])
    feature_names = vectorizer.get_feature_names_out()
    dense = X.todense()
    keyword_scores = dense.tolist()[0]
    keywords = [(feature_names[i], keyword_scores[i]) for i in range(len(feature_names))]
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:5]
    return keywords

# Feature 10: Random Product Improvement Suggestion
def random_product_suggestion():
    """ Generate a random product improvement suggestion. """
    suggestions = [
        "Improve the user interface for better accessibility.",
        "Offer a mobile version of the product.",
        "Add social media sharing options.",
        "Implement a loyalty rewards system.",
        "Integrate voice search functionality.",
        "Improve product documentation and FAQs.",
        "Offer personalized recommendations based on user behavior.",
        "Increase product speed and responsiveness.",
        "Enable multi-language support.",
        "Add dark mode for a better user experience."
    ]
    return random.choice(suggestions)

# Feature 11: Show Product Details (e.g., price, features)
def show_product_details(product_name, price, features):
    """ Display detailed product information. """
    st.write(f"Product: {product_name}")
    st.write(f"Price: {price}")
    st.write("Features:")
    for feature in features:
        st.write(f"- {feature}")

# Feature 12: Display Current Date and Time
def display_current_datetime():
    """ Display current date and time. """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Current Date and Time: {current_time}")

# Feature 13: Show Data Table from Scraped Text
def display_data_table(text_data):
    """ Convert text data to a table of unique words. """
    words = text_data.split()
    word_df = pd.DataFrame({"Word": words, "Count": [words.count(w) for w in words]})
    word_df = word_df.drop_duplicates(subset="Word")
    word_df = word_df.sort_values(by="Count", ascending=False)
    st.write(word_df)

# Feature 14: Show Related Products (Based on URL)
def show_related_products(url):
    """ Show related products based on website URL. """
    related_products = [
        "Product A - Best Seller",
        "Product B - New Arrival",
        "Product C - Recommended for You",
    ]
    st.write("Related Products:")
    for product in related_products:
        st.write(f"- {product}")

# Feature 15: Display Product Review Summary
def show_product_reviews_summary(product_reviews):
    """ Display a summary of product reviews. """
    st.write("Product Review Summary:")
    st.write(f"Total Reviews: {len(product_reviews)}")
    st.write(f"Average Rating: {np.mean([review['rating'] for review in product_reviews])}")

# Feature 16: Display Competitor Comparison Chart
def show_competitor_comparison(data):
    """ Display a bar chart comparing competitors. """
    competitors = ["Competitor A", "Competitor B", "Competitor C"]
    values = [data[competitor] for competitor in competitors]
    plt.bar(competitors, values)
    plt.title("Competitor Comparison")
    st.pyplot()

# Feature 17: Show Search Trends for Product Keywords
def show_search_trends(keywords):
    """ Display search trends for the product keywords. """
    trends = {keyword: random.randint(100, 1000) for keyword in keywords}
    st.write("Search Trends for Keywords:")
    st.write(trends)

# Feature 18: Display Pricing Insights
def display_pricing_insights(pricing_data):
    """ Display pricing insights. """
    st.write("Pricing Insights:")
    st.write(f"Lowest Price: {min(pricing_data)}")
    st.write(f"Highest Price: {max(pricing_data)}")
    st.write(f"Average Price: {np.mean(pricing_data)}")

# Feature 19: Display User Feedback Analysis
def analyze_user_feedback(feedback_data):
    """ Analyze and visualize user feedback. """
    feedback = pd.DataFrame(feedback_data)
    feedback_summary = feedback.groupby('rating').size()
    st.write("User Feedback Summary:")
    st.write(feedback_summary)

# Feature 20: Display Product Usage Stats
def display_usage_stats(usage_data):
    """ Display stats on product usage. """
    st.write("Product Usage Statistics:")
    st.write(f"Total Users: {usage_data['total_users']}")
    st.write(f"Active Users: {usage_data['active_users']}")
    st.write(f"Inactive Users: {usage_data['inactive_users']}")

# Feature 21: Display Marketing Campaign Analysis
def display_marketing_campaigns(campaign_data):
    """ Display analysis of marketing campaigns. """
    st.write("Marketing Campaigns:")
    st.write(f"Total Campaigns: {len(campaign_data)}")
    st.write(f"Campaigns Performance: {np.mean([campaign['performance'] for campaign in campaign_data])}")

# Feature 22: Display Social Media Mentions
def display_social_media_mentions(social_media_data):
    """ Display social media mentions. """
    st.write("Social Media Mentions:")
    for platform, mentions in social_media_data.items():
        st.write(f"{platform}: {mentions} mentions")

# Feature 23: Predict Future Trends (Based on Data)
def predict_future_trends(data):
    """ Predict future trends based on current data. """
    future_trend = np.polyfit(range(len(data)), data, 1)[0]
    st.write(f"Predicted Future Trend: {future_trend}")

# Feature 24: Display Competitor Product Reviews
def display_competitor_reviews(competitor_reviews):
    """ Display reviews for competitor products. """
    st.write("Competitor Product Reviews:")
    for review in competitor_reviews:
        st.write(f"Rating: {review['rating']} - {review['review_text']}")

# Feature 25: Show Seasonal Product Trends
def show_seasonal_trends(seasonal_data):
    """ Show seasonal trends for products. """
    st.write("Seasonal Trends:")
    st.write(seasonal_data)

# Feature 26: Generate User Persona
def generate_user_persona(user_data):
    """ Generate a user persona based on user data. """
    persona = {
        "Name": user_data['name'],
        "Age": user_data['age'],
        "Location": user_data['location'],
        "Interests": user_data['interests']
    }
    st.write("User Persona:")
    st.write(persona)

# Feature 27: Show Marketing Strategy Suggestions
def show_marketing_strategy_suggestions():
    """ Show marketing strategy suggestions. """
    strategies = [
        "Increase social media presence.",
        "Run email campaigns targeting specific demographics.",
        "Leverage influencers for brand promotion.",
        "Offer limited-time discounts."
    ]
    st.write("Marketing Strategy Suggestions:")
    for strategy in strategies:
        st.write(f"- {strategy}")

# Feature 28: Show Competitive Pricing Analysis
def show_competitive_pricing_analysis(pricing_data):
    """ Show competitive pricing analysis. """
    st.write("Competitive Pricing Analysis:")
    st.write(pricing_data)

# Feature 29: Show Customer Satisfaction Analysis
def show_customer_satisfaction(customer_feedback):
    """ Show customer satisfaction analysis. """
    satisfaction = pd.DataFrame(customer_feedback)
    st.write("Customer Satisfaction Analysis:")
    st.write(satisfaction.groupby('rating').size())

# Feature 30: Display Website Traffic Insights
def display_website_traffic(traffic_data):
    """ Display website traffic insights. """
    st.write("Website Traffic Insights:")
    st.write(f"Total Visits: {traffic_data['total_visits']}")
    st.write(f"New Visits: {traffic_data['new_visits']}")
    st.write(f"Returning Visits: {traffic_data['returning_visits']}")

# Feature 31: Display Product Launch Timeline
def display_product_launch_timeline(timeline_data):
    """ Display the product launch timeline. """
    st.write("Product Launch Timeline:")
    for phase, date in timeline_data.items():
        st.write(f"{phase}: {date}")

# Feature 32: Display Marketing Campaign ROI
def display_campaign_roi(campaign_data):
    """ Display marketing campaign ROI. """
    st.write("Marketing Campaign ROI:")
    for campaign in campaign_data:
        st.write(f"Campaign {campaign['name']} - ROI: {campaign['roi']}")

# Feature 33: Display Product Trial Statistics
def display_trial_stats(trial_data):
    """ Display statistics on product trials. """
    st.write("Product Trial Statistics:")
    st.write(f"Total Trials: {trial_data['total_trials']}")
    st.write(f"Converted Trials: {trial_data['converted_trials']}")

# Feature 34: Show Customer Demographics
def show_customer_demographics(customer_data):
    """ Show customer demographics. """
    st.write("Customer Demographics:")
    st.write(customer_data)

# Feature 35: Show Product Value Proposition
def show_product_value_proposition(value_proposition):
    """ Show the product's value proposition. """
    st.write("Product Value Proposition:")
    st.write(value_proposition)

# Feature 36: Display Product Testimonials
def display_product_testimonials(testimonials):
    """ Display product testimonials. """
    st.write("Product Testimonials:")
    for testimonial in testimonials:
        st.write(f"{testimonial['name']}: {testimonial['text']}")

# Feature 37: Display Customer Support Analysis
def display_customer_support_analysis(support_data):
    """ Display customer support analysis. """
    st.write("Customer Support Analysis:")
    st.write(f"Total Tickets: {support_data['total_tickets']}")
    st.write(f"Resolved Tickets: {support_data['resolved_tickets']}")

# Feature 38: Display User Growth Chart
def display_user_growth_chart(user_growth):
    """ Display a chart showing user growth over time. """
    plt.plot(user_growth)
    plt.title("User Growth Over Time")
    st.pyplot()

# Feature 39: Display Customer Retention Insights
def display_customer_retention_insights(retention_data):
    """ Display customer retention insights. """
    st.write("Customer Retention Insights:")
    st.write(retention_data)

# Feature 40: Display Sales Funnel Analysis
def display_sales_funnel(sales_data):
    """ Display sales funnel analysis. """
    st.write("Sales Funnel Analysis:")
    st.write(sales_data)

# Feature 41: Display A/B Testing Results
def display_ab_testing_results(ab_data):
    """ Display A/B testing results. """
    st.write("A/B Testing Results:")
    st.write(ab_data)

# Feature 42: Display Conversion Rate Optimization (CRO) Tips
def display_cro_tips():
    """ Display conversion rate optimization tips. """
    tips = [
        "Improve website load time.",
        "Optimize mobile user experience.",
        "Use strong call-to-action buttons.",
        "Offer free shipping."
    ]
    st.write("CRO Tips:")
    for tip in tips:
        st.write(f"- {tip}")

# Feature 43: Display User Engagement Insights
def display_user_engagement(user_engagement):
    """ Display user engagement insights. """
    st.write("User Engagement Insights:")
    st.write(user_engagement)

# Feature 44: Display Email Campaign Performance
def display_email_campaign_performance(email_data):
    """ Display email campaign performance. """
    st.write("Email Campaign Performance:")
    st.write(email_data)

# Feature 45: Display Product Roadmap
def display_product_roadmap(roadmap):
    """ Display product roadmap. """
    st.write("Product Roadmap:")
    st.write(roadmap)

# Feature 46: Display Conversion Funnel Analysis
def display_conversion_funnel(funnel_data):
    """ Display conversion funnel analysis. """
    st.write("Conversion Funnel Analysis:")
    st.write(funnel_data)

# Feature 47: Show Feature Requests
def show_feature_requests(requests_data):
    """ Show feature requests. """
    st.write("Feature Requests:")
    st.write(requests_data)

# Feature 48: Display Key Performance Indicators (KPIs)
def display_kpis(kpis):
    """ Display KPIs. """
    st.write("Key Performance Indicators:")
    st.write(kpis)

# Feature 49: Show Customer Loyalty Insights
def display_loyalty_insights(loyalty_data):
    """ Show customer loyalty insights. """
    st.write("Customer Loyalty Insights:")
    st.write(loyalty_data)

# Feature 50: Show Competitor Benchmarking
def show_competitor_benchmarking(benchmark_data):
    """ Show competitor benchmarking data. """
    st.write("Competitor Benchmarking:")
    st.write(benchmark_data)

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
        
        # Random Product Suggestion
        random_suggestion = random_product_suggestion()
        st.write(f"Random Product Suggestion: {random_suggestion}")
